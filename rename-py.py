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

VERSION = "0.1"
PATH_SEPARATOR = ";"

debug = False
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

args = vars(parser.parse_args())

if args["debug"]:
	debug = True

if debug:
	print(args["args"])

if args["dry_run"]:
	dry_run = True

	if debug:
		print(f"Dry Run: {dry_run}")

if args["version"]:
	print(f"Pyren version: {VERSION}")

if args["match_pattern"] is not None:
	regex_pattern = args["match_pattern"]

	if debug:
		print(f"Match Pattern: {regex_pattern}")

if args["replace_pattern"] is not None:
	regex_replace = args["replace_pattern"]
	
	if debug:
		print(f"Replace Pattern: {regex_replace}")

if args["profile"] is not None:
	script_path = path.join(sys.path[0], "rename-profiles.json")

	with open(script_path, "r") as profile_content_file:
		profile_content = profile_content_file.read()

	profiles = json.loads(profile_content)
	profile_str = args["profile"]

	if not profile_str in profiles:
		print(f"Profile \"{profile_str}\" not found")
		print("Aborting.")
		exit()

	profile = profiles[profile_str]
	regex_pattern = profile["match"]
	regex_replace = profile["replace"]
	file_types = profile["ext"]

	if debug:
		print(f"Name: \"{profile_str}\"")
		print(f"Match: \"{regex_pattern}\"")
		print(f"Replace: \"{regex_replace}\"")
		print(f"Available extensions: \"{file_types}\"")

	exit()

sub_ext = ["*.srt", "*.ass", "*.mkv", "*.mp4"]

arg_count = len(argv)

if arg_count < 2:
	print("At least one directory must be specified. Exiting…")
	exit()

for directory in args["args"].split(PATH_SEPARATOR):
	print(f"Entering \"{directory}\"")

	p = Path(directory)

	if not p.is_dir():
		print(f"Argument is not a directory")
		continue

	# for ext in sub_ext:
	# 	glob.glob(directory.extend(ext))
	#  = glob.glob(directory + "\*.+(srt|ass)")
	# for subFile in subFiles:
	# 	print(subFile)

	sub_files = []
	for ext in sub_ext:
		sub_files.extend(glob(join(directory, ext)))

	# print(sub_files)
	for file in sub_files:
		file_name = Path(file).name

		if debug:
			print(join(directory, re.sub(regex_pattern, regex_replace, file_name)))

		# m = re.match(regex_pattern, file_name)
		# if m is not None:
		# 	print(m.group(1) + " " + m.group(2) + m.group(3))

		# else:
		# 	print("No match")
