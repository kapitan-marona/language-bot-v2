from datetime import datetime, timezone

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def today_ymd() -> str:
    return datetime.now(timezone.utc).date().isoformat()
