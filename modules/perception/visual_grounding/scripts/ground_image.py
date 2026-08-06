"""Upload one existing image and one grounding instruction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import httpx


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    parser.add_argument("instruction")
    parser.add_argument("--target-object")
    parser.add_argument("--location-hint")
    parser.add_argument("--action")
    parser.add_argument("--backend")
    parser.add_argument("--service-url", default="http://127.0.0.1:8000")
    parser.add_argument("--maximum-latency-ms", type=int, default=10_000)
    args = parser.parse_args()

    image_path = Path(args.image).expanduser().resolve()
    if not image_path.is_file():
        raise FileNotFoundError(image_path)

    data = {
        "instruction": args.instruction,
        "maximum_latency_ms": str(args.maximum_latency_ms),
    }
    optional_fields = {
        "target_object": args.target_object,
        "location_hint": args.location_hint,
        "action": args.action,
        "preferred_backend": args.backend,
    }
    data.update({key: value for key, value in optional_fields.items() if value})

    with image_path.open("rb") as handle:
        response = httpx.post(
            f"{args.service_url.rstrip('/')}/v1/ground/upload",
            data=data,
            files={
                "image": (
                    image_path.name,
                    handle,
                    _media_type(image_path),
                )
            },
            timeout=max(30.0, args.maximum_latency_ms / 1000.0 + 5.0),
        )

    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))


def _media_type(path: Path) -> str:
    return {
        ".png": "image/png",
        ".webp": "image/webp",
    }.get(path.suffix.lower(), "image/jpeg")


if __name__ == "__main__":
    main()
