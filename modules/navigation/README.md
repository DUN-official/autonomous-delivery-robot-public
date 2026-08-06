# Navigation

The project contains two navigation paths with different maturity levels.

- [Nav2 navigation](nav2/README.md) is the demonstrated ROS 2 path for mapped indoor environments. It combines a static occupancy grid, AMCL, SmacPlanner2D, DWB, costmaps, and `NavigateToPose` goals.
- [Learned dynamic-obstacle avoidance](learned_dynamic_obstacle_avoidance/README.md) is a DQN prototype developed in a simplified 2D environment with LiDAR-style observations and moving obstacles.

The Nav2 stack remains the reference control path. Before the learned policy can become a selectable controller, both approaches need a matched scenario set, common metrics, and a ROS command interface with the same stopping and safety constraints.

Demonstrations: [Nav2 room-to-room navigation](../../demos/navigation/nav2_room_to_room.mp4), [AMCL localization](../../demos/localization/amcl_localization.mp4), [learned avoidance with moving obstacles](../../demos/navigation/RL_moving_obs_20_trimmed.mov), and [learned avoidance with stationary obstacles](../../demos/navigation/RL_stationary_obs_trimmed.mov).
