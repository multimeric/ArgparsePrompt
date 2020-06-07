import os
from unittest import TestCase, mock
from unittest.mock import patch

from argparse_prompt import PromptParser


class TestParser(TestCase):
    @mock.patch('builtins.input')
    def test_basic_parser(self, input_mock):
        """Test a basic parser with no type argument"""
        input_mock.return_value = 'abc'
        parser = PromptParser()
        parser.add_argument('--argument', '-a', help='An argument you could provide', default='foo')
        args = parser.parse_args([])
        self.assertEqual(args.argument, 'abc')

    @mock.patch('builtins.input')
    def test_default_parser(self, input_mock):
        """Test a basic parser with a default value"""
        input_mock.return_value = ''
        parser = PromptParser()
        parser.add_argument('--argument', '-a', help='An argument you could provide', default='foo')
        args = parser.parse_args([])
        self.assertEqual(args.argument, 'foo')

    @patch.dict(os.environ,{'ARGPARSE_PROMPT_AUTO':'True'})
    def test_auto_parser(self):
        """Test a basic parser when the enviroment variable is set to disable prompts"""
        parser = PromptParser()
        parser.add_argument('--argument', '-a', help='An argument you could provide', default='foo')
        args = parser.parse_args([])
        self.assertEqual(args.argument, 'foo')

    @mock.patch('builtins.input')
    def test_invalid_type(self, input_mock):
        """Test a parser with a type argument. Check that it fails when the type is wrong"""
        input_mock.return_value = 'abc'
        with self.assertRaises(SystemExit):
            parser = PromptParser()
            parser.add_argument('--argument', '-a', help='An argument you could provide',
                                type=int)
            args = parser.parse_args([])
        input_mock.assert_called()

    @mock.patch('builtins.input')
    def test_valid_type(self, input_mock):
        """Test a parser with a type argument. Check that it succeeds when the type is correct"""
        input_mock.return_value = '123'
        parser = PromptParser()
        parser.add_argument('--argument', '-a', help='An argument you could provide',
                            type=int)
        args = parser.parse_args([])
        self.assertEqual(args.argument, 123)
        input_mock.assert_called()

    @mock.patch('getpass.getpass')
    def test_secure_parser(self, getpass_mock):
        """Test a secure parser, which shouldn't echo the user's input to stdout"""
        getpass_mock.return_value = 'abc'
        parser = PromptParser()
        parser.add_argument('--argument', '-a', help='An argument you could provide', secure=True, default='foo')
        args = parser.parse_args([])
        self.assertEqual(args.argument, 'abc')
        getpass_mock.assert_called()


    @mock.patch('builtins.input')
    def test_mismatched_default(self, input_mock):
        """Test a parser which has a default which isn't the same type as the type"""
        input_mock.return_value = ''
        parser = PromptParser()
        parser.add_argument('--argument', type=str, default=None)
        args = parser.parse_args([])
        self.assertEqual(args.argument, None)
        input_mock.assert_called()
