from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name="argparse_prompt",
    long_description=long_description,
    version="0.0.2",
    py_modules=['argparse_prompt'],
    test_suite="test",
    license="GPL",
    author="Michael Milton",
    author_email="michael.r.milton@gmail.com",
    description="Wrapper for the built-in Argparse, allowing missing command-line arguments to be filled in by the user via interactive prompts",
    keywords="argparse prompt interactive argument",
    url="https://github.com/MelbourneGenomics/ArgparsePrompt"
)
