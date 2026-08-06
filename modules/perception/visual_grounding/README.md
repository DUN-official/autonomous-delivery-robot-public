# Visual Grounding and Video Tracking

This module maps a natural-language instruction and an indoor image to a target bounding box. It supports still images, uploaded video, live-camera acquisition, a localhost interface, tracking, optional reacquisition, and saved four-method evaluation results.

## Included methods

1. Grounding DINO
2. OWL-ViT
3. GPT Vision
4. GPT-guided OWL-ViT

The local application runs through FastAPI at `http://127.0.0.1:8000`. Grounding DINO and OWL-ViT run locally after their weights are provisioned. GPT-backed methods require `OPENAI_API_KEY`. Video sessions use language-guided acquisition followed by tracking and optional reacquisition.

## Module contents

```text
configs/              local and example service configuration
docs/                 evaluation and run notes
examples/outputs/     saved predictions for all four methods
notebooks/            five ordered Colab notebooks
results/final/         metric tables and summary charts
schemas/               structured output contract
scripts/               service, evaluation, and visualization helpers
src/grounding/         application source
tests/                 service and backend unit tests
```

Model weights, API credentials, raw uploads, local runtime sessions, and the full image corpus are not committed. A small set of sample images is included for interface checks; saved CSV outputs preserve the full 105-image benchmark results.

## Installation

Python 3.11 or 3.12 is supported.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[service,yolo,owlvit,dino,gpt,video,evaluation,test]"
grounding-provision-owlvit
grounding-provision-dino
```

Set the API key only when using a GPT-backed method:

```powershell
$env:OPENAI_API_KEY = "your-api-key"
```

## Run the service

```powershell
grounding-service --config configs\grounding_service.local.json
```

Open `http://127.0.0.1:8000`, upload an image or video, enter an instruction, and select a method. A command-line image request is also available:

```powershell
ground-image "examples\sample_images\vid_res_018_package_hidden_by_chair_frame_02.jpg" "find the package hidden behind the chair" --backend grounding_dino
```

## Evaluation

All methods use the same 105 image IDs, instructions, and corrected boxes. Failed predictions count as zero IoU.

| Method | Mean IoU | Median IoU | IoU >= 0.25 | IoU >= 0.50 | Failures |
|---|---:|---:|---:|---:|---:|
| Grounding DINO | 0.178 | 0.038 | 21.0% | 16.2% | 0 |
| OWL-ViT | 0.344 | 0.082 | 43.8% | 41.0% | 0 |
| GPT Vision | 0.300 | 0.280 | 54.3% | 21.0% | 0 |
| GPT-guided OWL-ViT | **0.473** | **0.573** | **78.1%** | **57.1%** | 2 |

Rebuild the compact report from the committed predictions with:

```powershell
python scripts\build_final_metrics.py
```

Evaluation definitions are in [docs/EVALUATION.md](docs/EVALUATION.md). Six recorded-video and live-camera examples are indexed in the repository [demo catalogue](../../../demos/README.md#visual-grounding-and-tracking).

## Tests

```powershell
pytest
```

The module currently has 61 automated tests. Tests that depend on an optional model or network service use mocks or explicit dependency checks.

## Robot integration status

The service returns structured boxes, confidence, method, timing, parser, and error information suitable for a ROS adapter. The remaining robot-facing work is to add depth, transform the selected point into the robot frame, apply confidence and safety checks, and send only verified targets to Nav2 or MoveIt 2.
