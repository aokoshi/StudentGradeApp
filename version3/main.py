"""StudentGradeAPP v2 — entry point.

Run with::

    python main.py

Initializes the SQLite database, wires up the services, and starts the
rich-based menu loop.
"""
from __future__ import annotations

import sys
from pathlib import Path

from database          import Database
from services          import CourseService, GradeService, StudentService
from ui                import ConsoleUI, run_main_menu

DB_PATH = Path(__file__).parent / "data" / "students.db"


def main() -> int:
    ui = ConsoleUI()
    db = Database(DB_PATH)
    try:
        students = StudentService(db)
        courses  = CourseService(db)
        grades   = GradeService(db)
        run_main_menu(ui, students, courses, grades)
    except KeyboardInterrupt:
        ui.console.print("\n[cyan]Interrupted — goodbye![/cyan]")
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
