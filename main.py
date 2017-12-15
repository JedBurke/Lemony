from datetime import date
import logging
from logging import Logger
from arguments.argument_factory import ArgumentFactory
from arguments.rename.main import ArgRename

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
    description="Rename files"
)

subparser = parser.add_subparsers()

# ArgRename largely consists of the original renaming logic which
# was present in the application. In the future, ArgRename won't be
# instantized as it is now, but via a plugin interface.

ArgRename(subparser)

args = parser.parse_args()
args.func(args)

# Usage:
# > main.py rename "" --profile "goldenboy" -n --verbose
# Be sure to use the dry run switch as the logic may still be
# unstable and have various bugs.
