# Capability Modules

This directory organizes the project by robot capability. Each module records the implemented behaviour, evaluation evidence, current limitations, and the work required before its ROS package is published in the unified workspace.

| Module | Capabilities |
|---|---|
| [Navigation](navigation/README.md) | Nav2 planning and control, AMCL integration, and learned dynamic-obstacle avoidance |
| [Localization](localization/README.md) | Metric localization through the navigation stack and ResNet18 semantic place recognition |
| [Perception](perception/README.md) | Package-label reading, package/human detection, visual grounding, and tracking |
| [Manipulation](manipulation/README.md) | ArUco package pose estimation and MoveIt 2 pick/place |
| [Elevator operation](elevator/README.md) | Door perception, guarded entry/exit, requested-button selection, and arm control |
| [System integration](system_integration/README.md) | Task coordination, uncertainty checks, safety supervision, and recovery |

Development phases are documented separately in [docs/phases](../docs/phases/).
