"""SQLite database manager — initializes schema and exposes a cursor."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

# Module-level SQL kept here so the schema lives next to the manager.
SCHEMA: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS students (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name  TEXT NOT NULL,
        last_name   TEXT NOT NULL,
        email       TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS courses (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        name     TEXT NOT NULL UNIQUE,
        credits  INTEGER NOT NULL CHECK (credits > 0),
        hours    INTEGER NOT NULL CHECK (hours  > 0)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS enrollments (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        course_id  INTEGER NOT NULL,
        t1         REAL,
        t2         REAL,
        t3         REAL,
        UNIQUE (student_id, course_id),
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
        FOREIGN KEY (course_id)  REFERENCES courses(id)  ON DELETE CASCADE
    )
    """,
)


class Database:
    """Thin wrapper around :mod:`sqlite3` with schema bootstrapping.

    The same connection is reused for the lifetime of the app; foreign-key
    constraints are turned on explicitly because SQLite leaves them off by
    default.
    """

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._init_schema()

    def _init_schema(self) -> None:
        """Create tables if they do not yet exist (idempotent)."""
        with self.conn:
            for stmt in SCHEMA:
                self.conn.execute(stmt)

    @contextmanager
    def cursor(self) -> Iterator[sqlite3.Cursor]:
        """Yield a cursor inside a transaction; commits on success."""
        cur = self.conn.cursor()
        try:
            yield cur
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cur.close()

    def close(self) -> None:
        self.conn.close()
