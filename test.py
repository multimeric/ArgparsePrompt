import unittest
import subprocess
from pathlib import Path
import sys


class TestParser(unittest.TestCase):
    base = Path('test').resolve()

    def setUp(self):
        self.python = sys.executable

    def run_script(self, path: str, stdin: str = ''):
        """
        Runs the python file with the current python interpreter, with the given stdin
        :param path: Path to the python file, relative to the test/ directory
        :param stdin: The stdin to pipe into the python process
        :returns The return code from the child process
        """
        proc = subprocess.Popen(
            [self.python, self.base / path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        proc.communicate(stdin.encode())
        return proc.poll()

    def test_parser(self):
        """Test a basic parser with no type argument"""
        self.assertEqual(self.run_script('parser.py', stdin='abc'), 0)

    def test_type_parser(self):
        """Test a parser with a type argument. Check that it fails when it should and succeeds when it should"""
        self.assertNotEqual(self.run_script('typed_parser.py', stdin='abc'), 0)
        self.assertEqual(self.run_script('typed_parser.py', stdin='123'), 0)
