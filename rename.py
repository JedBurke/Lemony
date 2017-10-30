import argparse
from glob import glob
import io
import json
import os
from os import path
from os.path import join
from pathlib import Path
import re
import sys
from colorama import init, Fore, Back, Style

from helpers import FileHelpers, PatternHelpers
from argument_actions import *

from profile_subcommand import ProfileSubCommand

init(autoreset=True)

VERSION = "0.5.3"

# Todo: Use for separating the file types as well.
PATH_SEPARATOR = ";"

EXTENSION_SEPARATOR = ","

PROFILES_FILE_NAME = "profiles.json"

USER_DATA_DIR_NAME = "org.rename_data"

# Prints certain values which the general user wouldn't need.
debug = False

# If "True", dictates that the rename action is not taken.
dry_run = False

# Profiles act as a convenient way to repetitively replace text. This
# variable dictates which profile is to be used.
profile = None

# Indicates whether the file extensions are deliberately excluded or
# included. Deliberately included or whitelisted, is the default.
blacklist_ext = False

# The list of directories which to scan for files matching the regex.
directory_list = []


####### TODO #######
# 1. Allow globbing the directories.
#   path/to/ecchi/*
#       Search in all ecchi sub-directories.
#
# 2. Move the default arguments to the 'rename' subcommand.

####################


regex_pattern = ""
regex_replace = ""
file_types = ["*"]

parser = argparse.ArgumentParser(description="Rename files")
parser.add_argument("args")

parser.add_argument("-n",
                    "--dry-run",
                    action="store_true")

parser.add_argument("--version",
                    action="version",
                    version=f"Pyren Version: {VERSION}")

parser.add_argument("--debug",
                    action="store_true")

parser.add_argument("-m",
                    "--match-pattern",
                    action=MatchPatternAction)

parser.add_argument("-r",
                    "--replace-pattern",
                    default=None)

parser.add_argument("-p",
                    "--profile",
                    default=None)

parser.add_argument("-x",
                    "--ext",
                    default=None)

parser.add_argument("--blacklist",
                    action="store_true",
                    default=False)

subparsers = parser.add_subparsers()

subparsers.add_parser("rename"
                      , help="Renames files with names matching the provided \
                        pattern in the input directories.")

ProfileSubCommand(subparsers.add_parser("profile"
                                        , help="Provides access to profiles"))

subparsers.add_parser("test"
                      , help="Provides methods to test the match patterns \
                        against without affecting files.")


args = parser.parse_args()

directory_list = args.args.split(PATH_SEPARATOR)

if args.debug:
    debug = True

if args.dry_run:
    dry_run = True

    if debug:
        print(Fore.CYAN + "Dry run: " + Fore.RESET + str(dry_run))

if args.match_pattern is not None:
    regex_pattern = args.match_pattern

    if debug:
        print(Fore.CYAN + "Match Pattern: "
              + Fore.RESET + f"{regex_pattern.pattern}")

if args.replace_pattern is not None:
    regex_replace = args.replace_pattern

    if debug:
        print(Fore.CYAN + f"Replace Pattern: {regex_replace}")

if args.ext is not None:
    file_types = FileHelpers.parse_extensions(args.ext)

    if debug:
        print(Fore.CYAN + f"Extension List: {file_types}")


# Extensions mentioned in the 'ext' list are to be excluded file types.
blacklist_ext = args.blacklist

# Profiles are last since they overwrite all other arguments.
if args.profile is not None:
    # Gets the profile path relative to the script.
    profile_path = path.join(sys.path[0], PROFILES_FILE_NAME)

    if os.path.exists(profile_path):
        with open(profile_path,
                  encoding="utf-8-sig",
                  mode="r") as profile_content_file:
            profile_content = profile_content_file.read()

        profiles = json.loads(profile_content)

    else:
        print(Fore.RED + "The profile configuration file cannot be found.")
        exit()

    user_config_path = path.join(path.expanduser(f"~/{USER_DATA_DIR_NAME}"),
                                 PROFILES_FILE_NAME)
    user_config = Path(user_config_path)

if user_config.exists():
    # Instead of creating the directory, check if it exists and include
    # it should if it does.
    with open(user_config_path,
              encoding="utf-8-sig",
              mode="r") as profile_content_file:
        profile_content = profile_content_file.read()

    user_profiles = json.loads(profile_content)

    if user_profiles is not None:
        profiles.update(user_profiles)

    profile_str = args.profile

    if profile_str not in profiles:
        print(Fore.RED + f"Profile \"{profile_str}\" not found")
        print(Fore.RED + "Aborting.")
        exit()

    profile = profiles[profile_str]
    regex_pattern = profile["match"]
    regex_replace = profile["replace"]
    file_types = profile["ext"]

    if regex_pattern is not None:
        regex_pattern = PatternHelpers.parse_regex(regex_pattern)

    if "dir" in profile:
        directory_list.extend(profile["dir"])

    if "whitelist" in profile:
        blacklist_ext = not profile["whitelist"]

    else:
        blacklist_ext = False

    if debug:
        # print(Fore.CYAN + f"Name: \"{profile_str}\"")
        print(Fore.CYAN + "Name: " + Fore.RESET + profile_str)
        # print(Fore.CYAN + f"Match: \"{regex_pattern}\"")
        print(Fore.CYAN + "Match: " + Fore.RESET + regex_pattern.pattern)
        # print(Fore.CYAN + f"Replace: \"{regex_replace}\"")
        print(Fore.CYAN + "Replace: " + Fore.RESET + regex_replace)
        # print(Fore.CYAN + f"Available extensions: \"{file_types}\"")
        print(Fore.CYAN + "Available extensions: " + Fore.RESET + f"{file_types}")
        # print(Fore.CYAN + f"Whitelist extensions: {not blacklist_ext}")
        print(Fore.CYAN + "Whitelist extensions: " + Fore.RESET + f"{not blacklist_ext}")

    if "dir" in profile:
        print(Fore.CYAN + f"Included directories: " + Fore.RESET + f"{profile['dir']}")

# Begin work.

# Verify and parse match pattern.
regex = regex_pattern

if debug:
    print(Fore.CYAN + "Regex object: " + Fore.RESET + f"{regex}")

for directory in directory_list:
    if directory == "":
        # Skip empty path. Used for profiles which contain the directory.

        if debug:
            print(Fore.CYAN + "Skipping blank directory path.")

        continue

    print(Fore.YELLOW + f"Entering \"{directory}\":")

    p = Path(directory)

    if not os.path.exists(directory):
        print(Fore.RED + "Directory does not exist.")
        continue

    elif not p.is_dir():
        print(Fore.RED + "Skipping, not a directory.")
        continue

    # Gather files.
    # Files which have types specified in the 'file_types' list will be added
    # to the 'files' list. Conversely, if the 'blacklist' switch is active,
    # those files will not be added, but everything else will be added.
    files = []

    if blacklist_ext:
        for file in os.listdir(directory):
            f_obj = Path(os.path.join(directory, file))

        if f_obj.is_file():
            # Remove the leading "."" from the extension.
            f_ext = f_obj.suffix.casefold()[1:]

            if not (f_ext) in file_types:
                print(file)

    else:
        for ext in file_types:
            t_ext = ext

            if not ext.startswith("*."):
                t_ext = "*." + ext

            files.extend(glob(join(directory, t_ext)))

for file in files:
    file_name = Path(file).name

    # Perform a search to see if the file is eligible then do the replacement.
    # This is done not to pollute the console output.
    if regex.search(file_name) is None:
        continue

    new_name = regex.sub(regex_replace, file_name)
    new_path = join(directory, new_name)

    if os.path.exists(new_path):
        if debug:
            print(Fore.RED + f"A file with the name of \"{new_name}\" already exists.")

        else:
            print(Fore.RED + f"A file with the target name already exists.")

        continue

    else:
        print(Fore.RED + f"{file_name}" + Fore.RESET
              + " -> "
              + Fore.GREEN + f"{new_name}")

        # Don't perform the rename if it's a dry run.
        if not dry_run:
            os.rename(file, new_path)
