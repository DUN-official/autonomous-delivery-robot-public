# Nav2 Navigation and Metric Localization

The classical navigation path uses a pre-generated condominium occupancy grid, AMCL, LiDAR updates, and Nav2 to move between predefined room goals.

## Configuration

- Global planner: SmacPlanner2D
- Local controller: DWB
- Global pose: AMCL on the static map
- Application interface: room names translated into `NavigateToPose` goals

All tested room-to-room tasks completed in the mapped Gazebo environment. The evaluation validates the integration of the map server, transforms, AMCL, costmaps, planner, and controller under the tested conditions.

See the [navigation demo](../../../demos/navigation/nav2_room_to_room.mp4), [AMCL demo](../../../demos/localization/amcl_localization.mp4), [labelled map](../../../assets/screenshots/navigation_labelled_condo_map.png), and [RViz map view](../../../assets/screenshots/localization_amcl_rviz.png).

The ROS package is being prepared for the unified workspace with portable map and world paths, consistent launch files, and documented navigation parameters.
