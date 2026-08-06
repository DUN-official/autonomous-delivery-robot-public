# Package and Human Detection

Separate YOLOv8 detectors publish package and human presence, bounding boxes, confidence, and class labels while navigation continues. Their outputs support awareness and behaviour-level decisions; they do not directly modify Nav2 costmaps or velocity commands.

At an IoU threshold of 0.50, the human detector reached F1 0.581, precision 0.654, and recall 0.522 on 1,149 images. The package detector reached F1 0.918, precision 0.933, and recall 0.903 on 16 images containing 31 package instances.

The [runtime demonstration](../../../demos/perception/package_human_detection.mp4) shows the detectors operating alongside the robot. Model retrieval and node launch files will be published together so the reported results remain tied to the correct checkpoints.
