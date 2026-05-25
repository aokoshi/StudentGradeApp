"""Unit tests for input validators."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validators import (
    is_valid_email,
    is_valid_name,
    parse_int,
    parse_score,
)


class EmailTests(unittest.TestCase):
    def test_valid(self) -> None:
        for email in ("a@b.co", "first.last@aitu.edu.kz", "x+y@example.org"):
            self.assertTrue(is_valid_email(email), email)

    def test_invalid(self) -> None:
        for email in ("", "no-at-sign", "a@b", "a@@b.co", "a b@c.co"):
            self.assertFalse(is_valid_email(email), email)


class NameTests(unittest.TestCase):
    def test_valid(self) -> None:
        for name in ("Aizada", "Mary Anne", "O'Brien", "Jean-Luc"):
            self.assertTrue(is_valid_name(name), name)

    def test_invalid(self) -> None:
        for name in ("", "123", "  ", "Bob123", "!"):
            self.assertFalse(is_valid_name(name), name)


class ParseIntTests(unittest.TestCase):
    def test_valid_bounds(self) -> None:
        self.assertEqual(parse_int("5", minimum=1, maximum=10), 5)

    def test_below_min_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_int("0", minimum=1)

    def test_above_max_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_int("11", maximum=10)

    def test_non_integer_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_int("abc")


class ParseScoreTests(unittest.TestCase):
    def test_valid(self) -> None:
        self.assertEqual(parse_score("87.5"), 87.5)
        self.assertEqual(parse_score("0"), 0.0)
        self.assertEqual(parse_score("100"), 100.0)

    def test_out_of_range(self) -> None:
        with self.assertRaises(ValueError):
            parse_score("-1")
        with self.assertRaises(ValueError):
            parse_score("101")


if __name__ == "__main__":
    unittest.main()
