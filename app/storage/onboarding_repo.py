from app.storage.db import get_conn
from app.utils.time import now_iso


class OnboardingRepo:
    def get(self, user_id: int):
        with get_conn() as conn:
            row = conn.execute("SELECT * FROM onboarding WHERE user_id=?", (user_id,)).fetchone()
            return dict(row) if row else None

    def set_stage(self, user_id: int, stage: str) -> None:
        with get_conn() as conn:
            conn.execute("UPDATE onboarding SET stage=? WHERE user_id=?", (stage, user_id))
            conn.commit()

    def complete(self, user_id: int) -> None:
        with get_conn() as conn:
            conn.execute(
                "UPDATE onboarding SET completed=1, stage='done', completed_at=? WHERE user_id=?",
                (now_iso(), user_id),
            )
            conn.commit()
