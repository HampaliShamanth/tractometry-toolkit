import numpy as np
from scipy.ndimage import binary_erosion


def calculate_length(streamlines):
    """
    Calculate the length of each streamline in the bundle.

    Parameters:
        streamlines (Streamlines): Streamlines of the tract.

    Returns:
        lengths (list): Lengths of each streamline.
    """
    lengths = [np.sum(np.linalg.norm(np.diff(streamline, axis=0), axis=1)) for streamline in streamlines]
    return lengths


def calculate_span(streamlines):
    """
    Calculate the span of each streamline in the bundle.

    Parameters:
        streamlines (Streamlines): Streamlines of the tract.

    Returns:
        spans (list): Spans of each streamline.
    """
    spans = [np.linalg.norm(streamline[0] - streamline[-1]) for streamline in streamlines]
    return spans


def calculate_curl(lengths, spans):
    """
    Calculate the curl of the bundle.

    Parameters:
        lengths (list): Lengths of each streamline.
        spans (list): Spans of each streamline.

    Returns:
        curl (float): Curl of the bundle.
    """
    avg_length = np.mean(lengths)
    avg_span = np.mean(spans)
    curl = (avg_length / avg_span) * 2
    return curl


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
    voxels_binary = voxels_data > 0
    surface_voxels = voxels_binary & ~binary_erosion(voxels_binary)
    surface_voxel_count = np.count_nonzero(surface_voxels)
    voxel_spacing_sq = np.sqrt(np.dot(voxel_spacing, voxel_spacing))
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


def calculate_diameter(surface_volume, mean_length):
    """
    Calculate the diameter of the tractogram.

    Parameters:
        surface_volume (float): Surface volume of the tractogram.
        mean_length (float): Mean length of the streamlines.

    Returns:
        diameter (float): Diameter of the tractogram.
    """
    return 2 * np.sqrt(surface_volume / (np.pi * mean_length))


def calculate_elongation(mean_length, diameter):
    """
    Calculate the elongation of the tractogram.

    Parameters:
        mean_length (float): Mean length of the streamlines.
        diameter (float): Diameter of the tractogram.

    Returns:
        elongation (float): Elongation of the tractogram.
    """
    return mean_length / diameter


def calculate_tract_statistics(lengths, spans, voxel_spacing, N, voxels_data):
    """
    Calculate various tract statistics.

    Parameters:
        lengths (list): Lengths of each streamline.
        spans (list): Spans of each streamline.
        voxel_spacing (tuple): Spacing of the voxels in x, y, and z directions.
        N (int): Number of non-zero voxels.
        voxels_data (ndarray): Voxel data of the tractogram.

    Returns:
        tract_stats (dict): Dictionary containing the computed statistics.
    """
    curl = calculate_curl(lengths, spans)
    voxel_volume = np.prod(voxel_spacing)
    surface_volume = calculate_surface_volume(N, voxel_volume)
    surface_area = calculate_surface_area(voxels_data, voxel_spacing)
    diameter = calculate_diameter(surface_volume, np.mean(lengths))
    elongation = calculate_elongation(np.mean(lengths), diameter)
    irregularity = surface_area / (np.pi * diameter * np.mean(lengths))

    tract_stats = {
        "Mean Length": float(np.mean(lengths)),
        "Mean Span": float(np.mean(spans) / 2),
        "Curl": float(curl),
        "Diameter": float(diameter),
        "Elongation": float(elongation),
        "Total Volume": float(surface_volume),
        "Total Surface Area": float(surface_area),
        "Irregularity": float(irregularity),
    }

    return tract_stats
