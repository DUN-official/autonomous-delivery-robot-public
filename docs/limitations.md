# Limitations

## Project-wide

- The current evidence comes from subsystem demonstrations rather than one uninterrupted lobby-to-door multi-floor run.
- Most robot motion and manipulation tests were completed in Gazebo, so real sensors, actuators, timing, lighting, and contact dynamics remain unvalidated.
- The complete ROS 2 source is still being consolidated and is not yet buildable from this repository root.

## Phase 1

- The static-map approach assumes a known environment and requires map maintenance after structural changes.
- OCR was tested on a small controlled label set with grayscale preprocessing only; it has no confidence gate or apartment-number validation.
- ArUco pose estimation requires a visible marker, calibrated camera geometry, and a package that matches the expected grasp setup.
- MoveIt 2 planning was sensitive to obstacle placement and collision margins.
- YOLO acts as an awareness layer and does not directly control Nav2.
- Human-detection performance was moderate on the offline test data.

## Phase 2

- Elevator-door data and entry testing were simulation-based.
- The tested entry threshold is tied to the simulated camera and doorway geometry.
- The elevator-button dataset contained class imbalance, inconsistent labels, and panel layouts that did not always match the intended deployment setting.
- Button depth was estimated under planar-panel assumptions rather than measured from a depth sensor.
- Semantic localization was trained for one building and cannot be expected to generalize to a new site without additional data.
- Single-frame place recognition was vulnerable to weak context and boundary views between hallways and elevator zones.

## Phase 3

- The grounding benchmark contains 105 images from a limited indoor environment.
- GPT-backed results may vary between calls and require a network connection and API credentials.
- Grounding outputs are 2D image boxes; the robot still needs depth, frame transformation, and physical feasibility checks before acting.
- Video tracking can drift after occlusion, rapid motion, or a substantial viewpoint change.
- The DQN policy was developed in a simplified 2D environment and has not replaced or been integrated with the production Nav2 control loop.
- Confidence, safety, and recovery modules are documented as integration components but do not yet form a complete deployed supervisor.
