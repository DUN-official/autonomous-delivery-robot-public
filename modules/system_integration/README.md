# System Integration

System integration connects independently demonstrated capabilities without allowing an uncertain perception result or an unsafe target to become an automatic action.

The planned coordinator will manage the delivery sequence, consume structured subsystem status, and route execution through:

- [uncertainty gating](uncertainty_gating/README.md) for confidence, temporal agreement, target stability, and coordinate validity;
- [safety supervision](safety_supervision/README.md) for clearance, localization, collision, reachability, speed, and stop conditions; and
- [failure recovery](failure_recovery/README.md) for bounded retries, reacquisition, replanning, retreat, relocalization, and safe task termination.

The elevator-entry trigger is an existing example of the intended pattern: perception supplies evidence, but movement is authorized only after staging, temporal, and clearance conditions pass.

The common ROS messages, state machine, and end-to-end launch sequence remain in progress and will be published with the [unified workspace](../../ros2_ws/README.md).
