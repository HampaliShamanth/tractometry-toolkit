import unittest
import os
from tract_analysis.data_aggregation import aggregate_results_to_dataframe, save_to_excel


class TestDataAggregation(unittest.TestCase):

    def setUp(self):
        # Setup mock data for testing
        self.root_directory = "mock_root_directory"
        self.file_paths = ["AF_L.tck", "AF_R.tck"]
        self.reference_image = os.path.join(self.root_directory, "mock_reference_image.nii")

        # Create mock directory structure
        os.makedirs(self.root_directory, exist_ok=True)
        open(self.reference_image, 'a').close()  # Create a mock reference image file

        for subject in ["subject1", "subject2"]:
            for subdir in ["subdir1", "subdir2"]:
                subject_dir = os.path.join(self.root_directory, subject, subdir)
                os.makedirs(subject_dir, exist_ok=True)
                for file_path in self.file_paths:
                    open(os.path.join(subject_dir, file_path), 'a').close()

    def tearDown(self):
        # Clean up mock directory structure
        for subject in ["subject1", "subject2"]:
            for subdir in ["subdir1", "subdir2"]:
                subject_dir = os.path.join(self.root_directory, subject, subdir)
                for file_path in self.file_paths:
                    os.remove(os.path.join(subject_dir, file_path))
                os.rmdir(subject_dir)
        os.remove(self.reference_image)
        os.rmdir(self.root_directory)

    def test_aggregate_results_to_dataframe(self):
        dfs = aggregate_results_to_dataframe(self.root_directory, self.file_paths, self.reference_image)
        self.assertTrue(isinstance(dfs, dict))

    def test_save_to_excel(self):
        dfs = aggregate_results_to_dataframe(self.root_directory, self.file_paths, self.reference_image)
        output_file = "mock_output.xlsx"
        save_to_excel(dfs, output_file)
        self.assertTrue(os.path.isfile(output_file))
        os.remove(output_file)


if __name__ == '__main__':
    unittest.main()
