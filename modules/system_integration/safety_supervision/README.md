# Safety Supervision

Safety checks remain separate from model confidence. A high-confidence result must still be rejected when the resulting action is physically unsafe.

The planned supervisor checks elevator and hallway clearance, person and obstacle proximity, localization and transform validity, collision-free Nav2 or MoveIt 2 plans, manipulator reach and joint limits, speed and stopping distance, and a clear fallback when an action cannot be verified.

The elevator-entry controller is an early example: door detection alone is insufficient, and movement requires staging, temporal, and clearance conditions. A common supervisor for the complete delivery system remains in progress.
