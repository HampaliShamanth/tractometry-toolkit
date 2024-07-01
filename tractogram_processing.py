import nibabel as nib
from dipy.io.streamline import load_tractogram
from dipy.tracking.streamline import Streamlines
from sklearn.cluster import KMeans
import numpy as np

def load_tractogram_file(tract_path, reference_image):
    """
    Load the tractogram file.

    Parameters:
        tract_path (str): Path to the tractography file.
        reference_image (str): Path to the reference image file.

    Returns:
        tractogram: Loaded tractogram.
    """
    tractogram = load_tractogram(tract_path, reference_image)
    return tractogram

def calculate_voxel_spacing(reference_image):
    """
    Calculate the voxel spacing of the reference image.

    Parameters:
        reference_image (str): Path to the reference image file.

    Returns:
        voxel_spacing (tuple): Spacing of the voxels in x, y, and z directions.
    """
    img = nib.load(reference_image)
    voxel_spacing = img.header.get_zooms()[:3]
    return voxel_spacing

def determine_surface_end(E1, E2):
    """
    Determine the surface end points of the tractogram.

    Parameters:
        E1 (ndarray): First set of endpoints.
        E2 (ndarray): Second set of endpoints.

    Returns:
        E1 (ndarray): First set of endpoints.
        E2 (ndarray): Second set of endpoints.
    """
    E1_mean = np.mean(E1, axis=0)
    E2_mean = np.mean(E2, axis=0)
    largest_diff_dim = np.argmax(np.abs(E1_mean - E2_mean))
    if E1_mean[largest_diff_dim] > E2_mean[largest_diff_dim]:
        return E1, E2
    else:
        return E2, E1

def cluster_endpoints(streamlines):
    """
    Cluster the endpoints of the streamlines into two groups.

    Parameters:
        streamlines (Streamlines): Streamlines of the tract.

    Returns:
        E1 (ndarray): First set of endpoints.
        E2 (ndarray): Second set of endpoints.
    """
    endpoints = np.vstack([s[0] for s in streamlines] + [s[-1] for s in streamlines])
    kmeans = KMeans(n_clusters=2).fit(endpoints)
    labels = kmeans.labels_
    E1 = endpoints[labels == 0]
    E2 = endpoints[labels == 1]
    return E1, E2

def preprocess_tractogram(tract_path, reference_image):
    """
    Preprocess the tractogram file by loading it and calculating necessary parameters.

    Parameters:
        tract_path (str): Path to the tractography file.
        reference_image (str): Path to the reference image file.

    Returns:
        tractogram: Loaded tractogram.
        voxel_spacing (tuple): Spacing of the voxels in x, y, and z directions.
        E1 (ndarray): First set of endpoints.
        E2 (ndarray): Second set of endpoints.
    """
    tractogram = load_tractogram_file(tract_path, reference_image)
    voxel_spacing = calculate_voxel_spacing(reference_image)
    streamlines = tractogram.streamlines
    E1, E2 = cluster_endpoints(streamlines)
    E1, E2 = determine_surface_end(E1, E2)
    return tractogram, voxel_spacing, E1, E2
