import unittest
from helpers.users import UserHelpers

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.print_vars = False
        return

    def test_get_user_directory(self):
        result = UserHelpers.get_user_directory()

        self.print_result(result, "User Directory")

        self.assertIsNotNone(result)

    def test_get_user_profiles_path(self):
        result = UserHelpers.get_user_profiles_path()

        self.print_result(result, "User Profiles")

        self.assertIsNotNone(result)

    def test_get_profiles_path(self):
        result = UserHelpers.get_profiles_path()

        self.print_result(result, "System Profiles Path")

        self.assertIsNotNone(result)

    def print_result(self, result, prefix=None):
        if self.print_vars:
            if prefix == None:
                print(result)

            else:
                print(f"{prefix}: {result}")

if __name__ == '__main__':
    unittest.main()
