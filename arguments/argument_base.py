import argparse

class ArgumentBase:
    def __init__(self):
        return

    @property
    def shortcode(self):
        return self._shortcode
    @shortcode.setter
    def shortcode(self, value):
        if len(value) > 0 and value[0] != "-":
            value = "-" + value

        self._shortcode = value
    
    @property
    def argument(self):
        return self._argument
    @argument.setter
    def argument(self, value):
        self._argument = value
    
    def register_parser(self, argument, help):
        self.parser.add_parser(argument, help=help)

    def register_argument(self, longcode, help):
        self.register_argument(None, longcode, help, None)

    def register_argument(self, shortcode, longcode, help, action=None):
        self.parser.add_argument(
            shortcode,
            longcode,
            action=action,
            help=help
        )

    def register(self):
        return

    def debug(self):
        if self.shortcode:
            print(self.shortcode)

        if self.argument:
            print(self.argument)
