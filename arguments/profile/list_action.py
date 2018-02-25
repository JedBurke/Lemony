import argparse
import json
from helpers.file import FileHelpers
from helpers.user import UserHelpers

class ListAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")

        super(ListAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        profiles = []

        sys_profiles = UserHelpers.get_profiles_path()
        user_profiles = UserHelpers.get_user_profiles_path()
        
        if sys_profiles.exists():
            self.print_profiles("System", sys_profiles, True)

        if user_profiles.exists():
            self.print_profiles("User", user_profiles)
            

    def print_profiles(self, profile_type, path, new_line=False):
        profile_list = json.loads(FileHelpers.read_file(path))

        if len(profile_list) > 0:
            print(f"{profile_type} Profiles:")

            for profile in profile_list:
                print("    " + profile)

            if new_line:
                print()
