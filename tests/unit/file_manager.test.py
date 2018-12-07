import unittest
import os
from shutil import rmtree

from tests.features import global_config as config
from bdt_template import FileManager


def generate_test_file(file_path, selector_id):
    with open(file_path, "w+") as f:
        for i in range(20):
            f.write("Filler Text \n")
            if i == 10 and selector_id is not False:
                f.write(selector_id + '\n')


class FileManagerTests(unittest.TestCase):

    def test_file_exists(self):
        selector_id = "FMT1 test_file_exists"
        file_name = "test_file_exists.txt"
        file_path = config.TEMP_DIR + file_name

        # Create a test file with a selector id
        generate_test_file(file_path, selector_id)

        # Check the file_exists function detects the file
        result = FileManager.file_exists(file_path)
        expected = os.path.isfile(file_path)
        self.assertEqual(result, expected)

    def test_file_basename(self):
        selector_id = "FMT2 test_file_basename"
        file_name = "test_file_basename.txt"
        file_path = config.TEMP_DIR + file_name

        # Create a test file with a selector id
        generate_test_file(file_path, selector_id)

        # Check the file_basename function extracts the correct file basename
        result = FileManager.file_basename(file_path)
        expected = os.path.basename(file_path)
        self.assertEqual(result, expected)

    def test_scan_files_matched(self):
        selector_id = "FMT3 test_scan_files_matched"
        file_name = "test_scan_files_matched.txt"
        file_path = config.TEMP_DIR + file_name

        # Create a test file with a selector id
        generate_test_file(file_path, selector_id)

        # Check the file and directory are correctly returned
        filepath_result, directory_result = FileManager.scan_files(config.TEMP_DIR, selector_id, 'contents')
        directory_expected = config.TEMP_DIR
        filepath_expected = file_path
        self.assertEqual(directory_result, directory_expected)
        self.assertEqual(filepath_result, filepath_expected)

        # Clean up
        os.remove(file_path)

    def test_scan_files_unmatched(self):
        file_id = "FMT4 Test File"
        file_name = "test_scan_files_unmatched.txt"
        file_path = config.TEMP_DIR + file_name

        # Create a test file without a selector id
        generate_test_file(file_path, False)

        # Check the file and path are set to False
        filepath_result, directory_result = FileManager.scan_files(config.TEMP_DIR, file_id, 'contents')
        filepath_expected = False
        directory_expected = False
        self.assertEqual(filepath_result, filepath_expected)
        self.assertEqual(directory_result, directory_expected)

        # Clean up
        os.remove(file_path)

    def test_scan_dirs(self):
        file_id = "FMT5 Test File"
        test_dirs_names = ['test1', 'test2']
        test_files_valid = ['test_scan_dirs_match.txt']
        test_files_invalid = ['test_scan_dirs_no_match.txt']

        test_dirs = [config.TEMP_DIR + dir_name + '\\' for dir_name in test_dirs_names]

        # Make test directories
        for test_dir in test_dirs:
            os.makedirs(test_dir)

        # Generate all invalid test files in one directory
        for invalid_file in test_files_invalid:
            generate_test_file(test_dirs[0] + invalid_file, False)

        # Generate all valid test files in another directory
        for valid_file in test_files_valid:
            generate_test_file(test_dirs[1] + valid_file, file_id)

        # Get result, which should be the second directory
        matched_file, matched_dir = FileManager.scan_dirs(file_id, test_dirs, 'contents')
        expected = test_dirs[1]
        result = matched_dir

        self.assertEqual(result, expected)

        # Remove all test directories
        for test_dir in test_dirs:
            rmtree(test_dir)

    def test_copy_file(self):
        # Generate test file and directory
        test_filename = 'test_copy_file.txt'
        test_dir = 'copy_file_test\\'
        generate_test_file(config.TEMP_DIR + test_filename, '12345')
        os.makedirs(config.TEMP_DIR + test_dir)

        # Copy file to test directory
        FileManager.copy_file(config.TEMP_DIR + test_filename, config.TEMP_DIR + test_dir + test_filename)

        # Check that file exists in the
        result = os.path.isfile(config.TEMP_DIR + test_dir + test_filename)
        expected = True

        self.assertEqual(result, expected)

        # Remove all test directories
        rmtree(config.TEMP_DIR + test_dir)


if __name__ == '__main__':

    # Cleanup temp directory
    if os.path.isdir(config.TEMP_DIR):
        rmtree(config.TEMP_DIR)
    os.mkdir(config.TEMP_DIR)

    # Run tests
    unittest.main()
