import sqlite3
from typing import Optional

_DB_PATH: Optional[str] = None


def init_db(db_path: str) -> None:
    global _DB_PATH
    _DB_PATH = db_path

    from app.storage.migrations import run_migrations
    run_migrations()


def get_conn() -> sqlite3.Connection:
    if not _DB_PATH:
        raise RuntimeError("DB not initialized. Call init_db() first.")
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn
