import unittest
import numpy as np
from tract_analysis.calculations import calculate_length, calculate_span, calculate_curl, calculate_surface_volume, \
    calculate_surface_area, calculate_end_surface_area, calculate_radius, calculate_irregularity, calculate_diameter, \
    calculate_elongation, calculate_tract_statistics


class TestCalculations(unittest.TestCase):

    def setUp(self):
        # Setup mock data for testing
        self.streamlines = [np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]]), np.array([[0, 0, 0], [1, 0, 0], [2, 0, 0]])]
        self.lengths = calculate_length(self.streamlines)
        self.spans = calculate_span(self.streamlines)
        self.voxels_data = np.array([[[1, 0], [0, 1]], [[1, 1], [0, 0]]])
        self.voxel_spacing = (1.0, 1.0, 1.0)

    def test_calculate_length(self):
        self.assertEqual(self.lengths, [np.sqrt(3) * 2, 2])

    def test_calculate_span(self):
        self.assertEqual(self.spans, [np.sqrt(12), np.sqrt(4)])

    def test_calculate_curl(self):
        curl = calculate_curl(self.lengths, self.spans)
        self.assertTrue(isinstance(curl, float))

    def test_calculate_surface_volume(self):
        surface_volume = calculate_surface_volume(4, 1.0)
        self.assertEqual(surface_volume, 4.0)

    def test_calculate_surface_area(self):
        surface_area = calculate_surface_area(self.voxels_data, self.voxel_spacing)
        self.assertTrue(isinstance(surface_area, float))

    def test_calculate_end_surface_area(self):
        surface_area = calculate_end_surface_area(4, self.voxel_spacing)
        self.assertEqual(surface_area, 1.0)

    def test_calculate_radius(self):
        radius = calculate_radius(1.0)
        self.assertEqual(radius, np.sqrt(1.0 / np.pi))

    def test_calculate_irregularity(self):
        irregularity = calculate_irregularity(1.0, 1.0)
        self.assertEqual(irregularity, np.pi)

    def test_calculate_diameter(self):
        diameter = calculate_diameter(4.0, np.mean(self.lengths))
        self.assertTrue(isinstance(diameter, float))

    def test_calculate_elongation(self):
        diameter = calculate_diameter(4.0, np.mean(self.lengths))
        elongation = calculate_elongation(np.mean(self.lengths), diameter)
        self.assertTrue(isinstance(elongation, float))

    def test_calculate_tract_statistics(self):
        tract_stats = calculate_tract_statistics(self.lengths, self.spans, self.voxel_spacing, 4, self.voxels_data)
        self.assertTrue(isinstance(tract_stats, dict))


if __name__ == '__main__':
    unittest.main()
