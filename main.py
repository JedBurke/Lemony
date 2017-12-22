import argparse
from datetime import date
import logging
from logging import Logger
from arguments.argument_factory import ArgumentFactory

from arguments.rename.main import RenameArgument
from arguments.profile.main import ProfileArgument

from project_globals import Globals
from arguments.user_init import InitializeUserConfig

# This is a proof-of-concept where the CLI arguments have been
# decoupled from the main part of the application. It's far from
# done, but in the future, the arguments will be taken from the
# "arguments" directory and be dynamically consumed.

date = date.today().strftime("%Y-%m-%d")
log_path = f"settings/logs/log-{date}.txt"

logging.basicConfig(
    format='%(asctime)s - %(levelname)s > %(message)s',
    filename=log_path,
    level=logging.DEBUG
)

parser = ArgumentFactory.initiate_parser(
    description=f"{Globals.PRODUCT} facilitates the renaming of \
    files with the use of regular expressions."
)

subparser = parser.add_subparsers()

# parser.add_argument("args")

parser.add_argument(
    "--version",
    action="version",
    version=Globals.get_version_str(),
    help=f"display {Globals.PRODUCT_POSS} version"
)

# parser.add_argument(
#     "--init-user-config",
#     action=InitializeUserConfig,
#     help="setup an empty user configuration environment"
# )

# ArgRename largely consists of the original renaming logic which
# was present in the application. In the future, ArgRename won't be
# instantized as it is now, but via a plugin interface.

logging.info("Load argument - Rename")

#
RenameArgument(subparser)
ProfileArgument(subparser)

# Prefer having the extension return its parser over handing over the
# parser to it.

# subparser.add_parser(ArgRename().register_parser())

args = parser.parse_args()

if "func" in args:
    args.func(args)

# Usage:
# > main.py rename "" --profile "goldenboy" -n --verbose
# Be sure to use the dry run switch as the logic may still be
# unstable and have various bugs.
