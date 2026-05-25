"""Export reports to CSV and JSON files.

Each call produces a timestamped folder under ``exports/`` so successive
runs never overwrite previous reports.

CSV files (one per kind of report)
    - students.csv  → id, name, email, course/grade counts, cGPA
    - courses.csv   → id, name, credits, hours, # students
    - grades.csv    → row per (student, course) with all trimester scores

JSON file (single combined snapshot)
    - full_report.json → nested students[].enrollments[] + courses[]
"""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from services.course_service  import CourseService
from services.student_service import StudentService
from utils.gpa                import score_to_gpa, score_to_letter


@dataclass
class ExportResult:
    """Returned by export methods so the UI can show what was written."""

    folder: Path
    files:  list[Path]


class ExportService:
    """Generate CSV / JSON snapshots of the current database state."""

    def __init__(
        self,
        students: StudentService,
        courses:  CourseService,
        export_root: Path,
    ) -> None:
        self.students     = students
        self.courses      = courses
        self.export_root  = Path(export_root)
        self.export_root.mkdir(parents=True, exist_ok=True)

    # ---------- helpers ----------------------------------------------------

    def _new_run_folder(self) -> Path:
        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder = self.export_root / stamp
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def _collect_snapshot(self) -> dict:
        """Pull everything from the DB into a JSON-serializable dict."""
        all_students = self.students.all()
        all_courses  = self.courses.all()

        students_payload = []
        for s in all_students:
            pairs = self.students.enrollments_with_courses(s.id)
            enrollments = [
                {
                    "course_id":   course.id,
                    "course_name": course.name,
                    "credits":     course.credits,
                    "t1":          enr.t1,
                    "t2":          enr.t2,
                    "t3":          enr.t3,
                    "final_score": enr.final_score,
                    "letter":      score_to_letter(enr.final_score),
                    "gpa":         score_to_gpa(enr.final_score),
                }
                for enr, course in pairs
            ]
            students_payload.append({
                "id":           s.id,
                "first_name":   s.first_name,
                "last_name":    s.last_name,
                "full_name":    s.full_name,
                "email":        s.email,
                "course_count": self.students.course_count(s.id),
                "grade_count":  self.students.grade_count(s.id),
                "cgpa":         self.students.cgpa(s.id),
                "enrollments":  enrollments,
            })

        courses_payload = [
            {
                "id":            c.id,
                "name":          c.name,
                "credits":       c.credits,
                "hours":         c.hours,
                "student_count": self.courses.student_count(c.id),
            }
            for c in all_courses
        ]

        return {
            "exported_at": datetime.now().isoformat(timespec="seconds"),
            "students":    students_payload,
            "courses":     courses_payload,
        }

    # ---------- public API -------------------------------------------------

    def export_csv(self) -> ExportResult:
        """Write students.csv, courses.csv, grades.csv into a new folder."""
        folder   = self._new_run_folder()
        snapshot = self._collect_snapshot()
        written: list[Path] = []

        # students.csv — one row per student
        students_path = folder / "students.csv"
        with students_path.open("w", newline="", encoding="utf-8") as fp:
            writer = csv.writer(fp)
            writer.writerow([
                "student_id", "first_name", "last_name", "email",
                "course_count", "grade_count", "cgpa",
            ])
            for s in snapshot["students"]:
                writer.writerow([
                    s["id"], s["first_name"], s["last_name"], s["email"],
                    s["course_count"], s["grade_count"],
                    "" if s["cgpa"] is None else f"{s['cgpa']:.2f}",
                ])
        written.append(students_path)

        # courses.csv — one row per course
        courses_path = folder / "courses.csv"
        with courses_path.open("w", newline="", encoding="utf-8") as fp:
            writer = csv.writer(fp)
            writer.writerow(["course_id", "name", "credits", "hours", "student_count"])
            for c in snapshot["courses"]:
                writer.writerow([c["id"], c["name"], c["credits"], c["hours"], c["student_count"]])
        written.append(courses_path)

        # grades.csv — one row per (student, course) enrollment
        grades_path = folder / "grades.csv"
        with grades_path.open("w", newline="", encoding="utf-8") as fp:
            writer = csv.writer(fp)
            writer.writerow([
                "student_id", "full_name", "course_id", "course_name", "credits",
                "t1", "t2", "t3", "final_score", "letter", "gpa",
            ])
            for s in snapshot["students"]:
                for e in s["enrollments"]:
                    writer.writerow([
                        s["id"], s["full_name"],
                        e["course_id"], e["course_name"], e["credits"],
                        "" if e["t1"] is None else f"{e['t1']:.1f}",
                        "" if e["t2"] is None else f"{e['t2']:.1f}",
                        "" if e["t3"] is None else f"{e['t3']:.1f}",
                        "" if e["final_score"] is None else f"{e['final_score']:.2f}",
                        e["letter"],
                        "" if e["gpa"] is None else f"{e['gpa']:.2f}",
                    ])
        written.append(grades_path)

        return ExportResult(folder=folder, files=written)

    def export_json(self) -> ExportResult:
        """Write a single combined ``full_report.json`` into a new folder."""
        folder   = self._new_run_folder()
        snapshot = self._collect_snapshot()
        path     = folder / "full_report.json"
        with path.open("w", encoding="utf-8") as fp:
            json.dump(snapshot, fp, indent=2, ensure_ascii=False)
        return ExportResult(folder=folder, files=[path])
