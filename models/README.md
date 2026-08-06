# Model Assets

Large model files are not stored in this repository. This keeps the clone manageable and prevents model versions from being separated from their retrieval or training instructions.

The project uses:

- YOLOv8 weights for package, human, elevator-door, and elevator-button detection;
- a fine-tuned ResNet18 checkpoint for nine-class semantic localization;
- Grounding DINO and OWL-ViT for open-vocabulary visual grounding; and
- optional GPT Vision requests for direct and guided grounding experiments.

The visual-grounding module includes provisioning commands for its local Transformers models:

```powershell
cd modules\perception\visual_grounding
grounding-provision-owlvit
grounding-provision-dino
```

Detection and semantic-localization checkpoint retrieval or training instructions will be published with the ROS packages that consume them. This keeps each result tied to a documented model version, class map, preprocessing path, and node configuration.
