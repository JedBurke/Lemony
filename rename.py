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

init(autoreset=True)

VERSION = "0.3.0"

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

regex_pattern = ""
regex_replace = ""
file_types = ["*"]

parser = argparse.ArgumentParser(description="Rename files")
parser.add_argument("args")
parser.add_argument("-n", "--dry-run", action="store_true")
parser.add_argument("--version", action="store_true")
parser.add_argument("--debug", action="store_true")
parser.add_argument("-m", "--match-pattern", default=None)
parser.add_argument("-r", "--replace-pattern", default=None)
parser.add_argument("-p", "--profile", default=None)
parser.add_argument("-x", "--ext", default=None)
parser.add_argument("--blacklist", action="store_true")

# Todo: Implement
# --get-profile prints the profile contents. Works as --debug, but only for the profile and 
# exits once returned.
parser.add_argument("--get-profile")

# Todo: Implement subcommands for profile settings.
# --set-profile "subs" -m "pattern" -r "replacement" --ext "*.srt,*.ass"

args = parser.parse_args()

if args.debug:
  debug = True

if debug:
  print(args.args)

if args.dry_run:
  dry_run = True

  if debug:
    print(Fore.CYAN + f"Dry Run: {dry_run}")

if args.version:
  print(f"Pyren version: {VERSION}")

if args.match_pattern is not None:
  regex_pattern = args.match_pattern

  if debug:
    print(Fore.CYAN + f"Match Pattern: {regex_pattern}")

if args.replace_pattern is not None:
  regex_replace = args.replace_pattern
  
  if debug:
    print(Fore.CYAN + f"Replace Pattern: {regex_replace}")

if args.ext is not None:
  WHITESPACE_SEPARATOR = " "
  ext_delimiter = EXTENSION_SEPARATOR
  
  if EXTENSION_SEPARATOR not in args.ext:
    if PATH_SEPARATOR not in args.ext:
      if WHITESPACE_SEPARATOR in args.ext:
        ext_delimiter = WHITESPACE_SEPARATOR
    else:
      ext_delimiter = PATH_SEPARATOR

  file_types = args.ext.split(ext_delimiter)

  if debug:
    print(Fore.CYAN + f"Extension List: {file_types}")

if args.profile is not None:
  # Gets the profile path relative to the script.
  profile_path = path.join(sys.path[0], PROFILES_FILE_NAME)

  if os.path.exists(profile_path):
    with open(profile_path, encoding="utf-8", mode="r") as profile_content_file:
      profile_content = profile_content_file.read()

    profiles = json.loads(profile_content)
  
  else:
    print(Fore.RED + "The profile configuration file cannot be found.")
    exit()

  user_config_path = path.join(path.expanduser(f"~/{USER_DATA_DIR_NAME}"), PROFILES_FILE_NAME)
  user_config = Path(user_config_path)
  if user_config.exists():
    # Instead of creating the directory, check if it exists and include it should it.
    with open(user_config_path, encoding="utf-8", mode="r") as profile_content_file:
      profile_content = profile_content_file.read()

    user_profiles = json.loads(profile_content)

    if user_profiles is not None:
      profiles.update(user_profiles)


    profile_str = args.profile

  if not profile_str in profiles:
    print(Fore.RED + f"Profile \"{profile_str}\" not found")
    print(Fore.RED + "Aborting.")
    exit()

  profile = profiles[profile_str]
  regex_pattern = profile["match"]
  regex_replace = profile["replace"]
  file_types = profile["ext"]
  

  if debug:
    print(Fore.CYAN + f"Name: \"{profile_str}\"")
    print(Fore.CYAN + f"Match: \"{regex_pattern}\"")
    print(Fore.CYAN + f"Replace: \"{regex_replace}\"")
    print(Fore.CYAN + f"Available extensions: \"{file_types}\"")

for directory in args.args.split(PATH_SEPARATOR):
  print(Fore.CYAN + f"Entering \"{directory}\".")

  p = Path(directory)

  if not os.path.exists(directory):
    print(Fore.RED + "Directory does not exist.")
    continue

  elif not p.is_dir():
    print(Fore.RED + "Skipping, not a directory.")
    continue

  files = []
  for ext in file_types:
    files.extend(glob(join(directory, ext)))

  for file in files:
    file_name = Path(file).name

    # Todo: Compile regular expressions.

    # Perform a search to see if the file is eligible then do the replacement.
    # This is done not to pollute the console output.
    if re.search(regex_pattern, file_name) == None:
      continue

    new_name = re.sub(regex_pattern, regex_replace, file_name)
    new_path = join(directory, new_name)

    if os.path.exists(new_path):
      if debug:
        print(Fore.RED + f"A file with the name of \"{new_name}\" already exists.")
      
      else:
        print(Fore.RED + f"A file with the target name already exists.")
      
      continue

    else:
      if debug:
        print(Fore.RED + f"{file_name}" + Fore.RESET + " -> " + Fore.GREEN + f"{new_name}")

      # Don't perform the rename if it's a dry run.
      if not dry_run:
          os.rename(file, new_path)
