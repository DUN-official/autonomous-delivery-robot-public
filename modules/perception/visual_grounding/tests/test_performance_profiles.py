from pathlib import Path

import pytest
from pydantic import ValidationError

from grounding.config import load_config
from grounding.schemas import GroundingRequest, ImagePayload, PerformanceMode
from grounding.services.api_service import (
    profile_latency_ms,
    validate_profile_backend,
)
from grounding.video.live_session import LiveCameraSessionManager
from grounding.video.processor import VideoGroundingProcessor
from grounding.video.service_adapter import build_video_grounding_plan
from grounding.video.session_manager import VideoSessionManager


def test_web_interface_exposes_all_profiles_and_defaults_to_quality():
    html = Path("src/grounding/web/index.html").read_text(encoding="utf-8")

    assert html.count('name="performance_mode"') == 3
    assert html.count('<option value="quality" selected>') == 3
    assert 'data.set("performance_mode", "balanced")' not in html
    assert 'quality: "600000"' in html
    assert 'balanced: "300000"' in html
    assert 'fast: "120000"' in html


def test_profile_latency_budgets_allow_quality_to_finish():
    assert profile_latency_ms(PerformanceMode.QUALITY) == 600_000
    assert profile_latency_ms(PerformanceMode.BALANCED) == 300_000
    assert profile_latency_ms(PerformanceMode.FAST) == 120_000


def test_quality_rejects_incompatible_explicit_backend():
    with pytest.raises(Exception) as exc_info:
        validate_profile_backend(PerformanceMode.QUALITY, "yolo")

    assert getattr(exc_info.value, "status_code", None) == 400
    validate_profile_backend(PerformanceMode.QUALITY, "auto")
    validate_profile_backend(PerformanceMode.QUALITY, "gpt_guided_owlvit")


def test_request_schema_accepts_quality_latency_budget():
    request = GroundingRequest(
        image=ImagePayload(path="scene.jpg"),
        instruction="find the package",
        performance_mode=PerformanceMode.QUALITY,
        maximum_latency_ms=600_000,
    )

    assert request.maximum_latency_ms == 600_000
    with pytest.raises(ValidationError):
        GroundingRequest(
            image=ImagePayload(path="scene.jpg"),
            instruction="find the package",
            maximum_latency_ms=900_001,
        )


def test_quality_auto_routing_is_guided_for_recorded_and_live_video():
    plan = build_video_grounding_plan("track the package")

    assert VideoGroundingProcessor._select_backend(None, plan, "quality") == (
        "gpt_guided_owlvit"
    )
    assert LiveCameraSessionManager._select_backend(None, plan, "quality") == (
        "gpt_guided_owlvit"
    )


def test_recorded_video_session_queues_selected_profile(tmp_path):
    manager = VideoSessionManager(tmp_path)
    manager.shutdown()

    class _Executor:
        def __init__(self):
            self.kwargs = None

        def submit(self, function, **kwargs):
            self.kwargs = kwargs

    executor = _Executor()
    manager._executor = executor
    session_id = manager.create(
        input_path=tmp_path / "video.mp4",
        instruction="track the package",
        backend=None,
        service_url="http://127.0.0.1:8000",
        performance_mode="quality",
        maximum_latency_ms=600_000,
    )

    status = manager.get(session_id)
    assert status["performance_mode"] == "quality"
    assert status["maximum_latency_ms"] == 600_000
    assert executor.kwargs["performance_mode"] == "quality"
    assert executor.kwargs["maximum_latency_ms"] == 600_000


def test_live_session_stores_selected_profile(monkeypatch):
    class _Thread:
        def __init__(self, *args, **kwargs):
            self.started = False

        def start(self):
            self.started = True

        def is_alive(self):
            return False

        def join(self, timeout=None):
            return None

    monkeypatch.setattr("grounding.video.live_session.threading.Thread", _Thread)
    manager = LiveCameraSessionManager()
    session_id = manager.create(
        instruction="track the package",
        backend=None,
        camera_index=0,
        service_url="http://127.0.0.1:8000",
        performance_mode="quality",
        maximum_latency_ms=600_000,
    )

    status = manager.get(session_id)
    assert status["performance_mode"] == "quality"
    assert status["maximum_latency_ms"] == 600_000


def test_guided_config_uses_extended_call_timeout():
    config = load_config("configs/grounding_service.local.json")

    assert config.backends.gpt_guided_owlvit.openai_timeout_seconds == 120.0
