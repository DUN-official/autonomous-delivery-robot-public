# Project Summary

The autonomous delivery robot combines perception, localization, navigation, manipulation, elevator operation, and system-level supervision for indoor residential package delivery.

## Current capability set

The single-floor foundation uses ROS 2 Humble, Gazebo, TurtleBot3, a static occupancy grid, AMCL, and Nav2. Package handling combines label reading, ArUco pose estimation, and MoveIt 2 pick/place. Separate YOLOv8 detectors provide package and human awareness during robot operation.

Multi-floor work adds elevator-opening detection, guarded entry logic, requested-button selection, target-coordinate calculation, arm inverse kinematics, and a nine-class ResNet18 semantic place classifier.

Context-aware work adds a DQN obstacle-avoidance prototype and a visual-grounding service that converts language instructions into image targets. The grounding module supports still images, uploaded videos, live-camera acquisition, target tracking, four selectable methods, and a saved 105-image benchmark.

## Integration status

Subsystem behaviour and evaluation evidence are published, but the complete ROS source is still being consolidated. The remaining project-level task is to connect the demonstrated capabilities through stable ROS interfaces and validate a continuous multi-floor delivery sequence from a fresh clone.

The original development sequence is documented in [docs/phases](phases/). The capability implementation map is maintained in [modules](../modules/README.md).
