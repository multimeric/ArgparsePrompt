import argparse
import os
import sys


class PromptParser(argparse.ArgumentParser):
    """
    Extends ArgumentParser to allow any unspecified arguments to be input dynamically on the command line
    """

    def add_argument(self, *args, prompt=True, **kwargs):
        """
        :param args:
        :param prompt: False if we never want to prompt the user for this argument
        :param kwargs:
        :return:
        """
        if prompt and kwargs.get('action') != 'help' and not os.getenv('ARGPARSE_PROMPT_AUTO'):
            # Wrap the Prompt type around the type the user wants
            type = Prompt(help=kwargs.get('help'), type=kwargs.get('type'), default=kwargs.get('default'))

            # Remove the old type so we can replace it with our own
            if 'type' in kwargs:
                del kwargs['type']
            if 'default' in kwargs:
                del kwargs['default']

            # Delegate to the parent class. Default must be '' in order to get the type function to be called
            action = super().add_argument(*args, type=type, default='', **kwargs)

            # Set the argument name, now that the parser has parsed it
            type.name = action.dest

        else:
            super().add_argument(*args, **kwargs)


class Prompt:
    """A class the pretends to be a function so that it can be used as the 'type' argument for the ArgumentParser"""

    def __init__(self, name=None, help=None, type=None, default=None):
        """
        Creates a new prompt validator
        :param name: The identifier for the variable
        :param help: The help string to give the user when prompting
        :param type: The validation function to use on the prompted data
        """
        self.type = type if type is not None else lambda x: x
        self.name = name
        self.help = help
        self.default = default

    def __call__(self, val):
        default_str = '' if self.default is None else f'({self.default}) '
        help_str = '' if self.help is None else f': {self.help}'

        try:
            # If the user provided no value for this argument, prompt them for it
            if val == '':
                print('{}{}\n> {}'.format(self.name, help_str, default_str), end='', file=sys.stderr)
                newval = input()

                # If they just hit enter, they want the default value
                if newval == '':
                    return self.type(self.default)
                else:
                    return self.type(newval)

            return self.type(val)

        except BaseException:
            print(f'Argument "{self.name}" was given a value not of type {self.type}', file=sys.stderr)
            exit(1)
