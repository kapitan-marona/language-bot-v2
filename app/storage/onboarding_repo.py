from app.storage.db import get_conn
from app.utils.time import now_iso


class OnboardingRepo:
    def get(self, user_id: int):
        with get_conn() as conn:
            row = conn.execute(
                "SELECT * FROM onboarding WHERE user_id=?",
                (user_id,),
            ).fetchone()
            return dict(row) if row else None

    def set_stage(self, user_id: int, stage: str) -> None:
        """
        Обновляет stage. completed не трогаем.
        (Используется во время онбординга между шагами)
        """
        now = now_iso()
        with get_conn() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO onboarding(user_id, stage, completed, started_at) VALUES(?,?,?,?)",
                (user_id, stage, 0, now),
            )
            conn.execute(
                "UPDATE onboarding SET stage=? WHERE user_id=?",
                (stage, user_id),
            )
            conn.commit()

    def complete(self, user_id: int) -> None:
        with get_conn() as conn:
            conn.execute(
                "UPDATE onboarding SET completed=1 WHERE user_id=?",
                (user_id,),
            )
            conn.commit()

    def reset(self, user_id: int, stage: str = "interface_lang") -> None:
        """
        Полный рестарт онбординга для /start:
        - completed = 0
        - stage = interface_lang (или другой)
        - started_at обновляем
        """
        now = now_iso()
        with get_conn() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO onboarding(user_id, stage, completed, started_at) VALUES(?,?,?,?)",
                (user_id, stage, 0, now),
            )
            conn.execute(
                "UPDATE onboarding SET stage=?, completed=0, started_at=? WHERE user_id=?",
                (stage, now, user_id),
            )
            conn.commit()
