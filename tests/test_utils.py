import unittest
import numpy as np
from tract_analysis.utils import voxelise_tractogram, calculate_surface_volume, calculate_surface_area, \
    calculate_end_surface_area, calculate_radius, calculate_irregularity


class TestUtils(unittest.TestCase):

    def test_voxelise_tractogram(self):
        # Mock paths for testing
        tract_path = "mock_tractogram.tck"
        reference_image = "mock_reference_image.nii"

        # This function would require actual files, skipping actual call
        # voxel_count, voxels_data = voxelise_tractogram(tract_path, reference_image)
        # self.assertIsInstance(voxel_count, int)
        # self.assertIsInstance(voxels_data, np.ndarray)
        pass

    def test_calculate_surface_volume(self):
        surface_volume = calculate_surface_volume(4, 1.0)
        self.assertEqual(surface_volume, 4.0)

    def test_calculate_surface_area(self):
        voxels_data = np.array([[[1, 0], [0, 1]], [[1, 1], [0, 0]]])
        voxel_spacing = (1.0, 1.0, 1.0)
        surface_area = calculate_surface_area(voxels_data, voxel_spacing)
        self.assertTrue(isinstance(surface_area, float))

    def test_calculate_end_surface_area(self):
        surface_area = calculate_end_surface_area(4, (1.0, 1.0, 1.0))I
        self.assertEqual(surface_area, 1.0)

    def test_calculate_radius(self):
        radius = calculate_radius(1.0)
        self.assertEqual(radius, np.sqrt(1.0 / np.pi))

    def test_calculate_irregularity(self):
        irregularity = calculate_irregularity(1.0, 1.0)
        self.assertEqual(irregularity, np.pi)


if __name__ == '__main__':
    unittest.main()
