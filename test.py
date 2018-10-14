import os
import unittest
import subprocess
from pathlib import Path
import sys


class TestParser(unittest.TestCase):
    base = Path('test').resolve()

    def setUp(self):
        self.python = sys.executable

    def run_script(self, path: str, stdin: str = '', popen_args:dict = {}):
        """
        Runs the python file with the current python interpreter, with the given stdin
        :param path: Path to the python file, relative to the test/ directory
        :param stdin: The stdin to pipe into the python process
        :returns A tuple containing the return code from the child process, and stdout as a byte string
        """
        proc = subprocess.Popen(
            [self.python, self.base / path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            **popen_args
        )
        stdout, stderr = proc.communicate(stdin.encode())
        exitcode = proc.poll()
        return exitcode, stdout.decode().strip(), stderr.decode().strip()

    def test_basic_parser(self):
        """Test a basic parser with no type argument"""
        exitcode, stdout, stderr = self.run_script('default_parser.py', stdin='abc')
        self.assertEqual(exitcode, 0)
        self.assertEqual(stdout, 'abc')

    def test_default_parser(self):
        """Test a basic parser with a default value"""
        exitcode, stdout, stderr = self.run_script('default_parser.py', stdin='\n')
        self.assertEqual(exitcode, 0)
        self.assertEqual(stdout, 'foo')

    def test_auto_parser(self):
        """Test a basic parser when the enviroment variable is set to disable prompts"""
        newenv = os.environ.copy()
        newenv['ARGPARSE_PROMPT_AUTO'] = 'True'
        exitcode, stdout, stderr = self.run_script('default_parser.py', popen_args=dict(env=newenv))
        self.assertEqual(exitcode, 0)
        self.assertEqual(stdout, 'foo')

    def test_invalid_type(self):
        """Test a parser with a type argument. Check that it fails when the type is wrong"""
        exitcode, stdout, stderr = self.run_script('typed_parser.py', stdin='abc')
        self.assertNotEqual(exitcode, 0)

    def test_valid_type(self):
        """Test a parser with a type argument. Check that it succeeds when the type is correct"""
        stdin = '123'
        exitcode, stdout, stderr = self.run_script('typed_parser.py', stdin=stdin)
        self.assertEqual(exitcode, 0)
        self.assertEqual(stdout, stdin)

    def test_secure_parser(self):
        """Test a secure parser, which shouldn't echo the user's input to stdout"""
        exitcode, stdout, stderr = self.run_script('secure_parser.py', stdin='abc')
        self.assertEqual(exitcode, 0)
        self.assertEqual(stdout, 'abc')
