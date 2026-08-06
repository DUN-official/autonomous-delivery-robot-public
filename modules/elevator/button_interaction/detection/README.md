# Elevator-Button Detection and Selection

The detector subscribes to the panel image and requested button label. It identifies button candidates, selects the requested class, and publishes the selected image coordinate for downstream Cartesian localization.

The project used a Roboflow-derived elevator-panel dataset with augmentation. Results showed a precision-recall trade-off caused by class imbalance, inconsistent labels, and panel layouts that did not always match the intended deployment setting. The result is therefore treated as a proof of concept.

The complete perception-to-manipulation sequence is shown in the [button-interaction demo](../../../../demos/elevator/button_interaction.mp4). The cleaned ROS release will pair the node with a documented checkpoint and revised class mapping.
