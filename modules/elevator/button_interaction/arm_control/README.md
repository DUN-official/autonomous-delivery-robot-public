# Elevator-Button Arm Control

The manipulation chain converts the selected image coordinate into a Cartesian target relative to the camera, solves the arm joint angles, and publishes the result for visualization or execution.

The implementation assumes a planar button panel with known physical dimensions and camera geometry. The [button-interaction demo](../../../../demos/elevator/button_interaction.mp4) shows the complete node chain in RViz. Depth sensing and contact feedback remain necessary for reliable physical operation.
