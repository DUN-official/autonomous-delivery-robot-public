# Results and Metrics

## Phase 1

### Navigation and localization

All tested room-to-room Nav2 tasks completed in the mapped Gazebo condominium. The robot maintained a stable AMCL pose estimate during nominal navigation, and no localization loss, navigation abort, collision, or control instability was reported in those trials. These results validate the tested map, transform, AMCL, costmap, planner, and controller configuration; they are not a comparison against alternative navigation systems.

### Package and human detection

Offline object-detection evaluation used an IoU true-positive threshold of 0.50.

| Detector | Evaluation set | Best F1 | Precision | Recall | Approx. AP |
|---|---:|---:|---:|---:|---:|
| Human | 1,149 images; 3,678 objects | 0.5808 | 0.6541 | 0.5223 | 0.5362 |
| Package | 16 images; 31 objects | 0.9180 | 0.9333 | 0.9032 | 0.9171 |

The human detector was suitable for awareness in the controlled simulation but remained notably weaker than the package detector on the more varied offline dataset.

### Label reading and pick/place

Label reading and package manipulation were evaluated qualitatively. The controlled `Apt 4B` example showed occasional confusion between `B` and `8`. The ArUco-guided manipulation chain completed successful pick/place runs, while other trials exposed planning sensitivity and occasional obstacle collisions.

## Phase 2

### Elevator entry

The YOLOv8n elevator-door detector reached approximately 0.98 mAP50-95 on the simulated dataset. The guarded motion logic produced 100% trigger success with no false movement triggers in the tested Gazebo sequences. These values apply to the controlled simulation and do not represent real-elevator performance.

### Elevator-button interaction

The button workflow demonstrated the complete ROS sequence from a requested floor button to a detected image coordinate, Cartesian target, inverse-kinematics solution, and RViz arm motion. Class imbalance and inconsistent labels created a precision-recall trade-off in the detector, so this remains a proof of concept.

### Semantic localization

The ResNet18 classifier was trained for nine semantic building locations using 5,383 training images, 1,340 validation images, and 608 test images.

| Metric | Result |
|---|---:|
| Test accuracy | 0.7780 |
| Test loss | 0.8260 |
| Micro ROC AUC | 0.9714 |
| Macro ROC AUC | 0.9821 |

The strongest class F1 score was `floor3_hallway` at 0.9091. The weakest was `floor2_elevator_landmark` at 0.4928, reflecting confusion between visually similar hallway and elevator-adjacent views.

## Phase 3

### Visual grounding

All four methods use the same 105 images, instructions, and corrected ground-truth boxes. Mean and median IoU include failed predictions as zero.

| Method | Mean IoU | Median IoU | IoU >= 0.10 | IoU >= 0.25 | IoU >= 0.50 | Failures |
|---|---:|---:|---:|---:|---:|---:|
| Grounding DINO | 0.178 | 0.038 | 32.4% | 21.0% | 16.2% | 0 |
| OWL-ViT | 0.344 | 0.082 | 48.6% | 43.8% | 41.0% | 0 |
| GPT Vision | 0.300 | 0.280 | 79.0% | 54.3% | 21.0% | 0 |
| GPT-guided OWL-ViT | **0.473** | **0.573** | **81.9%** | **78.1%** | **57.1%** | 2 |

![Grounding success rates](../assets/screenshots/visual_grounding_success_rates.png)

The guided pipeline produced the strongest overlap results, while direct GPT Vision produced broad weak-overlap coverage. Saved per-image predictions and metric-generation scripts are committed with the [visual-grounding module](../modules/perception/visual_grounding/README.md).

### Learned navigation

The DQN environment uses a 24-value LiDAR observation with a relative target vector, a replay buffer of 1,000 transitions, a target network updated every 1,000 steps, and epsilon-greedy exploration decaying from 1.0 to 0.05. The reward includes progress toward the goal, a +200 goal reward, a -200 collision penalty, and a -0.1 step cost. Demonstrations cover stationary and moving obstacles; a shared quantitative comparison with Nav2 remains in progress.
