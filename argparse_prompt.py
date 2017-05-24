import argparse


class PromptParser(argparse.ArgumentParser):
    """
    Extends ArgumentParser to allow any unspecified arguments to be input dynamically on the command line
    """

    def add_argument(self, *args, **kwargs):
        # If they provided a default value, we don't need to prompt the user
        if 'default' in kwargs:
            super().add_argument(*args, **kwargs)

        else:
            # Wrap the Prompt type around the type the user wants. We don't yet know the argument name, so we pass None
            type = Prompt(None, help=kwargs.get('help'), type=kwargs.get('type'))

            # Remove the old type so we can replace it with our own
            if 'type' in kwargs:
                del kwargs['type']

            # Delegate to the parent class. Default must be '' in order to get the type function to be called
            action = super().add_argument(*args, type=type, default='', **kwargs)

            # Set the argument name, now that the parser has parsed it
            type.name = action.dest


class Prompt:
    """A class the pretends to be a function so that it can be used as the 'type' argument for the ArgumentParser"""

    def __init__(self, name=None, help='', type=None):
        """
        Creates a new prompt validator
        :param name: The identifier for the variable
        :param help: The help string to give the user when prompting
        :param type: The validation function to use on the prompted data
        """
        self.type = type if type is not None else lambda x: x
        self.name = name
        self.help = (': ' + help) if help else ''

    def __call__(self, val):
        if val == '':
            newval = input('({}{}) '.format(self.name, self.help))
            return self.type(newval)

        return self.type(val)
