from app.storage.db import get_conn
from app.utils.time import today_ymd


class UsageRepo:
    def get_today_count(self, user_id: int) -> int:
        d = today_ymd()
        with get_conn() as conn:
            row = conn.execute(
                "SELECT count FROM usage_counters WHERE user_id=? AND date=?",
                (user_id, d),
            ).fetchone()
            return int(row["count"]) if row else 0

    def inc_today(self, user_id: int, delta: int = 1) -> int:
        d = today_ymd()
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO usage_counters(user_id, date, count) VALUES(?,?,0) "
                "ON CONFLICT(user_id, date) DO UPDATE SET count=count+excluded.count",
                (user_id, d),
            )
            # Above adds 0; do real inc:
            conn.execute(
                "UPDATE usage_counters SET count=count+? WHERE user_id=? AND date=?",
                (delta, user_id, d),
            )
            row = conn.execute(
                "SELECT count FROM usage_counters WHERE user_id=? AND date=?",
                (user_id, d),
            ).fetchone()
            conn.commit()
            return int(row["count"])
