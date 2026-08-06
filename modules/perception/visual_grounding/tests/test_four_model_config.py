import json

from grounding.config import load_config
from grounding.services.local_service import LocalGroundingService


def test_canonical_config_exposes_four_evaluation_backends():
    config = load_config("configs/grounding_service.local.json")

    assert config.backends.grounding_dino.enabled
    assert config.backends.owlvit.enabled
    assert config.backends.gpt_vision.enabled
    assert config.backends.gpt_guided_owlvit.enabled


def test_canonical_config_constructs_complete_local_service():
    config = load_config("configs/grounding_service.local.json")

    service = LocalGroundingService.from_config(config)

    assert set(service.backends) >= {
        "grounding_dino",
        "owlvit",
        "gpt_vision",
        "gpt_guided_owlvit",
    }


def test_web_interface_lists_four_evaluation_backends():
    html = open("src/grounding/web/index.html", encoding="utf-8").read()
    for backend in ("grounding_dino", "owlvit", "gpt_vision", "gpt_guided_owlvit"):
        assert f'value="{backend}"' in html


def test_local_config_is_valid_json():
    with open("configs/grounding_service.local.json", encoding="utf-8") as handle:
        assert "backends" in json.load(handle)
