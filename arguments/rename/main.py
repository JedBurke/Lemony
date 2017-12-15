import argparse
import json
import logging
from logging import Logger
from ..argument_base import ArgumentBase
from .match_pattern_action import MatchPatternAction

from constants import Constants
from helpers.user import UserHelpers
from helpers.file import FileHelpers
from helpers.log import LogHelpers
from helpers.pattern import PatternHelpers

from modules.directory_manager import DirectoryManager
from modules.file_manager import FileManager
# from argument_actions import *
from colorama import init, Fore, Back, Style
import os
from os import path
from os.path import join
from pathlib import Path
import sys

init(autoreset=True)

class ArgRename(ArgumentBase):
    def __init__(self, parser):
        ArgumentBase.__init__(self)

        self.parent_parser = parser

        self.parser = self.parent_parser.add_parser(
            "rename",
            help="renames files with regular expression patterns"
        )

        self.register(self.parser)

        # Prints certain values which the general user wouldn't need.
        self.debug = False

        self.verbose = False

        # If "True", dictates that the rename action is not taken.
        self.dry_run = False

        # Profiles act as a convenient way to repetitively replace text. This
        # variable dictates which profile is to be used.
        self.profile = None

        # Indicates whether the file extensions are deliberately excluded or
        # included. Deliberately included or whitelisted, is the default.
        self.blacklist_ext = False

        # The list of directories which to scan for files matching the regex.
        self.directory_list = []

        self.regex_pattern = ""
        
        self.regex_replace = ""

        self.file_types = ["*"]

        self.directory_manager = DirectoryManager()

    def args_entry(self, args):
        self.parse_settings(args)
        self.run()

        # print(args)

        return

    def register(self, parser):
        parser.add_argument("args")

        parser.add_argument(
            "-n",
            "--dry-run",
            action="store_true",
            help="simulate operation without actually doing it"
        )

        parser.add_argument(
            "-m",
            "--match-pattern",
            action=MatchPatternAction,
            help="specify the regex pattern used to match files"
        )

        parser.add_argument(
            "-r",
            "--replace-pattern",
            default=None,
            help="specify the replacement string for matching files"
        )

        parser.add_argument(
            "-p",
            "--profile",
            default=None,
            help="select the saved profile to use for the renaming process"
        )

        parser.add_argument(
            "-x",
            "--ext",
            default=None,
            help="specify which extensions are to be included in the \
            search"
        )

        parser.add_argument(
            "--blacklist",
            action="store_true",
            default=False,
            help="exclude files based on extension rather than \
            including them based on it"
        )

        parser.add_argument(
            "--debug",
            action="store_true",
            help="display light information for debugging or troubleshooting \
            purposes"
        )

        parser.add_argument(
            "--verbose",
            action="store_true",
            default=False,
            help="display verbose information about the operation"
        )

        parser.set_defaults(func=self.args_entry)

    def parse_settings(self, args):
        # Todo: Fix bug where the directory won't be added.
        self.directory_manager.add(
            args.args.split(
                Constants.PATH_SEPARATOR
            )
        )
        
        if args.debug:
            self.debug = True

        if args.verbose:
            self.debug = True
            self.verbose = True

        if args.dry_run:
            self.dry_run = True

            if self.debug:
                print(Fore.CYAN + "Dry run: " + Fore.RESET + str(self.dry_run))

        if args.match_pattern is not None:
            self.regex_pattern = args.match_pattern

            if self.debug:
                print(Fore.CYAN + "Match Pattern: "
                      + Fore.RESET + f"{regex_pattern.pattern}")

        if args.replace_pattern is not None:
            self.regex_replace = args.replace_pattern

            if self.debug:
                print(Fore.CYAN + f"Replace Pattern: {regex_replace}")

        if args.ext is not None:
            self.file_types = FileHelpers.parse_extensions(args.ext)

            if self.debug:
                print(Fore.CYAN + f"Extension List: {file_types}")


        # Extensions mentioned in the 'ext' list are to be excluded file types.
        self.blacklist_ext = args.blacklist

        # Profiles are last since they overwrite all other arguments.
        if args.profile is not None:
            # Get the system profile path and load the files.

            profile_path = UserHelpers.get_profiles_path()
            if profile_path.exists():
                profile_content = FileHelpers.read_file(profile_path)

                profiles = json.loads(profile_content)

            else:
                print(Fore.RED + "The profile configuration file cannot be found.")
                exit()


            # Gets the profile path relative to the script.
            # profile_path = path.join(sys.path[0], PROFILES_FILE_NAME)

            # if os.path.exists(profile_path):
            #     with open(
            #         profile_path,
            #         encoding="utf-8-sig",
            #         mode="r"
            #     ) as profile_content_file:
            #         profile_content = profile_content_file.read()

            #     profiles = json.loads(profile_content)

            # else:
            #     print(Fore.RED + "The profile configuration file cannot be found.")
            #     exit()

            # user_config_path = path.join(
            #     path.expanduser(f"~/{USER_DATA_DIR_NAME}"),
            #     PROFILES_FILE_NAME
            # )

            # user_config = Path(user_config_path)

            # user_config = UserHelpers.get_user_directory()
            user_profiles_path = UserHelpers.get_user_profiles_path()



            # Todo: Check if there was an indentation error in the
            # original script.
            if user_profiles_path.exists():
                # Instead of creating the directory, check if it exists and include
                # it should if it does.
                with open(
                    user_profiles_path,
                    encoding="utf-8-sig",
                    mode="r"
                ) as profile_content_file:
                    profile_content = profile_content_file.read()

                user_profiles = json.loads(profile_content)

                if user_profiles is not None:
                    profiles.update(user_profiles)

                profile_str = args.profile

                if profile_str not in profiles:
                    print(Fore.RED + f"Profile \"{profile_str}\" not found")
                    print(Fore.RED + "Aborting.")
                    exit()

                self.profile = profiles[profile_str]
                self.regex_pattern = self.profile["match"]
                self.regex_replace = self.profile["replace"]
                self.file_types = self.profile["ext"]

                if self.regex_pattern is not None:
                    self.regex_pattern = PatternHelpers.parse_regex(self.regex_pattern)

                if "dir" in self.profile:
                    #directory_list.extend(profile["dir"])
                    self.directory_manager.add(self.profile["dir"])

                if "whitelist" in self.profile:
                    self.blacklist_ext = not self.profile["whitelist"]

                else:
                    self.blacklist_ext = False

                if self.debug:
                    print(Fore.CYAN + "Name: " + Fore.RESET + profile_str)
                    print(Fore.CYAN + "Match: " + Fore.RESET + self.regex_pattern.pattern)
                    print(Fore.CYAN + "Replace: " + Fore.RESET + self.regex_replace)
                    print(Fore.CYAN + "Available extensions: " + Fore.RESET + f"{ self.file_types }")
                    print(Fore.CYAN + "Whitelist extensions: " + Fore.RESET + f"{ not self.blacklist_ext }")

                if "dir" in self.profile:
                    print(Fore.CYAN + f"Included directories: " + Fore.RESET + f"{ self.profile['dir'] }")

    def run(self):
        # Begin work.

        # Verify and parse match pattern.
        regex = self.regex_pattern

        if self.debug:
            print(Fore.CYAN + "Regex object: " + Fore.RESET + f"{regex}")

        for directory in self.directory_manager.list():
            if directory == "":
                # Skip empty path. Used for profiles which contain the directory.

                if self.debug:
                    print(Fore.CYAN + "Skipping blank directory path.")

                continue

            print(Fore.YELLOW + f"\nEntering \"{directory}\":")

            directory_path = Path(directory)

            if not directory_path.exists():
                LogHelpers.print_error("Directory does not exist.")
                continue

            elif not directory_path.is_dir():
                LogHelpers.print_error("Skipping, not a directory.")
                continue

            # Gather files.
            # Files which have types specified in the 'file_types' list will be
            # added to the 'files' list. Conversely, if the 'blacklist' switch 
            # is active, those files will not be added, but everything else
            # will be added.

            file_manager = FileManager()    
            file_manager.add(
                directory,
                self.file_types,
                not self.blacklist_ext
            )

            if self.verbose:
                for file in file_manager.list():
                    print(Fore.CYAN + "Matching extension:\n    " + Fore.RESET + Path(file).name)

                # Create new line.
                print()

            # for file in files:
            for file in file_manager.list():
                file_name = Path(file).name

                # Perform a search to see if the file is eligible then do the replacement.
                # This is done not to pollute the console output.
                if regex.search(file_name) is None:
                    if verbose:
                        print(
                            Fore.CYAN + "No match: " + Fore.RESET + 
                            Fore.RED + file_name
                        )

                    continue

                new_name = regex.sub(self.regex_replace, file_name)
                new_path = Path(
                    join(
                        directory,
                        new_name
                    )
                )

                if new_path.exists():
                    if self.debug:
                        self.print_error(
                            f"A file with the name of \"{new_name}\" \
                            already exists."
                        )

                    else:
                        self.print_error(
                            "A file with the target name already exists."
                        )

                    continue

                else:
                    self.print_new_name(file_name, new_name)

                    self.rename(file, new_path, self.dry_run)

    def print_new_name(self, original_name, new_name):
        print(
            Fore.RED + original_name + Fore.RESET +
            "\n    -> " + Fore.GREEN +
            new_name
        )

    def rename(self, original_path, new_path, dry_run=False):
        # Don't perform the rename if it's a dry run.
        if not dry_run:
            # log.
            os.rename(original_path, new_path)

        else:
            # log.
            return

    def iterate_directories(self):
        return

    def iterate_files_action(self):
        return
