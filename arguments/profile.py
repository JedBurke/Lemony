import argparse

class ProfileSubCommand:
    subparser = None

    def __init__(self, subparser):
        self.subparser = subparser
        self.define_arguments();

    def define_arguments(self):
        self.subparser.add_argument(
            "-l",
            "ls",
            help="list the profiles"
        )

        self.subparser.add_argument(
            "--get-profile",
            help="Return a profile by its name"
        )

        self.subparser.add_argument(
            "-a",
            "--add",
            help="Add a profile"
        )

    def get_subcommand(self):
        return
