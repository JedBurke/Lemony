import argparse
from helpers import PatternHelpers


class MatchPatternAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")

        super(MatchPatternAction
              , self
              ).__init__(option_strings
                         , dest
                         , **kwargs
                         )

    def __call__(self, parser, namespace, values, option_string=None):
        values = PatternHelpers.parse_regex(values)
        setattr(namespace, self.dest, values)


class ParseArguments():
    def __init__(self):
        return
