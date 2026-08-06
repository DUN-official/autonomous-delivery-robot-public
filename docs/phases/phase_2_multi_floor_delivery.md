# Phase 2: Multi-Floor Delivery

## Objective

Extend the single-floor robot with the perception, motion logic, manipulation, and place awareness needed to move between floors.

## Elevator entry and exit

A YOLOv8n detector identifies the elevator opening in Gazebo. Movement is enabled only when the robot is at its staging pose, the opening exceeds the 165-pixel clearance threshold, and consecutive observations show the door opening rather than closing. The tested sequences achieved 100% trigger success with no false movement triggers.

## Elevator-button interaction

The button workflow separates image publication, requested-button selection, detection, coordinate calculation, inverse kinematics, and joint-state publication into individual ROS nodes. The demonstration connects a requested button to a visualized arm motion. Dataset imbalance and inconsistent labels remain limitations of the detector.

## Semantic localization

ResNet18 was fine-tuned as a nine-class place classifier using indoor footage. The classes cover hallways, elevator landmarks, a lobby, a laundry area, and a lounge. The processed dataset contains 7,331 images across training, validation, and test splits. Test accuracy reached 77.8%, with the main errors occurring between visually similar hallway and elevator-adjacent scenes.

## Published material

- [Elevator demonstrations](../../demos/README.md#manipulation-and-elevator-operation)
- [Semantic-localization demonstration](../../demos/localization/semantic_localization.mp4)
- [Detailed metrics](../results_and_metrics.md#phase-2)
- [Phase 2 limitations](../limitations.md#phase-2)
- [Elevator module](../../modules/elevator/README.md)

These results demonstrate the required subsystems but do not yet represent a continuous elevator ride controlled by one integrated launch sequence.
