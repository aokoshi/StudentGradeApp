"""Integration tests for the ExportService."""
import csv
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database          import Database
from services          import (
    CourseService,
    ExportService,
    GradeService,
    StudentService,
)


class ExportServiceTests(unittest.TestCase):
    """Spin up an in-memory-ish DB, seed it, and assert the export files."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="sga_test_"))
        self.db  = Database(self.tmp / "students.db")
        self.students = StudentService(self.db)
        self.courses  = CourseService(self.db)
        self.grades   = GradeService(self.db)
        self.exports  = ExportService(self.students, self.courses, self.tmp / "exports")

        s  = self.students.create("Aizada", "Tester", "a@aitu.edu.kz")
        c1 = self.courses.create("Intro to Programming 2", 3, 60)
        c2 = self.courses.create("Calculus I", 4, 90)
        self.grades.enroll(s.id, c1.id)
        self.grades.enroll(s.id, c2.id)
        self.grades.set_trimester_score(s.id, c1.id, 1, 92)
        self.grades.set_trimester_score(s.id, c1.id, 2, 88)
        self.grades.set_trimester_score(s.id, c2.id, 1, 75)
        self.student_id = s.id

    def tearDown(self) -> None:
        self.db.close()

    # ---------- CSV --------------------------------------------------------

    def test_csv_export_creates_three_files(self) -> None:
        result = self.exports.export_csv()
        names  = {p.name for p in result.files}
        self.assertEqual(names, {"students.csv", "courses.csv", "grades.csv"})
        for path in result.files:
            self.assertTrue(path.exists(), f"{path} should have been written")

    def test_csv_students_row_content(self) -> None:
        result = self.exports.export_csv()
        path   = next(p for p in result.files if p.name == "students.csv")
        with path.open(encoding="utf-8") as fp:
            rows = list(csv.DictReader(fp))
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["first_name"], "Aizada")
        self.assertEqual(row["course_count"], "2")
        self.assertEqual(row["grade_count"], "3")
        self.assertEqual(row["cgpa"], "3.10")  # see math in main README

    def test_csv_grades_has_per_enrollment_rows(self) -> None:
        result = self.exports.export_csv()
        path   = next(p for p in result.files if p.name == "grades.csv")
        with path.open(encoding="utf-8") as fp:
            rows = list(csv.DictReader(fp))
        # Two enrollments, so two grade rows.
        self.assertEqual(len(rows), 2)
        by_course = {r["course_name"]: r for r in rows}
        self.assertEqual(by_course["Intro to Programming 2"]["letter"], "A-")
        self.assertEqual(by_course["Calculus I"]["t1"], "75.0")

    # ---------- JSON -------------------------------------------------------

    def test_json_export_writes_single_file(self) -> None:
        result = self.exports.export_json()
        self.assertEqual(len(result.files), 1)
        self.assertEqual(result.files[0].name, "full_report.json")

    def test_json_payload_structure(self) -> None:
        result = self.exports.export_json()
        with result.files[0].open(encoding="utf-8") as fp:
            payload = json.load(fp)
        self.assertIn("exported_at", payload)
        self.assertEqual(len(payload["students"]), 1)
        self.assertEqual(len(payload["courses"]), 2)
        student = payload["students"][0]
        self.assertEqual(student["cgpa"], 3.10)
        self.assertEqual(len(student["enrollments"]), 2)


if __name__ == "__main__":
    unittest.main()
