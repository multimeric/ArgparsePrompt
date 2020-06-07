#!/usr/bin/env python3
from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name="argparse_prompt",
    long_description=long_description,
    version="0.0.5",
    py_modules=['argparse_prompt'],
    test_suite="test",
    license="GPL",
    author="Michael Milton",
    author_email="michael.r.milton@gmail.com",
    description="Wrapper for the built-in Argparse, allowing missing command-line arguments to be filled in by the user via interactive prompts",
    keywords="argparse prompt interactive argument",
    url="https://github.com/MelbourneGenomics/ArgparsePrompt",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: User Interfaces',
        'Programming Language :: Python :: 3 :: Only'
    ],
    long_description_content_type='text/markdown'
)
