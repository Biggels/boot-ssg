import unittest

from generation import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_h1_returns_title(self):
        self.assertEqual(extract_title("# A Simple Story"), "A Simple Story")

    def test_multiple_h1_returns_first(self):
        self.assertEqual(
            extract_title("# A Simple Story\n# A Simpler Story"), "A Simple Story"
        )

    def test_h1_on_second_line_returns_title(self):
        self.assertEqual(
            extract_title(
                "I wonder what I should call my story...how about\n# A Simple Story"
            ),
            "A Simple Story",
        )

    def test_None_input_raises_ValueError(self):
        with self.assertRaises(ValueError):
            extract_title(None)  # pyright: ignore[reportArgumentType]

    def test_empty_input_raises_ValueError(self):
        with self.assertRaises(ValueError):
            extract_title("")

    def test_whitespace_input_raises_ValueError(self):
        with self.assertRaises(ValueError):
            extract_title(" \t\n")

    def test_no_text_after_symbol_raises_ValueError(self):
        with self.assertRaises(ValueError):
            extract_title("# ")

    def test_missing_space_before_symbol_raises_ValueError(self):
        with self.assertRaises(ValueError):
            extract_title("#A Simple Story")

    def test_whitespace_before_h1_raises_ValueError(self):
        with self.assertRaises(ValueError):
            extract_title(" # A Simple Story")

    def test_text_before_h1_raises_ValueError(self):
        with self.assertRaises(ValueError):
            extract_title("the title of my story is # A Simple Story")

    def test_h2_raises_ValueError(self):
        with self.assertRaises(ValueError):
            extract_title("## A Little Simple Story")
