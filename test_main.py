import unittest
import subprocess

class TestMain(unittest.TestCase):

    def test_main_help(self):
        result = subprocess.run(["python", "tract_analysis/main.py", "--help"], stdout=subprocess.PIPE)
        self.assertIn(b"usage", result.stdout)

if __name__ == '__main__':
    unittest.main()
