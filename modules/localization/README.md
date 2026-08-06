# Localization

The project uses complementary metric and semantic localization.

- Metric localization is part of the [Nav2 module](../navigation/nav2/README.md), where AMCL estimates the robot pose on a static occupancy grid.
- [Semantic localization](semantic_localization/README.md) classifies the visible indoor place and supplies a building-level context cue after elevator travel.

Semantic predictions do not replace the metric pose. The planned coordinator will compare both signals, smooth semantic predictions across short sequences, and stop for relocalization when the cues disagree.
