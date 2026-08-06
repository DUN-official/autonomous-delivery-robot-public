# MoveIt 2 Pick/Place Planning

The motion-planning stage converts the ArUco-derived package pose into an end-effector goal for the OpenManipulator arm. MoveIt 2 performs inverse kinematics, collision checking, joint-space planning, trajectory execution, and package placement.

Successful Gazebo trials completed collision-free planning, grasping, transfer, and release. Other trials exposed sampling sensitivity and occasional obstacle collisions; replanning recovered from some planning failures.

The [published demo](../../../../demos/manipulation/package_pick_and_place.mp4) shows a successful run with an obstacle in the planning scene. The ROS package will be added after robot-description references, controller names, planning-scene configuration, and launch files are made portable.
