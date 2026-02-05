# app/storage/history_repo.py
from __future__ import annotations

from typing import List, Dict
from app.storage.db import get_conn


class HistoryRepo:
    def __init__(self):
        self._ensure()

    def _ensure(self):
        conn = get_conn()
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    task_mode TEXT NOT NULL,     -- chat | translator
                    role TEXT NOT NULL,          -- user | assistant | system
                    content TEXT NOT NULL,
                    created_at INTEGER NOT NULL
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_chat_history_user_mode_id ON chat_history(user_id, task_mode, id)"
            )
            conn.commit()
        finally:
            conn.close()

    def add(self, user_id: int, role: str, content: str, task_mode: str = "chat"):
        conn = get_conn()
        try:
            conn.execute(
                """
                INSERT INTO chat_history (user_id, task_mode, role, content, created_at)
                VALUES (?, ?, ?, ?, CAST(strftime('%s','now') AS INTEGER))
                """,
                (int(user_id), str(task_mode), str(role), str(content)),
            )
            conn.commit()
        finally:
            conn.close()

    def get_recent(self, user_id: int, limit: int = 40, task_mode: str = "chat") -> List[Dict]:
        """
        Возвращает сообщения в хронологическом порядке (старые -> новые)
        """
        conn = get_conn()
        try:
            rows = conn.execute(
                """
                SELECT role, content
                FROM chat_history
                WHERE user_id = ? AND task_mode = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (int(user_id), str(task_mode), int(limit)),
            ).fetchall()
            out = [{"role": r["role"], "content": r["content"]} for r in rows]
            out.reverse()
            return out
        finally:
            conn.close()

    def trim(self, user_id: int, keep: int = 40, task_mode: str = "chat"):
        """
        Оставить только последние keep сообщений (например 40 = 20 пар)
        """
        conn = get_conn()
        try:
            # найдём id, начиная с которого держим
            row = conn.execute(
                """
                SELECT id
                FROM chat_history
                WHERE user_id = ? AND task_mode = ?
                ORDER BY id DESC
                LIMIT 1 OFFSET ?
                """,
                (int(user_id), str(task_mode), int(keep - 1)),
            ).fetchone()

            if row is None:
                return

            threshold_id = row["id"]
            conn.execute(
                """
                DELETE FROM chat_history
                WHERE user_id = ? AND task_mode = ? AND id < ?
                """,
                (int(user_id), str(task_mode), int(threshold_id)),
            )
            conn.commit()
        finally:
            conn.close()

    def clear(self, user_id: int, task_mode: str = "chat"):
        conn = get_conn()
        try:
            conn.execute(
                "DELETE FROM chat_history WHERE user_id = ? AND task_mode = ?",
                (int(user_id), str(task_mode)),
            )
            conn.commit()
        finally:
            conn.close()
