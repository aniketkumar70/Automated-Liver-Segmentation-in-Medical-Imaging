# Automated Liver Segmentation in Medical Imaging

This project implements a deep learning-based pipeline for automated liver segmentation from medical imaging scans such as CT and MRI. It utilizes the 3D U-Net architecture with PyTorch and MONAI frameworks to deliver accurate and efficient segmentation, helping streamline clinical workflows and enhance diagnostic accuracy.

## 🚀 Features

- **3D U-Net Architecture:** Designed for volumetric medical image segmentation.
- **Frameworks Used:** PyTorch and MONAI.
- **Preprocessing:** Standardization, normalization, cropping, and augmentation of volumetric CT/MRI scans.
- **Data Formats:** Supports DICOM and NIfTI.
- **Evaluation Metrics:** Dice Similarity Coefficient (DSC) for performance assessment.
- **Visualization:** Outputs can be visualized using tools like 3D Slicer.

## 🧠 Technologies

- Python 3.x  
- PyTorch  
- MONAI  
- NumPy  
- nibabel  
- 3D Slicer (for visualization)


## 📊 Methodology

1. **Data Acquisition & Preparation**
   - Conversion from DICOM to NIfTI format
   - Resampling to standard voxel spacing
   - Intensity normalization and clipping
   - Slicing volumes into uniform chunks (65 slices each)

2. **Model Design**
   - 3D U-Net with skip connections
   - Loss functions: Dice Loss and Weighted Cross-Entropy
   - Optimizer: Adam (learning rate = 1e-5)

3. **Training & Evaluation**
   - Training over 100 epochs with batch size 16
   - Evaluated using Dice Coefficient
   - Final model preserved based on best validation score

## 📈 Results

| Metric            | Training | Testing |
|------------------|----------|---------|
| Dice Coefficient | 0.90     | 0.85    |
| Dice Loss        | 0.09     | 0.32    |

> Achieved **95.94% accuracy** in liver segmentation using volumetric CT scans.

## 🔍 Future Work

- Integration of larger and more diverse datasets
- Hyperparameter tuning via automated search
- Adoption of advanced architectures (e.g., Attention U-Net, Swin-UNETR)
- Real-time inference pipeline with PACS/HIS integration
- Extension to multi-organ segmentation

## 📌 Citation


## 📬 Contact

For any questions or collaboration ideas, feel free to reach out via GitHub.

