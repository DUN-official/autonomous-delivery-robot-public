# Elevator Operation

Elevator operation combines perception, guarded base motion, panel interaction, and place confirmation.

1. [Door perception](door_perception/README.md) identifies the elevator opening and estimates visible clearance.
2. [Entry and exit logic](entry_exit/README.md) requires the staging pose, sufficient clearance, and consistent opening observations before movement.
3. [Button interaction](button_interaction/README.md) selects the requested button, calculates the target position, and solves the arm motion.
4. [Semantic localization](../localization/semantic_localization/README.md) confirms the building place after the floor transition.

The current evidence demonstrates these subsystems separately. A complete elevator ride under one ROS launch sequence remains part of the unified workspace integration.

Demonstrations: [elevator entry](../../demos/elevator/elevator_entry.mp4) and [button interaction](../../demos/elevator/button_interaction.mp4).
