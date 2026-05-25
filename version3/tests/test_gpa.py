"""Unit tests for GPA conversion math."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.gpa import cumulative_gpa, score_to_gpa, score_to_letter


class ScoreToGpaTests(unittest.TestCase):
    def test_perfect_score_is_a(self) -> None:
        self.assertEqual(score_to_gpa(100), 4.00)
        self.assertEqual(score_to_letter(100), "A")

    def test_boundary_grades(self) -> None:
        boundaries = {
            95: "A",  90: "A-", 85: "B+", 80: "B",
            75: "B-", 70: "C+", 65: "C",  60: "C-",
            55: "D+", 50: "D",  49: "F",  0:  "F",
        }
        for score, expected in boundaries.items():
            self.assertEqual(score_to_letter(score), expected, f"failed at {score}")

    def test_none_is_returned_for_missing(self) -> None:
        self.assertIsNone(score_to_gpa(None))
        self.assertEqual(score_to_letter(None), "-")

    def test_out_of_range_raises(self) -> None:
        with self.assertRaises(ValueError):
            score_to_gpa(-1)
        with self.assertRaises(ValueError):
            score_to_gpa(101)


class CumulativeGpaTests(unittest.TestCase):
    def test_empty_returns_none(self) -> None:
        self.assertIsNone(cumulative_gpa([]))

    def test_single_course(self) -> None:
        self.assertEqual(cumulative_gpa([(92, 3)]), 3.67)

    def test_weighted_average(self) -> None:
        # 100 (A=4.0, credits=4) + 70 (C+=2.33, credits=2)
        # = (16 + 4.66) / 6 = 3.443... → rounded 3.44
        self.assertEqual(cumulative_gpa([(100, 4), (70, 2)]), 3.44)

    def test_missing_scores_are_skipped(self) -> None:
        self.assertEqual(cumulative_gpa([(None, 3), (90, 3)]), 3.67)


if __name__ == "__main__":
    unittest.main()
