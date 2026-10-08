# Mimi's Garden baseline model

Architecture: EfficientNet-B0, initialized with ImageNet-1K V1 weights.
Version: plant_model_v1. Selected checkpoint: epoch 3.
Checkpoint SHA-256: `6af9df60b7da07e1147705839075d449e64209f1f6e7586d9b2183dfcb2e4578`.

## Intended use

Classify clear leaf photos into `healthy`, `leaf_spots`, or `severe_damage`. This predicts broad visible conditions and does not identify a specific disease or establish its cause. The web app flags low-confidence predictions for review. It cannot reliably reject all non-plant or out-of-distribution images.

## Training and data

Three total epochs: one classifier-only warmup and two epochs of full fine-tuning. AdamW, cross-entropy, batch size 32, head learning rate 0.0005, backbone learning rate 0.00005, seed 42. Trained on Apple MPS. The seed does not guarantee bitwise reproducibility across hardware.

The existing prepared dataset supplied 80,665 images. Hash-based manifests retained 64,516 training, 8,060 validation, and 8,063 test images. Six duplicate groups crossed the original train/validation split and were excluded from validation/test. Other exact duplicate copies were also excluded. Source files were not modified.

The original validation pool was partitioned by hash within each class. The test subset was not used for checkpoint selection. Class mappings come from the repository's existing preparation script. Raw source disease labels are grouped into broad conditions and have not been independently verified as visual-condition annotations.

## Measured results

Best validation accuracy: 98.7221%; weighted F1: 0.9872.
Held-out accuracy: 98.9334%; weighted F1: 0.9893; macro F1: 0.9888.

| Class | Precision | Recall | F1 | Test images |
|---|---:|---:|---:|---:|
| healthy | 0.9911 | 0.9996 | 0.9954 | 2784 |
| leaf_spots | 0.9770 | 0.9886 | 0.9828 | 2022 |
| severe_damage | 0.9956 | 0.9810 | 0.9882 | 3257 |

## Limitations and release requirements

These scores are from the same source dataset, not an independent real-world evaluation. Exact hash checks do not detect near-duplicates or different augmented views of the same leaf. Plant identity and source-image grouping are not available in the current prepared folders. Lighting, backgrounds, plant species, and image capture conditions may differ substantially in use.

Confidence scores are uncalibrated softmax outputs. Existing review thresholds (0.5 and 0.7) were retained rather than tuned on the test set. Before making broad performance claims, evaluate separately collected garden photos with independently checked labels and plant-level grouping.

The checkpoint includes optimizer state and is a training artifact; the service reconstructs the architecture, validates the label contract, and loads only its model weights. Restart the service after replacing it. Do not silently relabel or replace a deployed model without updating its version and records.
