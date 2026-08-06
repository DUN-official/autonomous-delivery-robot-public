# Uncertainty Gating

Uncertainty gating is the planned interface between a perception result and a robot action. Its purpose is to prevent a weak label read, place prediction, detection, or grounded target from being executed automatically.

The gate will evaluate model confidence and status, agreement across observations, target stability after tracking or reacquisition, depth and coordinate validity, physical reachability, and disagreement between metric and semantic location cues.

The visual-grounding service already returns structured confidence, method, latency, bounding-box, and error fields. The shared ROS decision policy that combines those fields with navigation and manipulation state remains in progress.
