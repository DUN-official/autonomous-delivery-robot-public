# Elevator-Door Perception

A YOLOv8n detector identifies the elevator opening and measures its visible width in the Gazebo camera stream. The trained model reached approximately 0.98 mAP50-95 on the simulated elevator dataset.

The detector supplies evidence to the entry controller but does not command motion by itself. This separation prevents one detection from directly authorizing an unsafe entry.

The [elevator-entry demonstration](../../../demos/elevator/elevator_entry.mp4) shows the detector in its simulated operating environment. The public ROS package will include checkpoint retrieval and explicit camera and threshold configuration.
