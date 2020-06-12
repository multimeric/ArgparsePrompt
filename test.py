import os
from unittest import TestCase, mock
from unittest.mock import patch
import pytest

from argparse_prompt import PromptParser


def mock_input(ret_val):
    """
    Returns a function that acts like ``input()``, but with a fixed return value (``ret_val``)
    """

    def input(arg):
        print(arg)
        return ret_val

    return input


@mock.patch("builtins.input")
def test_basic_parser(input_mock, capsys):
    """Test a basic parser with no type argument"""
    # Mock the input function
    input_mock.side_effect = mock_input("abc")

    parser = PromptParser()
    parser.add_argument(
        "--argument", "-a", help="An argument you could provide", default="foo"
    )
    args = parser.parse_args([])

    # If the user inputs "abc", that should be the value of the argument
    assert args.argument == "abc"

    # The default value "foo" should be shown to the user
    captured = capsys.readouterr()
    assert "foo" in captured.out


@mock.patch("builtins.input")
def test_no_default(input_mock, capsys, monkeypatch):
    """If a flag has no default, the prompt should still say ``None``"""
    # Mock the input function
    input_mock.side_effect = mock_input("abc")

    # Create the parser
    parser = PromptParser()
    parser.add_argument("--argument", "-a", help="An argument you could provide")
    args = parser.parse_args([])

    captured = capsys.readouterr()
    assert "None" in captured.out


@mock.patch("builtins.input")
def test_default_parser(input_mock):
    """Test a basic parser with a default value"""
    input_mock.side_effect = mock_input("")

    parser = PromptParser()
    parser.add_argument(
        "--argument", "-a", help="An argument you could provide", default="foo"
    )
    args = parser.parse_args([])
    assert args.argument == "foo"


@patch.dict(os.environ, {"ARGPARSE_PROMPT_AUTO": "True"})
def test_auto_parser():
    """Test a basic parser when the enviroment variable is set to disable prompts"""
    parser = PromptParser()
    parser.add_argument(
        "--argument", "-a", help="An argument you could provide", default="foo"
    )
    args = parser.parse_args([])
    assert args.argument == "foo"


@mock.patch("builtins.input")
def test_invalid_type(input_mock):
    """Test a parser with a type argument. Check that it fails when the type is wrong"""
    input_mock.side_effect = mock_input("abc")

    with pytest.raises(SystemExit):
        parser = PromptParser()
        parser.add_argument(
            "--argument", "-a", help="An argument you could provide", type=int
        )
        args = parser.parse_args([])
    input_mock.assert_called()


@mock.patch("builtins.input")
def test_valid_type(input_mock):
    """Test a parser with a type argument. Check that it succeeds when the type is correct"""
    input_mock.side_effect = mock_input("123")

    parser = PromptParser()
    parser.add_argument(
        "--argument", "-a", help="An argument you could provide", type=int
    )
    args = parser.parse_args([])
    assert args.argument == 123
    input_mock.assert_called()


@mock.patch("getpass.getpass")
def test_secure_parser(getpass_mock):
    """Test a secure parser, which shouldn't echo the user's input to stdout"""
    getpass_mock.return_value = "abc"
    parser = PromptParser()
    parser.add_argument(
        "--argument",
        "-a",
        help="An argument you could provide",
        secure=True,
        default="foo",
    )
    args = parser.parse_args([])
    assert args.argument == "abc"
    getpass_mock.assert_called()


@mock.patch("builtins.input")
def test_mismatched_default(input_mock):
    """Test a parser which has a default which isn't the same type as the type"""
    input_mock.return_value = ""
    parser = PromptParser()
    parser.add_argument("--argument", type=str, default=None)
    args = parser.parse_args([])
    assert args.argument is None
    input_mock.assert_called()
