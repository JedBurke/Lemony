import argparse
from ..argument_base import ArgumentBase
from .list_action import ListAction

class ProfileArgument(ArgumentBase):
    
    def __init__(self, parser):
        ArgumentBase.__init__(self)

        self.parser = parser.add_parser(
            "profile",
            help="add, delete, list, and edit pattern profiles"
        )

        self.register(self.parser)

    def args_entry(self, args):
        return

    def register(self, parser):
        parser.add_argument(
            "ls",
            action=ListAction,
            help="list profiles by name",
        )

        parser.add_argument(
            "--get-profile",
            help="return a profile by its name"
        )

        parser.add_argument(
            "-a",
            "--add",
            help="add a profile"
        )

        parser.set_defaults(func=self.args_entry)

    def get_subcommand(self):
        return
