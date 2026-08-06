# Elevator Entry and Exit Logic

The entry controller requires several conditions before it sends a movement command:

1. the robot is confirmed at the elevator staging pose;
2. the detected opening exceeds the 165-pixel clearance threshold;
3. consecutive frames confirm the doorway is opening rather than closing; and
4. the clearance remains valid long enough to authorize entry.

The tested Gazebo sequences produced 100% trigger success with no false movement triggers. The result applies to the simulated camera and elevator geometry; real deployment would require metric clearance, depth sensing, obstruction monitoring, and corresponding exit checks.

See the [elevator-entry demonstration](../../../demos/elevator/elevator_entry.mp4).
