# Package Pick/Place

Package manipulation is one connected capability with two stages:

1. [ArUco pose estimation](pose_estimation/README.md) calculates a stable 6-DoF package pose relative to the camera and applies the configured grasp offset.
2. [MoveIt 2 motion planning](motion_planning/README.md) performs inverse kinematics, collision checking, trajectory planning, grasp transfer, and release.

Successful Gazebo trials completed marker detection, collision-free planning, grasping, transfer, and placement. Recorded failures exposed sensitivity to planning-scene geometry, obstacle placement, and collision margins.

The [package pick/place demonstration](../../../demos/manipulation/package_pick_and_place.mp4) shows a successful run with an obstacle in the planning scene. The public ROS package will include the robot description, camera calibration, planning-scene configuration, controller mapping, and launch files required to reproduce the complete chain.
