from argparse import Namespace
import unittest
import censoror
import pytest


def test_parse_args():
    # Prepare a list of command-line arguments for testing
    test_args = ["--input", "input_pattern", "--output", "output_directory", "--phones", "--stats", "stdout"]

    # Call the parse_args function with the test arguments
    with unittest.TestCase().assertRaises(SystemExit) as context:
        parsed_args = censoror.parse_args()
