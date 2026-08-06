# ArUco Package Pose Estimation

An ArUco marker attached to the package provides a stable 6-DoF pose estimate relative to the camera. A grasp pose is derived from the marker frame and passed to the manipulation pipeline.

This approach kept the simulation deterministic and computationally light. It assumes the marker is visible, the camera is calibrated, and the package geometry matches the configured grasp offset.

The pose-estimation node and calibration files are being normalized for the unified ROS 2 workspace. The connected result is shown in the [package pick/place demo](../../../../demos/manipulation/package_pick_and_place.mp4).
