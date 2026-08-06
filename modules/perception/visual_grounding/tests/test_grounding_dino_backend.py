from PIL import Image

from grounding.backends.grounding_dino_backend import GroundingDINOBackend
from grounding.schemas import GroundingRequest, ImagePayload


class FakeDetector:
    def __init__(self):
        self.calls = []

    def __call__(self, image, candidate_labels=None, threshold=0.0):
        self.calls.append((image.size, candidate_labels, threshold))
        return [
            {
                "score": 0.81,
                "label": candidate_labels[0],
                "box": {"xmin": 10, "ymin": 12, "xmax": 80, "ymax": 70},
            }
        ]


def test_dino_detects_and_returns_local_candidate(tmp_path):
    image_path = tmp_path / "room.jpg"
    Image.new("RGB", (100, 80), "white").save(image_path)
    backend = GroundingDINOBackend(
        model_path=tmp_path,
        warmup_on_startup=False,
        max_image_width=100,
    )
    backend._detector = FakeDetector()
    backend._started = True
    request = GroundingRequest(
        image=ImagePayload.from_path(image_path),
        instruction="find the chair",
        target_object="chair",
    )

    result = backend.ground(request)

    assert result.status == "success"
    assert result.backend_used == "grounding_dino"
    assert result.bbox_xyxy.as_list() == [10.0, 12.0, 80.0, 70.0]
    assert result.confidence == 0.81
    assert backend._detector.calls[0][1][0] == "chair"


def test_dino_inference_path_contains_no_model_download():
    import inspect

    source = inspect.getsource(GroundingDINOBackend._ground_impl)
    assert "from_pretrained" not in source
    assert "snapshot_download" not in source
