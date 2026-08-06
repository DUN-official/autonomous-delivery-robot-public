# Perception

The perception layer supplies task and scene information without directly commanding robot motion.

- [Package-label reading](label_recognition/README.md) extracts the apartment identifier from a camera frame.
- [Package and human detection](package_human_detection/README.md) provides class, confidence, and bounding-box awareness during operation.
- [Visual grounding and tracking](visual_grounding/README.md) selects an image target from a language instruction and can maintain that target through video frames.
- Elevator-specific door and button perception is grouped under the [elevator module](../elevator/README.md) because it is coupled to the elevator state machine.

The shared ROS interface will standardize timestamps, camera-frame identifiers, confidence fields, normalized image coordinates, and failure status across these outputs.
