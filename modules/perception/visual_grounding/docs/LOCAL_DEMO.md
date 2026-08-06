# Local Demo Runbook

## Install

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[service,yolo,owlvit,dino,gpt,video,evaluation,test]"
grounding-provision-owlvit
grounding-provision-dino
```

Set `OPENAI_API_KEY` only when using GPT Vision or GPT-guided OWL-ViT. Grounding DINO and OWL-ViT run locally after provisioning.

## Run

```powershell
grounding-service --config configs\grounding_service.local.json
```

Open `http://127.0.0.1:8000` and use an image from `examples/sample_images/`, or supply another local indoor image.

## Suggested review

1. Run the same instruction with Grounding DINO and OWL-ViT.
2. Enable a GPT-backed method when credentials are available.
3. Compare the returned box, confidence, backend, total latency, and stage timing.
4. Upload a short video to review acquisition and tracking.
5. Review `results/final/README.md` for the saved 105-image benchmark summary.

Generated logs, uploads, and videos are written under `runtime/` and are not tracked.
