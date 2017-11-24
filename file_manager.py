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
                        base = os.path.basename(entry.path)
                        split = os.path.splitext(base)
                        parts = len(split[1])

                        if len(split) > 1 and parts > 0:
                            extension = split[parts - 1][1:]

                            if not extension in extensions:
                                files.append(entry.path)

            # for file in os.listdir(directory):
            #     path = Path(os.path.join(directory, file))

            #     # Remove the leading "."" from the extension.
            #     extension = path.suffix.casefold()[1:]

            #     if extension != "*" and not extension in extensions:
            #         files.append(join(directory, file))

            #return

        for file in files:
            super().add(file)

    # # Gather files.
    # # Files which have types specified in the 'file_types' list will be added
    # # to the 'files' list. Conversely, if the 'blacklist' switch is active,
    # # those files will not be added, but everything else will be added.
    # files = []

    # if blacklist_ext:
    #     for file in os.listdir(directory):
    #         f_obj = Path(os.path.join(directory, file))

    #     if f_obj.is_file():
    #         # Remove the leading "."" from the extension.
    #         f_ext = f_obj.suffix.casefold()[1:]

    #         if not (f_ext) in file_types:
    #             print(file)

    # else:
    #     for ext in file_types:
    #         t_ext = ext

    #         if not ext.startswith("*."):
    #             t_ext = "*." + ext

    #         files.extend(glob(join(directory, t_ext)))

    def is_valid_file(self, path):
        return False

fm = FileManager()

fm.whitelist = True
fm.add_files("D:/documents")

print("Files:")
for f in fm.list():
    print(f)
