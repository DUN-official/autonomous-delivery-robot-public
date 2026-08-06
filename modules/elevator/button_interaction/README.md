# Elevator-Button Interaction

The elevator-button capability connects a requested button label to arm motion.

```text
panel image + requested button
        -> button detection and selection
        -> image coordinate
        -> Cartesian target
        -> inverse-kinematics solution
        -> joint-state publication
        -> RViz or robot arm
```

The [detection stage](detection/README.md) selects the requested class from the panel image. The [arm-control stage](arm_control/README.md) converts that selection into a target and joint solution.

The [demonstration](../../../demos/elevator/button_interaction.mp4) shows the full proof-of-concept chain. Reliable physical operation still requires depth sensing, panel calibration, contact feedback, and stronger button-class data.
