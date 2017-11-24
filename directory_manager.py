import unittest
import logging
from glob import glob
from pathlib import Path

class DirectoryManager(object):
    """
    Represents a class which stores a list of directories while validating
    which is valid and may be added.
    """
    def __init__(self):
        self.__directories = []
        super(
            DirectoryManager,
            self
        ).__init__()
    
    """
    Determines whether the path is a valid directory which may be added 
    to the the current instance.
    Returns: Boolean
    """
    def is_valid_directory(self, directory, directory_list):
        if self.is_empty(directory) or self.exists(directory):
           return False

        elif not Path(directory).is_dir():
            logging.info(f"\"{ directory }\" is not a directory.")
            return False

        else:
            return True

    """
    Determines whether the path is logically empty.
    Returns: Boolean
    """
    def is_empty(self, string):
        if string == "" or string == None:
            logging.info("Empty string passed")
            return True

        else:
            return False        

    """
    Replaces the Windows-specific path separator with the Unix-like one.
    Returns: String of the normalized path.
    """
    def normalize_path(self, path):
        return path.replace("\\", "/")

    """
    Adds a directory to the directory manager instance.
    """
    def add(self, directory):
        directory_list = []

        if isinstance(directory, list):
            directory_list.extend(directory)

        else:
            directory_list.append(directory)

        for path in directory_list:
            for globbed_path in glob(path):
                globbed_path = self.normalize_path(globbed_path)

                if self.is_valid_directory(globbed_path, self.__directories):
                    self.__directories.append(globbed_path)

    """
    Removes the specified path from the instance.
    Returns: A boolean of whether all specified paths were removed.
    """
    def remove(self, directory):
        raise NotImplementedError

    """
    Completely clears the instance.
    Returns: A boolean if it was successful.
    """
    def clear(self):
        self.__directories.clear()
        return True

    """
    Returns a list of all the directories managed by the instance.
    Returns: List
    """
    def list(self):
        return list(self.__directories)

    def exists(self, directory):
        if directory in self.__directories:
            logging.info(f"Directory exists: { directory }")
            return True
        
        else:
            return False


# class TestDirectoryManager(object):
#     """docstring for TestDirectoryManager"""

#     self.manager = None
#     def setUp(self):
#         self.manager = DirectoryManager()

#     def test_add_directories(self):        
#         self.manager.add([
#             "d://evrnet",
#             "c://byteb",
#             "c://hello",
#             "c://ruby/*",
#             "c://scripts/*"
#         ])

#     def tearDown(self):
#         self.manager.clear();
#         self.manager = None
        