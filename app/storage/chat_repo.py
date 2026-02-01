from app.storage.db import get_conn
from app.utils.time import now_iso


class ChatRepo:
    def add(self, user_id: int, role: str, content: str) -> None:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO chat_messages(user_id, role, content, created_at) VALUES(?,?,?,?)",
                (user_id, role, content, now_iso()),
            )
            conn.commit()

    def get_last_pairs(self, user_id: int, pairs: int = 20):
        # 20 pairs ≈ 40 messages
        limit = pairs * 2
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT role, content FROM chat_messages WHERE user_id=? ORDER BY id DESC LIMIT ?",
                (user_id, limit),
            ).fetchall()
            # reverse to chronological
            return [dict(r) for r in rows[::-1]]

    def trim_to_pairs(self, user_id: int, pairs: int = 20) -> None:
        limit = pairs * 2
        with get_conn() as conn:
            # delete everything except last limit rows
            conn.execute(
                """
                DELETE FROM chat_messages
                WHERE user_id=?
                  AND id NOT IN (
                    SELECT id FROM chat_messages
                    WHERE user_id=?
                    ORDER BY id DESC
                    LIMIT ?
                  )
                """,
                (user_id, user_id, limit),
            )
            conn.commit()
