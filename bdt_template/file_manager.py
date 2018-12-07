import os
import time
from shutil import copyfile
from glob import glob


class FileManager:

    @staticmethod
    def file_exists(file):
        """ Checks a file exists

        :param file: The full filepath to check exists
        :return: True if the file exists
        """
        return os.path.isfile(file)

    @staticmethod
    def file_basename(filepath):
        """ Returns the basename of a filepath

        :param filepath: The full filepath to extract the basename from
        :return: The basename of the given filepath
        """
        return os.path.basename(filepath)

    @staticmethod
    def copy_file(source, destination):
        """ Copies a file from one directory to another

        :param source: The source path of the file
        :param destination: The destination path to copy the file to
        """
        copyfile(source, destination)

    @staticmethod
    def scan_files(directory, selector_value, method, scanned_file_list=[]):
        """ Scans a directory for a select file

        :param directory: Directory to scan files for
        :param selector_value: The value to search for in each file
        :param method: Method used to scan files ('contents', 'filename')
        :param scanned_file_list: List of files that have already been scanned
        :return: The matched file and the directory, or False, False
        """
        # Lists all files in directory and filters those already scanned
        all_files = glob(os.path.join(directory, '*'))
        files = set(all_files) - set(scanned_file_list)

        # For each file read the contents to find the ID.
        for file in files:
            # Ignore sub-directories
            if os.path.isdir(file):
                scanned_file_list.append(file)
            else:
                # Search the contents of the file
                if method == 'contents':
                    f = open(file, 'r')
                    contents = f.read()
                    f.close()

                    # If ID is found return the directory it was found, otherwise add the file to the scanned file list
                    if not (contents.find(selector_value) == -1):
                        return file, directory
                    else:
                        scanned_file_list.append(file)
                # Search the name of the file
                elif method == 'filename':
                    if selector_value in os.path.basename(file):
                        return file, directory
                    else:
                        scanned_file_list.append(file)

        # If file is not found return False
        return False, False

    @staticmethod
    def scan_dirs(selector_value, directories, method):
        """ Scans a list of directories for a file using scan_files

        :param selector_value: The value to search for in each file
        :param directories: The directories to scan files for
        :param method: Method used to scan files ('contents', 'filename')
        :return: The matched file and the directory, or False, False
        """
        # Set the scanned file list to empty
        scanned_file_list = []
        print("[", end="", flush=True)

        # Scan over a 2 minute period
        for x in range(24):
            print(".", end="", flush=True)
            # Scan each directory passed
            for directory in filter(None, directories):
                # Scan files that have been processed successfully and break if found
                matched_file, matched_dir = FileManager.scan_files(directory, selector_value, method, scanned_file_list)
                if matched_file and matched_dir:
                    print('] - File Found!')
                    return matched_file, matched_dir

            time.sleep(5)

        print('] - No File Found!')
        return False, False
