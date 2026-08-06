# Final Four-Model Metrics

All models were evaluated on the same 105-image benchmark and corrected ground-truth boxes.

| Model | Mean IoU | Median IoU | IoU >= 0.10 | IoU >= 0.25 | IoU >= 0.50 | Failures |
|---|---:|---:|---:|---:|---:|---:|
| Grounding DINO | 0.178 | 0.038 | 32.4% | 21.0% | 16.2% | 0 |
| OWL-ViT | 0.344 | 0.082 | 48.6% | 43.8% | 41.0% | 0 |
| GPT Vision | 0.300 | 0.280 | 79.0% | 54.3% | 21.0% | 0 |
| GPT-guided OWL-ViT | **0.473** | **0.573** | **81.9%** | **78.1%** | **57.1%** | 2 |

The CSV files in `examples/outputs/` are the saved per-image predictions. Run `python scripts/build_final_metrics.py` from the module root to verify the image-ID sets and rebuild this report.
