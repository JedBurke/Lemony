import os
from os import path
from os.path import join
from pathlib import Path
from glob import glob

import fnmatch

from pathobject_manager import PathObjectManager

class FileManager(PathObjectManager):
    def __init__(self):
        super().__init__()

        self.whitelist = True
        self.validation_function = self.is_valid_file

    @property
    def whitelist(self):
        return self._whitelist
    @whitelist.setter
    def whitelist(self, value):
        self._whitelist = value
    
    def get_extension(self, path):
        base = os.path.basename(path)
        parts = os.path.splitext(base)
        
        extension = ""

        if len(parts) > 1:
            extension = parts[len(parts) - 1][1:]

        return extension

    def add_files(self, directory, included_extensions="*"):
        files = []
        extensions = []

        assert included_extensions != None

        if isinstance(included_extensions, list):
            extensions.extend(included_extensions)
        else:
            extensions.append(included_extensions)

        if self.whitelist:
            for extension in extensions:
                temp_extension = ""

                if not extension.startswith("*."):
                    temp_extension = "*." + extension

                files.extend(glob(join(directory, temp_extension)))

        else:
            with os.scandir(directory) as it:
                for entry in it:
                    if entry.is_file():
                        extension = self.get_extension(entry.path)

                        if not extension in extensions:
                            files.append(entry.path)

        for file in files:
            super().add(file)


    def is_valid_file(self, path):
        return False

fm = FileManager()

fm.whitelist = False
fm.add_files("D:/documents", ["7z", "idle"])

print("Files:")
for f in fm.list():
    print(f)
