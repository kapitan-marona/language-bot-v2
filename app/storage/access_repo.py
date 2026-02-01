from app.storage.db import get_conn
from app.utils.time import now_iso


class AccessRepo:
    def get(self, user_id: int):
        with get_conn() as conn:
            row = conn.execute("SELECT * FROM access_state WHERE user_id=?", (user_id,)).fetchone()
            return dict(row) if row else None

    def set_access(self, user_id: int, access_type: str, valid_until: str | None, allowed_languages_json: str | None):
        with get_conn() as conn:
            conn.execute(
                """
                INSERT INTO access_state(user_id, access_type, valid_until, allowed_languages, updated_at)
                VALUES(?,?,?,?,?)
                ON CONFLICT(user_id) DO UPDATE SET
                  access_type=excluded.access_type,
                  valid_until=excluded.valid_until,
                  allowed_languages=excluded.allowed_languages,
                  updated_at=excluded.updated_at
                """,
                (user_id, access_type, valid_until, allowed_languages_json, now_iso()),
            )
            conn.commit()
