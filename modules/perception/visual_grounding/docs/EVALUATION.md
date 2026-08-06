# Four-Model Evaluation

All reported methods use the same 105 image IDs, source prompts, and corrected boxes from `examples/ground_truth_boxes.csv`.

## Saved predictions

- Grounding DINO: `examples/outputs/grounding_dino_results.csv`
- OWL-ViT: `examples/outputs/owlvit_results.csv`
- GPT Vision: `examples/outputs/gpt_vision_results.csv`
- GPT-guided OWL-ViT: `examples/outputs/gpt_guided_owlvit/gpt_guided_owlvit_results.csv`

`scripts/build_final_metrics.py` verifies that each file contains the same image-ID set before producing the report.

## Metrics

- IoU: intersection over union between the predicted and corrected ground-truth boxes
- Mean IoU: average across all 105 rows, with failed predictions counted as zero
- Median IoU: median across all 105 rows
- Weak overlap: IoU at least 0.10
- Primary success: IoU at least 0.25
- Strict success: IoU at least 0.50
- Prediction failure: no valid successful predicted box

The repository retains the final summary charts and one representative four-model comparison. The full set of per-model overlays can be regenerated when the complete benchmark image corpus is restored locally.

Notebooks 03 and 04 regenerate predictions. Notebook 05 and `scripts/build_final_metrics.py` rebuild the common report. GPT outputs can vary between calls, so the committed CSV files should be replaced only during an intentional full evaluation.
