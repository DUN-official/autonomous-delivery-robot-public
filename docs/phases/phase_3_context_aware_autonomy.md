# Phase 3: Context-Aware Autonomy

## Objective

Add dynamic-obstacle navigation and language-guided target selection for less structured pickup and delivery scenes.

## Learned navigation

The DQN prototype uses a Pygame/Gymnasium environment with continuous 2D positions, a 24-value LiDAR observation, a relative goal vector, and moving obstacles. Its policy is trained with replay memory, a target network, and epsilon-greedy exploration. Demonstrations show reactions to stationary and moving obstacles. Comparison against Nav2 under matched scenarios remains part of the integration plan.

## Visual grounding

The grounding module translates instructions such as `find the package hidden behind the chair` and `go to the door at the end of the hallway` into image-space targets. The benchmark compares Grounding DINO, OWL-ViT, GPT Vision, and GPT-guided OWL-ViT on the same 105 images. GPT-guided OWL-ViT produced the strongest result, with 0.473 mean IoU and 57.1% success at IoU 0.50.

The service also supports uploaded-video and live-camera acquisition followed by tracking and optional reacquisition. Six public interface demonstrations cover packages, doors, a toy car, and a robot cube.

## Integration path

The remaining robot integration will add depth, camera-to-base transforms, motion feasibility, confidence checks, safety supervision, and recovery logic before a selected target can become a Nav2 or MoveIt 2 action.

## Published material

- [Context-aware demonstrations](../../demos/README.md#visual-grounding-and-tracking)
- [Visual-grounding module and benchmark](../../modules/perception/visual_grounding/README.md)
- [Detailed metrics](../results_and_metrics.md#phase-3)
- [Phase 3 limitations](../limitations.md#phase-3)
