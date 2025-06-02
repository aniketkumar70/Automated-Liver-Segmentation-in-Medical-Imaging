import os
from glob import glob
import nibabel as nib
from monai.transforms import (
    Compose,
    EnsureChannelFirstD,
    LoadImaged,
    Resized,
    ToTensord,
    Spacingd,
    Orientationd,
    ScaleIntensityRanged,
    CropForegroundd,
)
from monai.data import DataLoader, Dataset, CacheDataset
from monai.utils import set_determinism


def prepare(in_dir, pixdim=(1.5, 1.5, 1.0), a_min=-200, a_max=200, spatial_size=[128, 128, 64], cache=True, cache_rate=1.0):
  

    set_determinism(seed=0)

    # Define paths
    path_train_volumes = sorted(glob(os.path.join(in_dir, "trainvolume", "*.nii.gz")))
    path_train_segmentation = sorted(glob(os.path.join(in_dir, "trainsegmentation", "*.nii.gz")))

    path_test_volumes = sorted(glob(os.path.join(in_dir, "testvolume", "*.nii.gz")))
    path_test_segmentation = sorted(glob(os.path.join(in_dir, "testsegmentation", "*.nii.gz")))

    # Error handling: Ensure all folders have files
    if not path_train_volumes or not path_train_segmentation:
        raise FileNotFoundError("Error: Train volume or segmentation files not found.")

    if not path_test_volumes or not path_test_segmentation:
        raise FileNotFoundError("Error: Test volume or segmentation files not found.")

    # Create dataset dictionaries
    train_files = [{"vol": vol, "seg": seg} for vol, seg in zip(path_train_volumes, path_train_segmentation)]
    test_files = [{"vol": vol, "seg": seg} for vol, seg in zip(path_test_volumes, path_test_segmentation)]

    # Define transformations
    transforms = Compose([
        LoadImaged(keys=["vol", "seg"]),
        EnsureChannelFirstD(keys=["vol", "seg"]),
        Spacingd(keys=["vol", "seg"], pixdim=pixdim, mode=("bilinear", "nearest")),
        Orientationd(keys=["vol", "seg"], axcodes="RAS"),
        ScaleIntensityRanged(keys=["vol"], a_min=a_min, a_max=a_max, b_min=0.0, b_max=1.0, clip=True),
        CropForegroundd(keys=["vol", "seg"], source_key="vol"),
        Resized(keys=["vol", "seg"], spatial_size=spatial_size),
        ToTensord(keys=["vol", "seg"]),
    ])

    # Dataset and DataLoader
    if cache:
        train_ds = CacheDataset(data=train_files, transform=transforms, cache_rate=cache_rate)
        test_ds = CacheDataset(data=test_files, transform=transforms, cache_rate=cache_rate)
    else:
        train_ds = Dataset(data=train_files, transform=transforms)
        test_ds = Dataset(data=test_files, transform=transforms)

    train_loader = DataLoader(train_ds, batch_size=1, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=1)

    # Log dataset sizes
    print(f" Train Volumes: {len(train_files)} | Train Segmentations: {len(train_files)}")
    print(f" Test Volumes: {len(test_files)} | Test Segmentations: {len(test_files)}")

    return train_loader, test_loader
