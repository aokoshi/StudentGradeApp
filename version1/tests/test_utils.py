import unittest
import tempfile
import os
from utils import (
    load_grades_csv, save_grades_csv,
    is_valid_email, is_valid_score, is_valid_course_code,
)
from models import Student, Grade


class TestValidators(unittest.TestCase):
    def test_email(self):
        self.assertTrue(is_valid_email("a@b.co"))
        self.assertFalse(is_valid_email("not-an-email"))
        self.assertFalse(is_valid_email(""))

    def test_score(self):
        self.assertTrue(is_valid_score(85))
        self.assertTrue(is_valid_score("0"))
        self.assertFalse(is_valid_score(-1))
        self.assertFalse(is_valid_score("abc"))

    def test_course_code(self):
        self.assertTrue(is_valid_course_code("CS101"))
        self.assertTrue(is_valid_course_code("MATH2010"))
        self.assertFalse(is_valid_course_code("cs101"))
        self.assertFalse(is_valid_course_code("CS"))


class TestCsvRoundtrip(unittest.TestCase):
    def test_save_then_load(self):
        s = Student(1, "Alice")
        s.add_grade(Grade(1, "Math", 90))
        s.add_grade(Grade(1, "Physics", 75))

        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
            path = tmp.name
        try:
            save_grades_csv(path, {1: s})
            loaded, grades = load_grades_csv(path)
            self.assertIn(1, loaded)
            self.assertEqual(len(grades), 2)
            self.assertEqual(loaded[1].name, "Alice")
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
