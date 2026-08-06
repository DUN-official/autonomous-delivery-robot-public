import argparse
import json
from pathlib import Path

from grounding.config import load_config
from grounding.schemas import GroundingRequest, ImagePayload
from grounding.services.local_service import LocalGroundingService

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    parser.add_argument("instruction")
    parser.add_argument("--target-object")
    parser.add_argument("--location-hint")
    parser.add_argument("--image-id")
    parser.add_argument("--config", default="configs/grounding_service.local.json")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = root / config_path
    service = LocalGroundingService.from_config(load_config(config_path))
    service.startup()
    try:
        result = service.ground(
            GroundingRequest(
                image=ImagePayload.from_path(Path(args.image).resolve()),
                instruction=args.instruction,
                target_object=args.target_object,
                location_hint=args.location_hint,
                metadata={"image_id": args.image_id} if args.image_id else {},
            )
        )
        print(json.dumps(result.model_dump(mode="json"), indent=2))
    finally:
        service.shutdown()

if __name__ == "__main__":
    main()
