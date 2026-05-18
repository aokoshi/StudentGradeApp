import unittest
from models import Student, Course, Grade
from services import calculate_gpa, top_students, course_averages


def _setup():
    courses = {
        "Math":    Course("Math", "Calculus", credits=4),
        "Physics": Course("Physics", "Physics I", credits=3),
    }
    s1 = Student(1, "Alice")
    s1.add_grade(Grade(1, "Math", 95))      # A → 4.0 × 4 = 16
    s1.add_grade(Grade(1, "Physics", 85))   # B → 3.0 × 3 = 9
    # GPA = 25 / 7 ≈ 3.57

    s2 = Student(2, "Bob")
    s2.add_grade(Grade(2, "Math", 65))      # D → 1.0 × 4 = 4
    # GPA = 4 / 4 = 1.0
    return [s1, s2], courses


class TestGPA(unittest.TestCase):
    def test_calculate_gpa_weighted(self):
        (s1, _s2), courses = _setup()
        self.assertAlmostEqual(calculate_gpa(s1, courses), 3.57, places=2)

    def test_empty_student(self):
        s = Student(99, "Nobody")
        self.assertEqual(calculate_gpa(s, {}), 0.0)


class TestReports(unittest.TestCase):
    def test_top_students_order(self):
        students, courses = _setup()
        ranked = top_students(students, courses, n=2)
        self.assertEqual(ranked[0][0].name, "Alice")
        self.assertEqual(ranked[1][0].name, "Bob")

    def test_course_averages(self):
        grades = [
            Grade(1, "Math", 80),
            Grade(2, "Math", 60),
            Grade(1, "Physics", 100),
        ]
        avgs = course_averages(grades)
        self.assertEqual(avgs["Math"], 70.0)
        self.assertEqual(avgs["Physics"], 100.0)


if __name__ == "__main__":
    unittest.main()
