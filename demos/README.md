# Demonstrations

The public videos are organized by capability. Phase labels are included only to show when each subsystem entered the project.

## Navigation

| Demonstration | Phase | What it shows |
|---|---:|---|
| [Nav2 room-to-room navigation](navigation/nav2_room_to_room.mp4) | 1 | Path planning and execution on the mapped condominium floor |
| [AMCL localization](localization/amcl_localization.mp4) | 1 | Pose tracking against the static occupancy grid in RViz |
| [Learned avoidance with moving obstacles](navigation/RL_moving_obs_20_trimmed.mov) | 3 | DQN motion decisions around moving obstacles |
| [Learned avoidance with stationary obstacles](navigation/RL_stationary_obs_trimmed.mov) | 3 | DQN motion decisions around stationary obstacles |

## Perception and localization

| Demonstration | Phase | What it shows |
|---|---:|---|
| [Package-label reading](perception/label_reading.mp4) | 1 | Camera input, grayscale preprocessing, and Tesseract destination extraction |
| [Package and human detection](perception/package_human_detection.mp4) | 1 | Parallel detections during robot operation |
| [Semantic localization](localization/semantic_localisation.mp4) | 2 | ResNet18 predictions across indoor building locations |

## Manipulation and elevator operation

| Demonstration | Phase | What it shows |
|---|---:|---|
| [Package pick/place](manipulation/package_pick_and_place.mp4) | 1 | ArUco pose estimation and MoveIt 2 manipulation with an obstacle in the planning scene |
| [Elevator entry](elevator/elevator_entry.mp4) | 2 | Door-state detection and the guarded entry trigger in Gazebo |
| [Elevator-button interaction](elevator/button_interaction.mp4) | 2 | Requested-button selection, target coordinates, inverse kinematics, and RViz arm motion |

## Visual grounding and tracking

| Demonstration | Mode | Instruction |
|---|---|---|
| [Toy car beside a water bottle](visual_grounding/recorded_toy_car_tracking.mp4) | Recorded video | `track the toy car beside green water bottle` |
| [Robot cube](visual_grounding/live_robot_cube_tracking.mp4) | Live camera | `look for the robot cube` |
| [Package on the floor](visual_grounding/package_on_floor.mp4) | Recorded video | `find the package on the floor` |
| [Door at the end of a hallway](visual_grounding/hallway_door.mp4) | Recorded video | `go to the door at the end of the hallway` |
| [Grey door](visual_grounding/grey_door.mp4) | Recorded video | `look for the grey door` |
| [Package hidden behind a chair](visual_grounding/hidden_package.mp4) | Recorded video | `find the package hidden behind the chair` |

The visual-grounding clips show target acquisition, tracking, and status reporting through the local interface. They demonstrate the perception service rather than a complete robot navigation run.

Long raw captures, duplicate recordings, training footage, and private runtime uploads are excluded. The published clips are compressed for browser playback while retaining the interface and tracked target.
