import unittest
import logging
from glob import glob
from pathlib import Path
import os
from os import path

class PathObjectManager:
    def __init__(self):
        self.__paths = []
        self.validation_function = None
    
    """
    Determines whether the path is a valid directory which may be added 
    to the the current instance.

    Returns:
        Boolean
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
    Determines whether the string is logically empty.

    Returns:
        Boolean
    """
    def is_empty(self, string):
        if string == "" or string == None:
            logging.info("Empty string passed")
            return True

        else:
            return False        

    """
    Replaces the Windows-specific path separator with the Unix-like one.

    Returns:
        String of the normalized path.
    """
    def normalize_path(self, path):
        return path.replace("\\", "/")

    """
    Adds a path to the manager instance.
    """
    def add(self, path):
        paths_list = []

        # Tests if the passed path is a list. If it is, the paths_list
        # will be extended with it.
        if isinstance(path, list):
            paths_list.extend(path)

        else:
            paths_list.append(path)

        # Iterate through each item in the paths list.
        for path in paths_list:
            path = os.path.normpath(path)

            valid_path = False
            
            if self.validation_function is not None:
                valid_path = self.validation_function(path)

            else:
                valid_path = True

            self.__paths.append(path)


    """
    Removes the specified path from the instance.
    
    Returns:
        A boolean of whether all specified paths were removed.
    """
    def remove(self, path):
        raise NotImplementedError

    """
    Completely clears the instance of its paths.
    
    Returns: 
        A boolean if it was successful.
    """
    def clear(self):
        self.__paths.clear()
        return True

    """
    Returns a list of all the directories managed by the instance.
    
    Returns:
        List
    """
    def list(self):
        return list(self.__paths)

    def exists(self, directory):
        if directory in self.__paths:
            logging.info(f"Directory exists: { directory }")
            return True
        
        else:
            return False
