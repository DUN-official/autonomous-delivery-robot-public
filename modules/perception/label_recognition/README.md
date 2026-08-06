# Package-Label Recognition

This module extracts the destination apartment from a package label before task-level navigation begins.

## Current design

- Input: RGB frames from `/pi_camera/image_raw`
- Preprocessing: full-frame grayscale conversion with OpenCV
- Recognition: Tesseract OCR
- Output: apartment identifier published on `/apt_no`

The simulation test used a visible `Apt 4B` label. It showed that OCR can provide a semantic destination to the delivery coordinator, but also exposed occasional confusion between `B` and `8`.

The behaviour is shown in the [package-label demo](../../../demos/perception/label_reading.mp4). The ROS node will be added after preprocessing, confidence handling, and apartment-number validation are made reproducible.
