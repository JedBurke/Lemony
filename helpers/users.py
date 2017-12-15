from constants import Constants
import sys
import os
from os import path
from os.path import join
from pathlib import Path

"""
A collection of static functions which provide access to the user's
settings directory and profile paths.

The class is a catch-all one for directories pertaining to the user.
As such, the general profile directory is available from this class
as well.
"""
class UserHelpers:
    """
    Gets the path to the directory which stores the user's profiles
    and settings.

    Returns:
        Path-object
    """
    def get_user_directory():        
        user_dir = path.expanduser(f"~/{Constants.USER_DATA_DIR_NAME}")
        norm_user_dir = path.normpath(user_dir)

        return norm_user_dir

    """
    Gets the path to the file which stores the user's rename
    profiles.

    Returns:
        Path-object
    """
    def get_user_profiles_path():
        user_profiles_path = path.join(
            UserHelpers.get_user_directory(),
            Constants.PROFILES_FILE_NAME
        )

        norm_user_profiles_path = path.normpath(user_profiles_path)

        return Path(norm_user_profiles_path)

    """
    Gets the path to the directory where the generally-available profiles
    and settings are stored.
    """
    def get_system_directory():
        system_path = path.join(
            os.getcwd(),
            Constants.SYSTEM_DATA_DIR_NAME
        )

        return Path(system_path)

    """
    Returns the path to the file which stores the generally-available
    profiles.

    Returns:
        Path-object
    """
    def get_profiles_path():
        profiles_path = path.join(
            UserHelpers.get_system_directory(),
            Constants.PROFILES_FILE_NAME
        )

        norm_profiles_path = path.normpath(profiles_path)

        return Path(norm_profiles_path)

    """
    Returns the path to the user's log file.

    Returns:
        Path-object
    """
    def get_user_log_path():
        return

    """
    Returns the path to the system's log file.

    Returns:
        Path-object
    """
    def get_log_path():
        return
