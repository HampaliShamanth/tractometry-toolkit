import os
import numpy as np
import nibabel as nib
from scipy.ndimage import binary_erosion


def voxelise_tractogram(tract_path, reference_image):
    """
    Voxelize the tractogram and calculate the number of non-zero voxels.

    Parameters:
        tract_path (str): Path to the tractography file.
        reference_image (str): Path to the reference image file.

    Returns:
        voxel_count (int): Number of non-zero voxels.
        voxels_data (ndarray): Voxel data of the tractogram.
    """
    # Generate voxel data using an external command (tckmap)
    os.system(f"tckmap -template {reference_image} {tract_path} voxels.nii.gz")

    # Load the generated voxel data
    voxels_img = nib.load("voxels.nii.gz")
    voxels_data = voxels_img.get_fdata()

    # Count the number of non-zero voxels
    voxel_count = np.count_nonzero(voxels_data)

    # Remove the temporary voxel file
    os.remove("voxels.nii.gz")

    return voxel_count, voxels_data


def calculate_surface_volume(N, voxel_volume):
    """
    Calculate the surface volume of the tractogram.

    Parameters:
        N (int): Number of non-zero voxels.
        voxel_volume (float): Volume of a single voxel.

    Returns:
        surface_volume (float): Surface volume of the tractogram.
    """
    return N * voxel_volume


def calculate_surface_area(voxels_data, voxel_spacing):
    """
    Calculate the surface area of the tractogram.

    Parameters:
        voxels_data (ndarray): Voxel data of the tractogram.
        voxel_spacing (tuple): Spacing of the voxels in x, y, and z directions.

    Returns:
        surface_area (float): Surface area of the tractogram.
    """
    # Create a binary mask of the voxels
    voxels_binary = voxels_data > 0

    # Perform binary erosion to find surface voxels
    surface_voxels = voxels_binary & ~binary_erosion(voxels_binary)

    # Count the number of surface voxels
    surface_voxel_count = np.count_nonzero(surface_voxels)

    # Calculate the squared voxel spacing
    voxel_spacing_sq = np.sqrt(np.dot(voxel_spacing, voxel_spacing))

    # Calculate the surface area
    return surface_voxel_count * voxel_spacing_sq ** 2


def calculate_end_surface_area(surface_voxels, voxel_spacing):
    """
    Calculate the surface area of the end points.

    Parameters:
        surface_voxels (int): Number of surface voxels.
        voxel_spacing (tuple): Spacing of the voxels in x, y, and z directions.

    Returns:
        surface_area (float): Surface area of the end points.
    """
    return surface_voxels * (voxel_spacing[0] * voxel_spacing[1])


def calculate_radius(area):
    """
    Calculate the radius from the given area.

    Parameters:
        area (float): Area value.

    Returns:
        radius (float): Calculated radius.
    """
    return np.sqrt(area / np.pi)


def calculate_irregularity(area, radius):
    """
    Calculate the irregularity based on the area and radius.

    Parameters:
        area (float): Area value.
        radius (float): Radius value.

    Returns:
        irregularity (float): Calculated irregularity.
    """
    return (np.pi * radius * radius) / area
