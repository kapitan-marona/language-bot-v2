from app.storage.db import get_conn
from app.utils.time import now_iso


class TranslatorRepo:
    def add(self, user_id: int, role: str, content: str) -> None:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO translator_messages(user_id, role, content, created_at) VALUES(?,?,?,?)",
                (user_id, role, content, now_iso()),
            )
            conn.commit()

    def trim_to_pairs(self, user_id: int, pairs: int = 20) -> None:
        limit = pairs * 2
        with get_conn() as conn:
            conn.execute(
                """
                DELETE FROM translator_messages
                WHERE user_id=?
                  AND id NOT IN (
                    SELECT id FROM translator_messages
                    WHERE user_id=?
                    ORDER BY id DESC
                    LIMIT ?
                  )
                """,
                (user_id, user_id, limit),
            )
            conn.commit()
