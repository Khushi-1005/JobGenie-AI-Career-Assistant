"""
Simple SQLite storage for job search history.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "jobgenie.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            min_salary_lpa REAL,
            location TEXT,
            results TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_search(keyword: str, min_salary_lpa: float, location: str, results: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO search_history (keyword, min_salary_lpa, location, results, created_at) VALUES (?, ?, ?, ?, ?)",
        (keyword, min_salary_lpa, location, results, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def get_recent_searches(limit: int = 10):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM search_history ORDER BY created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


init_db()