# ArgparsePrompt
ArgparsePrompt is a wrapper for the built-in Argparse, allowing missing command-line arguments to be filled in by the
user via interactive prompts

# Installation
ArgparsePrompt can be installed using pip:
```bash
pip install argparse_prompt
```

# Usage

## Basic Usage
The only public interface of this module is the `PromptParser` class, which is a subclass of Python's 
[ArgumentParser](https://docs.python.org/3/library/argparse.html). Use this class in exactly the same way that you would
use ArgumentParser, except that, if any argument does not have a specified `default` value, and a value is not provided
for it on the commandline, the `PromptParser` will prompt for a value for this argument using `input()`, which is read 
from stdin.

Consider the code below (taken from one of the unit tests):

```python
from argparse_prompt import PromptParser

parser = PromptParser()
parser.add_argument('--argument', '-a', help='An argument you could provide', default='foo')
print(parser.parse_args().argument)
```

If you run this script with a value for `argument`, the parsing will run as normal:
```
$ python test/default_parser.py --argument 12
12
```

However if you don't specify a value for `arg`, the parser will prompt you for one
```
$ python test/default_parser.py
argument: An argument you could provide
> (foo) car
car
```

## Default Values
Since this argument has a default value, you can also just hit enter and this value will be used automatically:
```
python test/default_parser.py
argument: An argument you could provide
> (foo) 
foo
```

## Type Checking
You can also specify a type for the argument in the normal way:

```python
from argparse_prompt import PromptParser

parser = PromptParser()
parser.add_argument('--argument', '-a', help='An argument you could provide', type=int)
print(parser.parse_args().argument)
```

If you do, this type checking will be used for the value you enter at the prompt:
```
$ python test/typed_parser.py  
argument: An argument you could provide
abc
Argument "argument" was given a value not of type <class 'int'>
```

## Secure Values
For arguments that need to be secure, such as passwords, secret keys etc, you can use `secure=True` when defining your
argument. This will cause whatever the user inputs for that field to be hidden from the terminal, in the same way that 
`git`, or `ssh` hides the password input.

For example:
```python
parser.add_argument('--password', '-p', help='A very secret password', secure=True)
```


## Situationally Disabling the Prompt
If you use the `prompt` argument to `add_argument`, parsing will be disabled:

```python
parser.add_argument('--argument', '-a', help='An argument you could provide', default='foo', prompt=False)
```

Also, if you want to disable all prompting (for an automated script, for example), just set the `ARGPARSE_PROMPT_AUTO` to
a truthy value:
```bash
ARGPARSE_PROMPT_AUTO=1 python test/default_parser.py
```
