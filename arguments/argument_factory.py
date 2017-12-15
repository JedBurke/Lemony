import argparse

class ArgumentFactory:
    def __init__(self):
        return

    """
    Readies the environemt for agrument parsing.
    """
    def initiate_parser(description):
        parser = argparse.ArgumentParser(
            description=description
        )

        return parser