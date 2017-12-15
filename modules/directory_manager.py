from .pathobject_manager import PathObjectManager

from glob import glob
import logging
from pathlib import Path

class DirectoryManager(PathObjectManager):
    def __init__(self):        
        super().__init__()

        # self.whitelist = True
        self.validation_function = self.is_valid_directory

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
