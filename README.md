# ArgparsePrompt
Wrapper for the built-in Argparse, allowing missing command-line arguments to be filled in by the user via interactive prompts

# Installation
ArgparsePrompt has not yet been published to PYPI, but in the meantime, you can install it using pip+git:
```bash
pip install git+https://github.com/MelbourneGenomics/ArgparsePrompt
```

# Usage

The only public interface of this module is the `PromptParser` class, which is a subclass of Python's 
[ArgumentParser](https://docs.python.org/3/library/argparse.html). Use this class in exactly the same way that you would
use ArgumentParser, except that, if any argument does not have a specified `default` value, and a value is not provided
for it on the commandline, the `PromptParser` will prompt for a value for this argument using `input()`, which is read 
from stdin.

Consider the code below:

```python
from argparse_prompt import PromptParser

parser = PromptParser()
parser.add_argument('--arg', '-a')
print(parser.parse_args())
```

If you run this script with a value for `arg`, the parsing will run as normal:
```
$ python test.py --arg 12
Namespace(something='12')
```

However if you don't specify a value for `arg`, the parser will prompt you for one
```
$ python test.py
(something) 12
Namespace(arg='12')
```

If you provide a `type` argument, this type checking will be applied to the prompted value as well:
```
parser = PromptParser()
parser.add_argument('--arg', '-a', type=int)
print(parser.parse_args())
```
```
$ python test.py
(something) abc
usage: typed_parser.py [-h] [--something SOMETHING]
typed_parser.py: error: argument --arg/-a: invalid <argparse_prompt.Prompt object at 0x7fa0b5f5eeb8> value: ''
$ python test.py
(something) 12
Namespace(arg='12')
```
```
