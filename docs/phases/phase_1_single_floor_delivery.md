# Phase 1: Single-Floor Delivery

## Objective

Build a simulation-based residential delivery robot that can identify a package destination, pick up the package, navigate through a known condominium floor, and monitor people and packages during operation.

## Capability set

- ROS 2 Humble, Gazebo, TurtleBot3, and OpenManipulator
- static occupancy grid, AMCL, Nav2, SmacPlanner2D, and DWB
- OpenCV and Tesseract package-label reading
- ArUco 6-DoF package pose estimation
- MoveIt 2 grasp planning and pick/place execution
- YOLOv8 package and human detection

## Delivery sequence

1. Move to the designated pickup area.
2. Detect the package and read its apartment label.
3. Estimate the package pose from its ArUco marker.
4. Plan and execute the grasp with MoveIt 2.
5. Convert the apartment identifier into a predefined room goal.
6. Navigate with Nav2 while AMCL maintains the global pose.
7. Monitor people and packages through a separate perception node.
8. Place the package and return to the pickup area.

## Evaluation summary

All tested room-to-room goals completed in the mapped Gazebo environment. The package detector reached F1 0.918 on its offline test set, while the human detector reached F1 0.581. Label reading and manipulation were evaluated qualitatively through successful demonstrations and recorded failure cases.

## Published material

- [Demonstration catalogue](../../demos/README.md)
- [Detailed metrics](../results_and_metrics.md#phase-1)
- [Phase 1 limitations](../limitations.md#phase-1)
- [Capability modules](../../modules/README.md)

The complete ROS packages remain part of the unified-workspace release described in [ros2_ws/README.md](../../ros2_ws/README.md).
