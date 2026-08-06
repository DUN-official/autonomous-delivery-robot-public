from __future__ import annotations

from pathlib import Path
import time

from PIL import Image

from ..evaluation.metrics import box_iou
from ..exceptions import ModelProvisioningError
from ..image_utils import load_pil_image, resize_for_inference
from ..interface import GroundingBackend
from ..schemas import (
    BBoxXYXY,
    GroundingCandidate,
    GroundingPrediction,
    GroundingResult,
    GroundingStatus,
    TraceEvent,
)
from ..task_parser import normalize_text


class GroundingDINOBackend(GroundingBackend):
    """Local Grounding DINO zero-shot detector loaded once at service startup."""

    def __init__(
        self,
        *,
        model_path,
        device="auto",
        thresholds=None,
        top_k=6,
        max_pairwise_iou=0.85,
        max_image_width=1280,
        warmup_on_startup=True,
        allowed_image_roots=None,
        max_image_bytes=30 * 1024 * 1024,
    ):
        super().__init__("grounding_dino")
        self.model_path = Path(model_path)
        self.device_setting = device
        self.thresholds = thresholds or [0.08, 0.05, 0.02, 0.005]
        self.top_k = top_k
        self.max_pairwise_iou = max_pairwise_iou
        self.max_image_width = max_image_width
        self.warmup_on_startup = warmup_on_startup
        self.allowed_image_roots = allowed_image_roots
        self.max_image_bytes = max_image_bytes
        self._detector = None
        self._device = "cpu"

    def startup(self):
        if not self.model_path.is_dir():
            raise ModelProvisioningError(
                f"Grounding DINO local model directory is missing: {self.model_path}"
            )
        import torch
        from transformers import pipeline

        self._device = (
            "cuda"
            if self.device_setting == "auto" and torch.cuda.is_available()
            else "cpu"
            if self.device_setting == "auto"
            else self.device_setting
        )
        device_id = 0 if str(self._device).startswith("cuda") else -1
        self._detector = pipeline(
            task="zero-shot-object-detection",
            model=str(self.model_path),
            device=device_id,
        )
        self._started = True
        warmup = "not requested"
        if self.warmup_on_startup:
            try:
                self.detect_candidates(
                    _WarmupRequest(),
                    image=Image.new("RGB", (320, 240), "black"),
                    labels=["object"],
                    top_k=1,
                )
                warmup = "complete"
            except Exception as exc:
                warmup = f"skipped ({type(exc).__name__})"
        self._health_detail = f"Grounding DINO loaded on {self._device}; warmup {warmup}"
        self._model_reference = str(self.model_path)

    def shutdown(self):
        self._detector = None
        super().shutdown()

    def _ground_impl(self, request):
        started = time.perf_counter()
        image = load_pil_image(
            request.image,
            allowed_roots=self.allowed_image_roots,
            max_bytes=self.max_image_bytes,
        )
        decode_ms = (time.perf_counter() - started) * 1000.0
        inference_started = time.perf_counter()
        candidates = self.detect_candidates(
            request,
            image=image,
            top_k=request.maximum_results,
        )
        inference_ms = (time.perf_counter() - inference_started) * 1000.0
        if not candidates:
            return GroundingResult.failure(
                request,
                backend_used=self.name,
                message="Grounding DINO produced no candidate",
                clarification_required=True,
                trace=[
                    TraceEvent(
                        stage="grounding_dino_candidate_generation",
                        duration_ms=inference_ms,
                    )
                ],
            )

        count = request.maximum_results if request.quantity.value in {"multiple", "all"} else 1
        selected = candidates[:count]
        predictions = [
            GroundingPrediction(
                bbox_xyxy=candidate.bbox_xyxy,
                confidence=candidate.confidence,
                label=candidate.label,
                candidate_id=candidate.candidate_id,
            )
            for candidate in selected
        ]
        return GroundingResult(
            request_id=request.request_id,
            status=GroundingStatus.SUCCESS,
            bbox_xyxy=predictions[0].bbox_xyxy,
            predictions=predictions,
            confidence=predictions[0].confidence,
            backend_used=self.name,
            candidates=candidates,
            trace=[
                TraceEvent(stage="image_decode", duration_ms=decode_ms),
                TraceEvent(
                    stage="grounding_dino_candidate_generation",
                    duration_ms=inference_ms,
                    message="selected open-vocabulary candidate(s)",
                    data={"candidate_count": len(candidates)},
                ),
            ],
            metadata={
                "stage_latencies_ms": {
                    "image_decode": decode_ms,
                    "grounding_dino": inference_ms,
                }
            },
        )

    def detect_candidates(self, request, *, image=None, labels=None, top_k=None):
        if not self._started or self._detector is None:
            raise RuntimeError("Grounding DINO is not started")
        image = image or load_pil_image(
            request.image,
            allowed_roots=self.allowed_image_roots,
            max_bytes=self.max_image_bytes,
        )
        original_width, original_height = image.size
        inference_image, scale_x, scale_y = resize_for_inference(image, self.max_image_width)
        labels = labels or self._labels_for_request(request)
        labels = [value for value in dict.fromkeys(value.strip() for value in labels) if value]
        labels = labels or ["object"]
        top_k = top_k or self.top_k

        predictions = []
        used_threshold = None
        for threshold in self.thresholds:
            try:
                predictions = self._detector(
                    inference_image,
                    candidate_labels=labels,
                    threshold=float(threshold),
                )
            except TypeError:
                predictions = self._detector(
                    inference_image,
                    labels,
                    threshold=float(threshold),
                )
            if predictions:
                used_threshold = float(threshold)
                break

        candidates = []
        for prediction in predictions:
            raw_box = prediction.get("box") or {}
            try:
                box = BBoxXYXY(
                    x_min=float(raw_box["xmin"]) * scale_x,
                    y_min=float(raw_box["ymin"]) * scale_y,
                    x_max=float(raw_box["xmax"]) * scale_x,
                    y_max=float(raw_box["ymax"]) * scale_y,
                ).clipped(original_width, original_height)
                confidence = min(1.0, max(0.0, float(prediction.get("score", 0.0))))
            except (KeyError, TypeError, ValueError):
                continue
            candidates.append(
                GroundingCandidate(
                    candidate_id=f"dino_{len(candidates) + 1}",
                    bbox_xyxy=box,
                    confidence=confidence,
                    label=str(prediction.get("label", request.target_object or "object")),
                    source=self.name,
                    metadata={
                        "threshold": used_threshold,
                        "inference_size": list(inference_image.size),
                        "original_size": [original_width, original_height],
                    },
                )
            )

        candidates.sort(key=lambda item: item.confidence, reverse=True)
        kept = []
        for candidate in candidates:
            if any(
                box_iou(candidate.bbox_xyxy, existing.bbox_xyxy) > self.max_pairwise_iou
                for existing in kept
            ):
                continue
            candidate.candidate_id = f"dino_{len(kept) + 1}"
            kept.append(candidate)
            if len(kept) >= top_k:
                break
        return kept

    @staticmethod
    def _labels_for_request(request):
        target = normalize_text(request.target_object) or "object"
        labels = [target]
        if request.target_phrase and normalize_text(request.target_phrase) != target:
            labels.append(request.target_phrase)
        if request.attributes:
            labels.append(" ".join([*request.attributes, target]))
        if request.location_hint:
            labels.append(f"{target} {request.location_hint}")
        return labels


class _WarmupRequest:
    target_object = "object"
    target_phrase = "object"
    attributes = []
    location_hint = None
