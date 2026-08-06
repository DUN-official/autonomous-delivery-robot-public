from __future__ import annotations

import json
import os
import time

from ..image_utils import image_to_data_url, load_pil_image
from ..interface import GroundingBackend
from ..schemas import (
    BBoxXYXY,
    GroundingPrediction,
    GroundingResult,
    GroundingStatus,
    TraceEvent,
)


class GPTVisionBackend(GroundingBackend):
    """Direct GPT Vision bounding-box baseline exposed through the local service."""

    def __init__(
        self,
        *,
        openai_model,
        api_key_env="OPENAI_API_KEY",
        image_detail="high",
        image_max_width=1600,
        jpeg_quality=88,
        openai_timeout_seconds=30.0,
        openai_max_retries=1,
        allowed_image_roots=None,
        max_image_bytes=30 * 1024 * 1024,
    ):
        super().__init__("gpt_vision")
        self.openai_model = openai_model
        self.api_key_env = api_key_env
        self.image_detail = image_detail
        self.image_max_width = image_max_width
        self.jpeg_quality = jpeg_quality
        self.openai_timeout_seconds = openai_timeout_seconds
        self.openai_max_retries = openai_max_retries
        self.allowed_image_roots = allowed_image_roots
        self.max_image_bytes = max_image_bytes
        self._client = None

    def startup(self):
        api_key = os.environ.get(self.api_key_env)
        if not api_key:
            raise EnvironmentError(f"missing API key environment variable: {self.api_key_env}")
        from openai import OpenAI

        self._client = OpenAI(
            api_key=api_key,
            timeout=self.openai_timeout_seconds,
            max_retries=self.openai_max_retries,
        )
        self._started = True
        self._health_detail = "direct GPT Vision grounding ready"
        self._model_reference = self.openai_model

    def shutdown(self):
        self._client = None
        super().shutdown()

    def _ground_impl(self, request):
        started = time.perf_counter()
        image = load_pil_image(
            request.image,
            allowed_roots=self.allowed_image_roots,
            max_bytes=self.max_image_bytes,
        )
        decode_ms = (time.perf_counter() - started) * 1000.0
        width, height = image.size
        data_url = image_to_data_url(
            image,
            quality=self.jpeg_quality,
            max_width=self.image_max_width,
        )
        prompt = self._prompt(request, width, height)

        request_started = time.perf_counter()
        response = self._client.responses.create(
            model=self.openai_model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": data_url,
                            "detail": self.image_detail,
                        },
                    ],
                }
            ],
        )
        gpt_ms = (time.perf_counter() - request_started) * 1000.0
        parsed = self._extract_json(response.output_text)
        if str(parsed.get("status", "failed")).strip().lower() != "success":
            return GroundingResult.failure(
                request,
                backend_used=self.name,
                message=str(parsed.get("notes") or "GPT Vision did not find the target"),
                clarification_required=True,
                trace=[
                    TraceEvent(stage="image_decode", duration_ms=decode_ms),
                    TraceEvent(stage="gpt_vision", duration_ms=gpt_ms),
                ],
            )

        box = BBoxXYXY(
            x_min=float(parsed["x_min"]),
            y_min=float(parsed["y_min"]),
            x_max=float(parsed["x_max"]),
            y_max=float(parsed["y_max"]),
        ).clipped(width, height)
        confidence = min(1.0, max(0.0, float(parsed.get("confidence", 0.5))))
        label = str(parsed.get("matched_phrase") or request.target_phrase or request.target_object or "target")
        prediction = GroundingPrediction(
            bbox_xyxy=box,
            confidence=confidence,
            label=label,
        )
        return GroundingResult(
            request_id=request.request_id,
            status=GroundingStatus.SUCCESS,
            bbox_xyxy=box,
            predictions=[prediction],
            confidence=confidence,
            backend_used=self.name,
            trace=[
                TraceEvent(stage="image_decode", duration_ms=decode_ms),
                TraceEvent(
                    stage="gpt_vision",
                    duration_ms=gpt_ms,
                    message="direct vision bounding-box response",
                ),
            ],
            metadata={
                "gpt_request_count": 1,
                "stage_latencies_ms": {
                    "image_decode": decode_ms,
                    "gpt_vision": gpt_ms,
                },
                "notes": str(parsed.get("notes", "")),
            },
        )

    @staticmethod
    def _extract_json(text):
        text = str(text).strip()
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("GPT Vision response did not contain a JSON object")
        parsed = json.loads(text[start : end + 1])
        required = ("x_min", "y_min", "x_max", "y_max")
        if str(parsed.get("status", "failed")).lower() == "success":
            missing = [key for key in required if parsed.get(key) is None]
            if missing:
                raise ValueError(f"GPT Vision response is missing coordinates: {missing}")
        return parsed

    @staticmethod
    def _prompt(request, width, height):
        return f"""
Return one JSON object only.
Image size: width={width}, height={height}.
Instruction: {request.instruction}
Parsed target: {request.target_phrase or request.target_object or "target object"}
Location hint: {request.location_hint or ""}
Find the visible target and return its bounding box in pixel coordinates.
Schema:
{{
  "status": "success" or "failed",
  "x_min": number,
  "y_min": number,
  "x_max": number,
  "y_max": number,
  "confidence": number between 0 and 1,
  "matched_phrase": string,
  "notes": string
}}
""".strip()
