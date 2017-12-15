from colorama import init, Fore, Back, Style

"""
A collection of functions which presents errors and general
information to the user. All functions log the parameters
passed to them.
"""
class LogHelpers:
    initialized = False

    def initialize():
        init(autoreset=True)

    def print_error(error, log=True):
        if not initialized:
            initialize()

        print(Fore.RED + error)

        if log:
            # log
            return
 
