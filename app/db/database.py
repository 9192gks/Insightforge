import sqlite3
from pathlib import Path

DB_PATH = Path("insightforge.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            rows INTEGER NOT NULL,
            columns INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            path TEXT NOT NULL
        )
        """)
        conn.commit()

def add_dataset(dataset_id, filename, rows, columns, created_at, path):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO datasets VALUES (?, ?, ?, ?, ?, ?)",
            (dataset_id, filename, rows, columns, created_at, path)
        )
        conn.commit()

def get_dataset(dataset_id):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT id, filename, rows, columns, created_at, path "
            "FROM datasets WHERE id=?", (dataset_id,)
        ).fetchone()
    if not row:
        return None
    keys = ["id", "filename", "rows", "columns", "created_at", "path"]
    return dict(zip(keys, row))

def list_datasets():
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT id, filename, rows, columns, created_at "
            "FROM datasets ORDER BY created_at DESC"
        ).fetchall()
    keys = ["id", "filename", "rows", "columns", "created_at"]
    return [dict(zip(keys, r)) for r in rows]
