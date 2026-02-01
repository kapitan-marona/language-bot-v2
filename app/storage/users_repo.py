from app.storage.db import get_conn
from app.utils.time import now_iso


class UsersRepo:
    def ensure_user(self, user_id: int, default_interface_lang: str = "ru") -> None:
        now = now_iso()
        with get_conn() as conn:
            cur = conn.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
            if cur.fetchone():
                conn.execute("UPDATE users SET updated_at=? WHERE user_id=?", (now, user_id))
            else:
                conn.execute(
                    "INSERT INTO users(user_id, interface_lang, created_at, updated_at) VALUES(?,?,?,?)",
                    (user_id, default_interface_lang, now, now),
                )
                conn.execute(
                    "INSERT OR IGNORE INTO access_state(user_id, access_type, updated_at) VALUES(?,?,?)",
                    (user_id, "free", now),
                )
                conn.execute(
                    "INSERT OR IGNORE INTO onboarding(user_id, stage, completed, started_at) VALUES(?,?,?,?)",
                    (user_id, "interface_lang", 0, now),
                )
            conn.commit()

    def get_user(self, user_id: int):
        with get_conn() as conn:
            row = conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
            return dict(row) if row else None

    def update_user(self, user_id: int, **fields) -> None:
        if not fields:
            return
        fields["updated_at"] = now_iso()
        keys = list(fields.keys())
        sets = ", ".join([f"{k}=?" for k in keys])
        vals = [fields[k] for k in keys] + [user_id]
        with get_conn() as conn:
            conn.execute(f"UPDATE users SET {sets} WHERE user_id=?", vals)
            conn.commit()
