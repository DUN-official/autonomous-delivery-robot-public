# Notebooks

Project notebooks are stored beside the capability that uses them. This directory provides a central index.

## Semantic localization

The complete executed Colab workflow is published under the [semantic-localization module](../modules/localization/semantic_localization/README.md#notebook-workflow):

1. [Video frame extraction](../modules/localization/semantic_localization/notebooks/01_video_frame_extractor.ipynb)
2. [Training and validation split](../modules/localization/semantic_localization/notebooks/02_train_val_splitter.ipynb)
3. [Test-video frame extraction](../modules/localization/semantic_localization/notebooks/03_test_video_frame_extractor.ipynb)
4. [Test-set preparation](../modules/localization/semantic_localization/notebooks/04_test_splitter.ipynb)
5. [ResNet18 training and testing](../modules/localization/semantic_localization/notebooks/05_resnet18_train_test.ipynb)
6. [Semantic-localization demonstration](../modules/localization/semantic_localization/notebooks/06_semantic_localisation_demo.ipynb)

## Visual grounding

The cleaned visual-grounding notebooks are published under the [visual-grounding module](../modules/perception/visual_grounding/README.md):

1. [Frame extraction](../modules/perception/visual_grounding/notebooks/01_frame_extraction_colab.ipynb)
2. [Ground-truth coordinate generation](../modules/perception/visual_grounding/notebooks/02_ground_truth_coordinate_generator_colab.ipynb)
3. [Baseline method evaluation](../modules/perception/visual_grounding/notebooks/03_baseline_models_colab.ipynb)
4. [GPT-guided OWL-ViT](../modules/perception/visual_grounding/notebooks/04_gpt_guided_owlvit_colab.ipynb)
5. [Four-method comparison](../modules/perception/visual_grounding/notebooks/05_compare_all_models_colab.ipynb)

The semantic-localization notebooks preserve the original executed workflow and Google Drive paths. The visual-grounding notebooks are cleaned publication copies aligned with the runnable module.
