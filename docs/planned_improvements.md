# Release and Integration Roadmap

## 1. Consolidate the ROS 2 workspace

- Normalize package, node, launch, and parameter names.
- Remove machine-specific paths and duplicate workspaces.
- Document ROS 2 Humble, Gazebo, Nav2, MoveIt 2, and model dependencies.
- Add repeatable launch commands for each demonstrated subsystem.
- Add small smoke tests and sample worlds before publishing each package.

## 2. Define shared interfaces

- Create common messages for detections, semantic locations, grounded targets, confidence, and recovery state.
- Record the expected topics, services, actions, frames, and units.
- Add a task-level state machine that can coordinate pickup, navigation, elevator use, and final delivery.

## 3. Connect perception to physical targets

- Combine grounding boxes with depth and camera calibration.
- Transform targets into the robot base frame.
- Reject unreachable, low-confidence, or unsafe targets before motion planning.
- Add reacquisition after occlusion or camera motion.

## 4. Improve subsystem robustness

- Add OCR thresholding, denoising, region selection, and apartment-number validation.
- Expand human-detection data and tighten annotations.
- Rebuild the elevator-button dataset around the target panel types.
- Use short frame sequences to smooth semantic localization.
- Evaluate DQN navigation against Nav2 under the same obstacle scenarios.

## 5. Validate the integrated delivery sequence

- Run a complete simulated pickup-to-drop-off mission.
- Record success, failure, recovery, latency, and safety-gate outcomes.
- Test deliberate failure cases such as unreadable labels, blocked paths, closing elevator doors, uncertain locations, and missing targets.
- Publish the integrated launch path only after it is reproducible from a fresh clone.
