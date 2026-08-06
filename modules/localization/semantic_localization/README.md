# Semantic Localization

This module classifies the current indoor scene as one of nine semantic building locations. It provides a place-confirmation cue after elevator travel and complements metric localization rather than replacing it.

The original executed Google Colab workflow is published here as proof of the completed development and evaluation work. The notebooks cover the complete sequence from raw-video frame extraction through dataset preparation, model training, independent testing, and video demonstration. The ROS 2 runtime version is still being reorganized for the unified workspace.

## Notebook workflow

Run the notebooks in order:

| Step | Notebook | Purpose | Recorded output |
|---:|---|---|---|
| 1 | [Video frame extraction](notebooks/01_video_frame_extractor.ipynb) | Extract frames from the training and validation source videos at fixed time intervals. | 6,723 images |
| 2 | [Training and validation split](notebooks/02_train_val_splitter.ipynb) | Divide the extracted images into class-organized training and validation folders using an 80/20 split. | 5,383 training and 1,340 validation images |
| 3 | [Test-video frame extraction](notebooks/03_test_video_frame_extractor.ipynb) | Extract frames from a separately recorded set of test videos. | 875 candidate test images |
| 4 | [Test-set preparation](notebooks/04_test_splitter.ipynb) | Select and copy the independent test images into the processed dataset. | 608 test images |
| 5 | [ResNet18 training and testing](notebooks/05_resnet18_train_test.ipynb) | Fine-tune ResNet18, save the best and final checkpoints, evaluate validation and test performance, and export plots and prediction files. | 97.24% best validation accuracy and 77.8% test accuracy |
| 6 | [Semantic-localization demonstration](notebooks/06_semantic_localisation_demo.ipynb) | Load the best checkpoint, classify a compiled demonstration video, apply short-window prediction smoothing, and export an annotated video with CSV and JSON summaries. | 68.86% frame accuracy on the compiled demonstration |

The notebooks retain their executed outputs and original Colab paths so the recorded workflow and results remain visible.

## Required data layout

The notebooks use this Google Drive root:

```text
/content/drive/MyDrive/UofT (Google Drive)/MIE1076/AI_Localisation/residence_localization/
```

The starting inputs are the class-organized `raw_videos/` and `raw_videos_test/` folders. The final demonstration also requires `demo/mie1076_ai_localisation_video_comp.mp4`. The workflow creates the extracted-frame folders, processed dataset, experiment outputs, and model checkpoints.

```text
residence_localization/
  raw_videos/<class>/
  raw_videos_test/<class>/
  extracted_frames/<class>/
  extracted_frames_test/<class>/
  processed_images/
    train/<class>/
    val/<class>/
    test/<class>/
  experiments/resnet18_baseline/
    checkpoints/
    outputs/
  demo/mie1076_ai_localisation_video_comp.mp4
```

Raw videos, extracted frames, and generated checkpoints are not committed to this repository. They are development data and generated artifacts, while the executed notebooks and public demonstration preserve the workflow and results.

## Location classes

The nine classes are:

- `floor1_hallway`
- `floor2_hallway`
- `floor3_hallway`
- `front_lobby`
- `laundry`
- `ccu_lounge`
- `floor1_elevator_landmark`
- `floor2_elevator_landmark`
- `floor3_elevator_landmark`

The logical floor labels were used to keep the class names portable: floor 1 corresponds to the building's first floor, floor 2 to the sixth floor, and floor 3 to the ninth floor.

## Results and publication status

The processed dataset contains 7,331 images: 5,383 training, 1,340 validation, and 608 independent test images. ResNet18 was fine-tuned end to end with ImageNet initialization and reached 77.8% test accuracy.

Performance was strongest for visually distinctive areas and weakest where hallways and elevator landmarks shared similar structure. Sequence smoothing, stricter boundary labels, and more floor-specific footage remain planned improvements.

See the [semantic-localization demonstration](../../../demos/localization/semantic_localisation.mp4) and the broader [results summary](../../../docs/results_and_metrics.md#semantic-localization).

The notebooks are the published development workflow, not the final robot runtime. The ROS 2 package still needs the trained inference code to be separated into a node, connected to the camera and task coordinator, given portable configuration and model paths, and tested inside the unified workspace.
