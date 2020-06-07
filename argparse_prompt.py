import argparse
import os
import sys
import getpass


class PromptParser(argparse.ArgumentParser):
    """
    Extends ArgumentParser to allow any unspecified arguments to be input dynamically on the command line
    """

    def add_argument(self, *args, prompt=True, secure=False, **kwargs):
        """
        For all unlisted arguments, refer to the parent class
        :param prompt: False if we never want to prompt the user for this argument
        :param secure: True if this argument contains sensitive information, and the input should not be shown on the
            command line while it's input.
        """
        if prompt and kwargs.get('action') != 'help' and not os.getenv('ARGPARSE_PROMPT_AUTO'):
            # Wrap the Prompt type around the type the user wants
            type = Prompt(help=kwargs.get('help'), type=kwargs.get('type'), secure=secure, default=kwargs.get('default'))

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
    """
    A class the pretends to be a function so that it can be used as the 'type' argument for the ArgumentParser
    """

    def __init__(self, name=None, help=None, type=None, default=None, secure=False):
        """
        Creates a new prompt validator
        :param name: The identifier for the variable
        :param help: The help string to give the user when prompting
        :param type: The validation function to use on the prompted data
        :param secure: True if this argument contains sensitive information, and the input should not be shown on the
            command line while it's input.
        """
        self.type = type if type is not None else lambda x: x
        self.name = name
        self.help = help
        self.default = default
        self.secure = secure

    def __call__(self, val):
        default_str = '' if self.default is None else f'({self.default}) '
        help_str = '' if self.help is None else f': {self.help}'

        try:
            # If the user provided no value for this argument, prompt them for it
            if val == '':
                prompt = '{}{}\n> {}'.format(self.name, help_str, default_str)

                newval = getpass.getpass(prompt=prompt) \
                    if self.secure else input(prompt)

                # If they just hit enter, they want the default value
                if newval == '':
                    newval = self.default

                # According to the argparse docs, if the default is a string we should convert it, but otherwise
                # we return it verbatim: https://docs.python.org/3/library/argparse.html#default
                if isinstance(newval, str):
                    return self.type(newval)
                else:
                    return newval

            return self.type(val)

        except BaseException:
            print(f'Argument "{self.name}" was given a value not of type {self.type}', file=sys.stderr)
            exit(1)
