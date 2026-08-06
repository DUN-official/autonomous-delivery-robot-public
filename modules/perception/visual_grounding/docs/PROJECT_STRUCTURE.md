# Visual-Grounding Module Structure

This directory contains the grounding code and the compact evidence needed to review its behaviour without committing local model weights, credentials, runtime uploads, or the full image corpus.

## Tracked

- `configs/` - localhost and example configuration
- `docs/` - run and evaluation notes
- `examples/sample_images/` - three small interface-check images
- `examples/outputs/` - saved predictions for the 105-image benchmark
- `notebooks/` - ordered Colab workflow
- `results/final/` - summary metrics and figures
- `schemas/` - structured result contract
- `scripts/` - service and report utilities
- `src/` - application source
- `tests/` - automated tests
- `.env.example` and `pyproject.toml`

The entire repository is covered by the [root MIT License](../../../../LICENSE).

## Restored locally

- `models/` through the provisioning commands or documented checkpoints
- `.venv/` through `pyproject.toml`
- `runtime/` when the service processes requests
- the full benchmark images when predictions are intentionally regenerated

Keeping generated and heavyweight files outside Git prevents accidental credential, upload, checkpoint, and duplicate-result commits.
