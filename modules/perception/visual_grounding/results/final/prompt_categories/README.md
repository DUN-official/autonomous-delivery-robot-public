# Prompt-category performance analysis

This report uses the existing saved predictions. It does not rerun a model and is separate from the live application.

## Headline results

| Model | Mean IoU | IoU ≥ 0.25 | IoU ≥ 0.50 |
|---|---:|---:|---:|
| Grounding DINO | 0.178 | 21.0% | 16.2% |
| OWL-ViT | 0.344 | 43.8% | 41.0% |
| GPT Vision | 0.300 | 54.3% | 21.0% |
| GPT-guided OWL-ViT | 0.473 | 78.1% | 57.1% |

## What the category results show

- **Grounding DINO:** strongest primary success on Attribute selection (37.9%); weakest on Multi-instance / ordinal (8.3%).
- **OWL-ViT:** strongest primary success on Attribute selection (62.1%); weakest on Multiple references (0.0%).
- **GPT Vision:** strongest primary success on Attribute selection (75.9%); weakest on Multiple references (16.7%).
- **GPT-guided OWL-ViT:** strongest primary success on Multiple references (100.0%); weakest on Direct target (33.3%).

## Why the guided setup is justified

GPT-guided OWL-ViT exceeds the best unguided result on primary localization in 6 of 9 reported category views. Its largest primary gain is +66.7% on Multiple references.

For spatial prompts, guided primary success is 81.5%, compared with 54.3% for the best unguided model. For complex prompts, the corresponding values are 76.6% and 55.3%.

The guided configuration is not uniformly superior. It does not exceed the best unguided primary-success result for Direct target, Multi-instance / ordinal, Negation. This supports retaining selectable backends and treating the guided pipeline as the accuracy-oriented choice for relation-heavy prompts, not as proof that it is optimal for every prompt.

The component pattern supports the architecture: GPT Vision is relatively effective at interpreting which object the instruction refers to, while OWL-ViT provides detector proposals and tighter boxes. The guided pipeline uses the language-aware stage to select/refine OWL-ViT candidates, addressing the standalone models' complementary weaknesses.

## Prompt taxonomy

Categories are deterministic, multi-label, and defined before aggregation. A prompt may therefore appear in more than one category.

- **All prompts:** Every benchmark prompt. Example: *man by door*.
- **Direct target:** Target naming without a spatial, attribute, multiplicity, negation, or occlusion constraint. Example: *elevator button panel*.
- **Spatial relation:** Uses a location, direction, proximity, support, or ordinal spatial relation. Example: *package beside the chair*.
- **Attribute selection:** Uses colour, clothing, posture, or visible-state information to select the target. Example: *man in blue*.
- **Multiple references:** Uses two or more reference objects or a chained relation. Example: *package between books and shoes*.
- **Multi-instance / ordinal:** Requests plural targets or selects one instance by rank, such as second closest. Example: *second closest package*.
- **Negation:** Excludes a target by a negative constraint. Example: *package not red*.
- **Occlusion:** Describes a target as covered, hidden, or occluded. Example: *package partially covered by chair*.
- **Complex instruction:** Combines at least two independent constraints, two spatial operators, or multiple references. Example: *man by the elevator green shirt*.

## Interpretation limits

- These are historical saved outputs, not a rerun of the latest Quality profile.
- The benchmark contains 105 frames from 35 short scenarios. Adjacent frames are related observations.
- Small categories, especially negation and multiple-reference prompts, should be treated as directional evidence rather than a final generalization claim.
- Category overlap means results answer different diagnostic questions and should not be added together.
- Target-correct and relation-match fields come from different evaluation procedures and are retained in the CSV but are not plotted as directly comparable measures.
- YOLO is not included because there is no saved YOLO result CSV for this benchmark.
- Latency was not measured in the saved result files, so this analysis supports accuracy claims only.

The frame-level category assignments are recorded in `prompt_category_assignments.csv`; the full metrics and guided uplift values are in the companion CSV files.
