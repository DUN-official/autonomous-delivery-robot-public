"""One-time model provisioning commands. Runtime inference never downloads weights."""

from __future__ import annotations

import argparse
from pathlib import Path


def _provision(*, description: str, default_repo: str, default_destination: str) -> None:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--repo-id", default=default_repo)
    parser.add_argument(
        "--destination",
        default=default_destination,
    )
    args = parser.parse_args()

    destination = Path(args.destination).expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)

    from huggingface_hub import snapshot_download

    snapshot_download(
        repo_id=args.repo_id,
        local_dir=str(destination),
    )
    print(f"Model provisioned at: {destination}")


def provision_owlvit() -> None:
    _provision(
        description="Download OWL ViT once into a local model directory",
        default_repo="google/owlvit-base-patch32",
        default_destination="models/owlvit/owlvit-base-patch32",
    )


def provision_grounding_dino() -> None:
    _provision(
        description="Download Grounding DINO once into a local model directory",
        default_repo="IDEA-Research/grounding-dino-tiny",
        default_destination="models/grounding_dino/grounding-dino-tiny",
    )
