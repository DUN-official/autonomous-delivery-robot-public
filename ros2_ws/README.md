# Unified ROS 2 Workspace

The complete ROS 2 packages are in progress and are not included in this publication copy yet.

The working code currently spans separate development workspaces with different package names, absolute paths, launch conventions, robot descriptions, world files, checkpoint locations, and topic assumptions. Those workspaces are being reworked before publication so a fresh clone can be built and launched without reconstructing the original machines.

The planned workspace groups packages by capability:

```text
ros2_ws/src/
  delivery_bringup/             shared launch files and parameters
  delivery_description/         robot description, controllers, and transforms
  delivery_interfaces/          shared messages, services, and actions
  delivery_navigation/          maps, AMCL, Nav2 configuration, and room goals
  delivery_perception/          labels and package/human perception
  package_manipulation/         ArUco pose and MoveIt 2 pick/place
  elevator_operation/           door state, entry/exit, and button interaction
  semantic_localization/        ResNet18 place-recognition node
  grounding_bridge/             grounding-service request and target adapter
  delivery_supervisor/          task state, confidence, safety, and recovery
```

Publication criteria are:

- dependencies documented and installable with `rosdep`;
- all packages build together with `colcon build`;
- no machine-specific paths or private datasets;
- one launch entry point per demonstrated capability;
- documented topic, service, action, frame, and unit contracts;
- reproducible model, map, and world setup;
- small repeatable Gazebo verification scenarios; and
- an integrated launch path connecting perception, localization, navigation, elevator operation, manipulation, and supervision.

Until those criteria are met, implemented behaviour and evaluation evidence remain documented under [modules](../modules/README.md) and in the [demo catalogue](../demos/README.md).
