import unittest
from argparse import Namespace

import pytest
import censoror

class TestCensorText(unittest.TestCase):
    def test_checkStopWord(self):
        """Tests the checkForStopWord function for various inputs."""
        self.assertTrue(censoror.checkForStopWord("the"))  # Stop word
        self.assertTrue(censoror.checkForStopWord("Graduate"))  # Custom word to exclude
        self.assertFalse(censoror.checkForStopWord("dragon"))  # Not a stop word or custom word

    def test_preprocess_text(self):
        """Tests the censoror.preprocess_text function for punctuation removal."""
        text = "This is some text, with punctuation!"
        expected_output = "This is some text  with punctuation "
        self.assertEqual(censoror.preprocess_text(text), expected_output)

    def test_mask_phone_numbers(self):
        """Tests the mask_phone_numbers function for different phone number formats."""
        text = "My phone number is 503 464 3926 ."
        masked, masked_text = censoror.mask_phone_numbers(text)
        self.assertTrue(masked)  # Phone number was masked

        text = "123 456 7890 ext . 345"
        masked, masked_text = censoror.mask_phone_numbers(text)
        print(masked_text)
        self.assertTrue(masked)

        text = "No phone numbers here."
        masked, masked_text = censoror.mask_phone_numbers(text)
        self.assertFalse(masked)  # No phone number found
        self.assertEqual(masked_text, text)
