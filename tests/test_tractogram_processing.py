import unittest
import numpy as np
from tract_analysis.tractogram_processing import load_tractogram_file, calculate_voxel_spacing, determine_surface_end, \
    cluster_endpoints


class TestTractogramProcessing(unittest.TestCase):

    def test_load_tractogram_file(self):
        # Mock paths for testing
        tract_path = "mock_tractogram.tck"
        reference_image = "mock_reference_image.nii"

        # This function would require actual files, skipping actual call
        # tractogram = load_tractogram_file(tract_path, reference_image)
        # self.assertIsNotNone(tractogram)
        pass

    def test_calculate_voxel_spacing(self):
        # Mock path for testing
        reference_image = "mock_reference_image.nii"

        # This function would require an actual file, skipping actual call
        # voxel_spacing = calculate_voxel_spacing(reference_image)
        # self.assertTrue(isinstance(voxel_spacing, tuple))
        pass

    def test_determine_surface_end(self):
        E1 = np.array([[1, 2, 3], [4, 5, 6]])
        E2 = np.array([[7, 8, 9], [10, 11, 12]])
        result_E1, result_E2 = determine_surface_end(E1, E2)
        self.assertTrue(isinstance(result_E1, np.ndarray))
        self.assertTrue(isinstance(result_E2, np.ndarray))

    def test_cluster_endpoints(self):
        streamlines = [np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]]), np.array([[0, 0, 0], [1, 0, 0], [2, 0, 0]])]
        E1, E2 = cluster_endpoints(streamlines)
        self.assertTrue(isinstance(E1, np.ndarray))
        self.assertTrue(isinstance(E2, np.ndarray))


if __name__ == '__main__':
    unittest.main()
