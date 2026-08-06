# Failure Recovery

The integrated controller needs explicit recovery paths instead of repeatedly retrying a failed action.

Planned recovery states include reframing an unreadable label, reacquiring a grounded target, replanning around a blocked route, waiting or retreating when elevator clearance becomes invalid, relocalizing after metric and semantic disagreement, replanning a failed grasp, and stopping safely after a bounded retry budget.

Individual subsystems already expose useful recovery signals, including Nav2 action status, MoveIt 2 planning failure, grounding error fields, and tracker reacquisition state. The common ROS recovery state machine remains in progress.
