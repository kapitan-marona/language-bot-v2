# app/utils/logging.py

import logging


def setup_logging():
    # ✅ скрываем URL запросов httpx (там бывает BOT TOKEN)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    # ✅ общий формат логов
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
