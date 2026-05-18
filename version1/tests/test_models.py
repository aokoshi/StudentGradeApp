import unittest
from models import Student, Course, Grade, Admin


class TestStudent(unittest.TestCase):
    def test_create_student(self):
        s = Student(1, "Alice", "CS-2102")
        self.assertEqual(s.id, 1)
        self.assertEqual(s.name, "Alice")
        self.assertEqual(s.role(), "student")

    def test_empty_name_rejected(self):
        with self.assertRaises(ValueError):
            Student(1, "   ")

    def test_add_grade(self):
        s = Student(1, "Alice")
        s.add_grade(Grade(1, "Math", 90))
        self.assertEqual(len(s.grades), 1)
        self.assertIn("Math", s.courses())


class TestGrade(unittest.TestCase):
    def test_letter_and_gpa(self):
        self.assertEqual(Grade(1, "X", 95).letter, "A")
        self.assertEqual(Grade(1, "X", 95).gpa_points, 4.0)
        self.assertEqual(Grade(1, "X", 55).letter, "F")

    def test_out_of_range(self):
        with self.assertRaises(ValueError):
            Grade(1, "X", 150)


class TestCourse(unittest.TestCase):
    def test_equality(self):
        self.assertEqual(Course("CS101", "Intro"), Course("CS101", "Whatever"))

    def test_invalid_credits(self):
        with self.assertRaises(ValueError):
            Course("CS101", "Intro", credits=0)


class TestAdmin(unittest.TestCase):
    def test_verify(self):
        a = Admin(1, "Admin", "admin", "pwd")
        self.assertTrue(a.verify("admin", "pwd"))
        self.assertFalse(a.verify("admin", "wrong"))


if __name__ == "__main__":
    unittest.main()
