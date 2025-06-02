from glob import glob
import shutil 
import os
import dicom2nifti
import nibabel as nib
import numpy as np


# # Convert the dicom files into nifties

import os
import SimpleITK as sitk
import numpy as np

def split_nifti(input_nifti_path, output_folder, num_slices=65):
   
    # Load the NIfTI image
    img = sitk.ReadImage(input_nifti_path)
    img_array = sitk.GetArrayFromImage(img)  # Shape: (slices, height, width)

    total_slices = img_array.shape[0]  # Total slices in the original file
    num_full_splits = total_slices // num_slices  # Only complete splits

    print(f" Processing {os.path.basename(input_nifti_path)}: {total_slices} slices → {num_full_splits} NIfTI files")

    # Get metadata
    spacing = list(img.GetSpacing())  # Voxel spacing
    direction = img.GetDirection()    # Orientation
    origin = img.GetOrigin()          # Image origin

    # Adjust Z-axis spacing
    spacing[2] *= total_slices / num_slices  # Adjust slice spacing

    # Split and save
    for i in range(num_full_splits):
        start_idx = i * num_slices
        end_idx = start_idx + num_slices
        
        sub_img_array = img_array[start_idx:end_idx]  # Get the slice range

        # Convert back to SimpleITK image
        sub_img = sitk.GetImageFromArray(sub_img_array)
        sub_img.SetSpacing(tuple(spacing))  # Preserve voxel spacing
        sub_img.SetDirection(direction)  # Preserve direction
        sub_img.SetOrigin(origin)  # Preserve origin

        # Save new NIfTI file
        output_nifti_path = os.path.join(output_folder, f"{os.path.basename(input_nifti_path).replace('.nii.gz', '')}_part_{i+1}.nii.gz")
        sitk.WriteImage(sub_img, output_nifti_path)
        print(f" Saved: {output_nifti_path} ({num_slices} slices)")

    print(f" Discarded {total_slices % num_slices} remaining slices (not enough for a full 65-slice file)")

def process_nifti_folder(input_folder, output_folder, num_slices=65):
    
    os.makedirs(output_folder, exist_ok=True)
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".nii.gz"):  # Check for NIfTI files
            input_nifti_path = os.path.join(input_folder, file_name)
            split_nifti(input_nifti_path, output_folder, num_slices)

# Set Input and Output Directories
input_nifti_folder = r"D:\VIT INTERNSHIP\LIVER\Task03_Liver\imagesTr"
output_nifti_folder = r"D:\VIT INTERNSHIP\LIVER\Task03_Liver\NF\images"

# Run the splitting process
print("\n Splitting NIfTI files into 65-slice chunks...")
process_nifti_folder(input_nifti_folder, output_nifti_folder)

print("\n All files have been processed successfully!")



import os
import SimpleITK as sitk

def split_nifti_labels(input_nifti_path, output_folder, num_slices=65):
    
    # Load the NIfTI image
    img = sitk.ReadImage(input_nifti_path)
    img_array = sitk.GetArrayFromImage(img)  # Shape: (slices, height, width)

    total_slices = img_array.shape[0]  # Total slices in the original file
    num_full_splits = total_slices // num_slices  # Only complete splits

    print(f" Processing {os.path.basename(input_nifti_path)}: {total_slices} slices → {num_full_splits} NIfTI files")

    # Get metadata
    spacing = list(img.GetSpacing())  # Voxel spacing
    direction = img.GetDirection()    # Orientation
    origin = img.GetOrigin()          # Image origin

    # Adjust Z-axis spacing
    spacing[2] *= total_slices / num_slices  # Adjust slice spacing

    # Split and save
    for i in range(num_full_splits):
        start_idx = i * num_slices
        end_idx = start_idx + num_slices
        
        sub_img_array = img_array[start_idx:end_idx]  # Get the slice range

        # Convert back to SimpleITK image
        sub_img = sitk.GetImageFromArray(sub_img_array)
        sub_img.SetSpacing(tuple(spacing))  # Preserve voxel spacing
        sub_img.SetDirection(direction)  # Preserve direction
        sub_img.SetOrigin(origin)  # Preserve origin

        # Save new NIfTI file
        output_nifti_path = os.path.join(output_folder, f"{os.path.basename(input_nifti_path).replace('.nii.gz', '')}_part_{i+1}.nii.gz")
        sitk.WriteImage(sub_img, output_nifti_path)
        print(f" Saved: {output_nifti_path} ({num_slices} slices)")

    print(f" Discarded {total_slices % num_slices} remaining slices (not enough for a full 65-slice file)")

def process_label_folder(label_folder, output_label_folder, num_slices=65):
   
    os.makedirs(output_label_folder, exist_ok=True)

    for file_name in sorted(os.listdir(label_folder)):
        if file_name.endswith(".nii.gz"):  # Check for NIfTI files
            input_nifti_path = os.path.join(label_folder, file_name)
            print(f"\n Processing label: {file_name}")
            split_nifti_labels(input_nifti_path, output_label_folder, num_slices)

# Set Input and Output Directories for Labels
input_label_folder = r"D:\VIT INTERNSHIP\LIVER\Task03_Liver\labelsTr"
output_label_folder = r"D:\VIT INTERNSHIP\LIVER\Task03_Liver\NF\labels"

# Run the splitting process for Labels Only
print("\n Splitting Label NIfTI files into 65-slice chunks...")
process_label_folder(input_label_folder, output_label_folder)

print("\n All label files have been processed successfully!")


from glob import glob
import nibabel as nib
import numpy as np
# Define the input directory
input_nifti_file_path = r'D:\VIT INTERNSHIP\LIVER\Task03_Liver\NF\labels'  

# Get a list of NIfTI files (both .nii and .nii.gz)
list_labels = glob(input_nifti_file_path + '/*.nii*')

for patient in list_labels:
    nifti_file = nib.load(patient)  # Load NIfTI file
    fdata = nifti_file.get_fdata()  # Get image data as a NumPy array
    np_unique = np.unique(fdata)  # Get unique values in the array

    if len(np_unique) == 1:  # If only one unique value exists
        print(f"File {patient} contains only one unique intensity value: {np_unique[0]}")



import os
from glob import glob
import nibabel as nib
import numpy as np

# Define directories for labels and images
label_dir = r'D:\VIT INTERNSHIP\LIVER\Task03_Liver\NF\labels'
image_dir = r'D:\VIT INTERNSHIP\LIVER\Task03_Liver\NF\images'  # Adjust this if images are stored elsewhere

# Get list of all label files
label_files = glob(os.path.join(label_dir, '*.nii.gz'))

# Loop through each label file
for label_path in label_files:
    nifti_label = nib.load(label_path)  # Load the label file
    label_data = nifti_label.get_fdata()  # Extract voxel data
    unique_values = np.unique(label_data)  # Get unique intensity values

    # If the label contains only a single intensity value (e.g., 0.0), delete both label & corresponding image
    if len(unique_values) == 1:
        print(f"Deleting label: {label_path} (contains only {unique_values[0]})")
        os.remove(label_path)  # Delete label file

        # Construct corresponding image file path
        image_filename = os.path.basename(label_path)  # Get filename
        image_path = os.path.join(image_dir, image_filename)  # Find corresponding image

        # Check if the corresponding image exists and delete it
        if os.path.exists(image_path):
            print(f"Deleting image: {image_path} (corresponding to deleted label)")
            os.remove(image_path)
        else:
            print(f"Warning: Corresponding image {image_path} not found.")

print("File cleanup completed.")



