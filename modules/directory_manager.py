from .pathobject_manager import PathObjectManager

from glob import glob
import logging
from pathlib import Path
import unittest

class DirectoryManager(PathObjectManager):
    def __init__(self):        
        super().__init__()

        # self.whitelist = True
        self.validation_function = self.is_valid_directory


    """
    Adds a directory or list of diectories to the instance.
    """
    def add(self, directory):        
        directories = []
        processed_directories = []
        globbed_paths = []

        if isinstance(directory, list):
            directories.extend(directory)

        else:
            directories.append(directory)

        for directory in directories:
            globbed_paths = glob(directory)

            for directory in globbed_paths:
                if self.is_valid_directory(directory):
                    processed_directories.append(directory)
                
                # Todo: Log failure to add directory.


        super().add(processed_directories)

        # directory_list = []

        # if isinstance(directory, list):
        #     directory_list.extend(directory)

        # else:
        #     directory_list.append(directory)

        # for path in directory_list:
        #     for globbed_path in glob(path):
        #         globbed_path = self.normalize_path(globbed_path)

        #         if self.is_valid_directory(globbed_path, self.__directories):
        #             self.__directories.append(globbed_path)

    """
    Determines whether the path is a valid directory which may be added 
    to the the current instance.
    
    Returns:
        Boolean
    """
    def is_valid_directory(self, directory):
        if self.is_empty(directory) or self.exists(directory):
           return False

        elif not Path(directory).is_dir():
            logging.info(f"\"{ directory }\" is not a directory.")
            return False

        else:
            return True

    """
    Determines whether the path is logically empty.
    
    Returns:
        Boolean
    """
    def is_empty(self, string):
        if string == "" or string == None:
            logging.info("Empty string passed")
            return True

        else:
            return False

class TestDirectoryManager(unittest.TestCase):
    def setUp(self):
        self.instance = DirectoryManager()

    def test_add(self):
        # Todo: Use proper testing environment.
        self.instance.add("d:/*")

        # for directory in self.instance.list():
        #     print(directory)

    def test_add_list(self):
        # Todo: Use proper testing environment.
        self.instance.add([
            "d:/*",
            "d:/queen's blade/*/*/*/*"
        ])

        # for directory in self.instance.list():
        #     print(directory)

if __name__ == '__main__':
    unittest.main()
