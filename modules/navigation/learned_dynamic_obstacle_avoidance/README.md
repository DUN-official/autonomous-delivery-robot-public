# Learned Dynamic-Obstacle Avoidance

The learned-navigation prototype uses a Deep Q-Network in a Pygame/Gymnasium environment to choose motion around static and moving obstacles.

The observation combines 24 LiDAR distances with a relative goal vector. Training uses a replay buffer of 1,000 transitions, a target network updated every 1,000 steps, and epsilon-greedy exploration decaying from 1.0 to 0.05. Rewards combine progress, a +200 goal reward, a -200 collision penalty, and a -0.1 step cost.

The [moving-obstacle demonstration](../../../demos/navigation/RL_moving_obs_20_trimmed.mov) and [stationary-obstacle demonstration](../../../demos/navigation/RL_stationary_obs_trimmed.mov) show the current policy in simulation. A quantitative comparison with Nav2, ROS 2 integration, and transfer from the simplified environment remain in progress.
