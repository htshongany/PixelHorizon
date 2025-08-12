import sys
import os
import unittest
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from image_ops.vectorize import vectorize_image
from image_ops.utils import get_image_name

def is_potrace_available():
    """Check if potrace executable is available in the project's bin directory or system PATH."""
    potrace_executable = "potrace.exe"
    
    # Check for potrace.exe in the project's bin directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    local_potrace_path = os.path.join(project_root, "bin", potrace_executable)
    if os.path.exists(local_potrace_path):
        return True

    # If not found locally, check the system's PATH
    try:
        subprocess.run([potrace_executable, '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

@unittest.skipIf(not is_potrace_available(), "Potrace executable not found, skipping vectorization tests.")
class TestVectorize(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.input_image_path = os.path.join(os.path.dirname(__file__), 'logo.png')
        self.output_dir = os.path.dirname(__file__)
        self.test_image_name = get_image_name(self.input_image_path)
        self.output_files = []

    def tearDown(self):
        """Clean up after each test."""
        for file_path in self.output_files:
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_vectorize_image(self):
        """Test converting a PNG image to SVG."""
        output_path = os.path.join(self.output_dir, f"{self.test_image_name}.svg")
        self.output_files.append(output_path)

        result_path = vectorize_image(self.input_image_path, custom_output_path=output_path)
        
        self.assertTrue(os.path.exists(result_path))
        self.assertEqual(result_path, output_path)
        
        # Check if the output file contains SVG tags
        with open(result_path, 'r') as f:
            content = f.read()
            self.assertIn('<svg', content)
            self.assertIn('</svg>', content)

if __name__ == '__main__':
    unittest.main(verbosity=2)
