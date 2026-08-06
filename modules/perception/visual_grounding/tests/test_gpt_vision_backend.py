from types import SimpleNamespace

from PIL import Image

from grounding.backends.gpt_vision_backend import GPTVisionBackend
from grounding.schemas import GroundingRequest, ImagePayload


class FakeResponses:
    def __init__(self, output_text):
        self.output_text = output_text
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(output_text=self.output_text)


def test_gpt_vision_returns_pixel_box(tmp_path):
    image_path = tmp_path / "room.jpg"
    Image.new("RGB", (200, 100), "white").save(image_path)
    backend = GPTVisionBackend(openai_model="test-model")
    responses = FakeResponses(
        'Result: {"status":"success","x_min":20,"y_min":10,'
        '"x_max":180,"y_max":90,"confidence":0.77,'
        '"matched_phrase":"chair","notes":"visible"}'
    )
    backend._client = SimpleNamespace(responses=responses)
    backend._started = True
    request = GroundingRequest(
        image=ImagePayload.from_path(image_path),
        instruction="find the chair beside the table",
        target_object="chair",
    )

    result = backend.ground(request)

    assert result.status == "success"
    assert result.backend_used == "gpt_vision"
    assert result.bbox_xyxy.as_list() == [20.0, 10.0, 180.0, 90.0]
    assert result.metadata["gpt_request_count"] == 1
    assert len(responses.calls) == 1


def test_gpt_json_extraction_rejects_missing_coordinates():
    try:
        GPTVisionBackend._extract_json('{"status":"success","x_min":1}')
    except ValueError as exc:
        assert "missing coordinates" in str(exc)
    else:
        raise AssertionError("missing coordinates were accepted")
