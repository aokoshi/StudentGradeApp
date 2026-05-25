"""StudentGradeAPP v2 — entry point.

Run with::

    python main.py

Initializes the SQLite database, wires up the services (including the
ExportService that writes CSV / JSON reports), and starts the rich-based
menu loop.
"""
from __future__ import annotations

import sys
from pathlib import Path

from database          import Database
from services          import (
    CourseService,
    ExportService,
    GradeService,
    StudentService,
)
from ui                import ConsoleUI, run_main_menu

PROJECT_DIR  = Path(__file__).parent
DB_PATH      = PROJECT_DIR / "data"    / "students.db"
EXPORT_DIR   = PROJECT_DIR / "exports"


def main() -> int:
    ui = ConsoleUI()
    db = Database(DB_PATH)
    try:
        students = StudentService(db)
        courses  = CourseService(db)
        grades   = GradeService(db)
        exports  = ExportService(students, courses, EXPORT_DIR)
        run_main_menu(ui, students, courses, grades, exports)
    except KeyboardInterrupt:
        ui.console.print("\n[cyan]Interrupted — goodbye![/cyan]")
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
