from dataclasses import dataclass
from app.storage.usage_repo import UsageRepo
from app.storage.access_repo import AccessRepo


@dataclass
class GateDecision:
    ok: bool
    reason: str | None = None
    remaining: int | None = None


class UsageGate:
    FREE_DAILY_LIMIT = 15

    def __init__(self):
        self.usage = UsageRepo()
        self.access = AccessRepo()

    def can_consume(self, user_id: int) -> GateDecision:
        a = self.access.get(user_id)
        # If premium/strong promo, limit might be different; for now only free enforced
        if a and a["access_type"] != "free":
            return GateDecision(ok=True)

        used = self.usage.get_today_count(user_id)
        remaining = self.FREE_DAILY_LIMIT - used
        if remaining <= 0:
            return GateDecision(ok=False, reason="free_limit_reached", remaining=0)
        return GateDecision(ok=True, remaining=remaining)

    def consume(self, user_id: int) -> int:
        return self.usage.inc_today(user_id, 1)
