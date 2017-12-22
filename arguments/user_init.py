import argparse
import os
from helpers.user import UserHelpers

class InitializeUserConfig(argparse.Action):
    """docstring for InitializeUserConfig"""
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")

        super(InitializeUserConfig, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        user_dir = UserHelpers.get_user_directory()

        if user_dir.exists():
            print(f"User directory already exists at:\n    { user_dir }")
