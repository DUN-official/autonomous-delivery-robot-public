# Problem Statement

Package delivery inside high-density residential buildings creates a second logistics problem after a courier reaches the building. Parcels accumulate in lobbies and storage rooms, staff must record and organize arrivals, residents may experience delays, and misplaced packages become difficult to trace.

This project investigates an autonomous internal courier that can:

- identify a package and read its destination label;
- estimate the package pose and pick it up;
- localize and navigate through known indoor spaces;
- detect people and packages while moving;
- enter an elevator and operate its controls;
- confirm its semantic location after changing floors;
- resolve a final target from a natural-language description; and
- stop, wait, or recover when the requested action is uncertain or unsafe.

The current prototype is evaluated through simulation and recorded indoor imagery. It assumes flat accessible paths, visible labels, designated pickup areas, functioning elevators, and packages that fit within the robot gripper.
