# Saved Model Outputs

The committed CSV files preserve the predictions used for the final 105-image comparison:

- `grounding_dino_results.csv`
- `owlvit_results.csv`
- `gpt_vision_results.csv`
- `gpt_guided_owlvit/gpt_guided_owlvit_results.csv`

The additional guided-method CSV files record candidate proposals, selection decisions, and bounded box adjustments used to produce the final guided result.

These files should be replaced only during an intentional full rerun on the same corrected ground-truth set.
