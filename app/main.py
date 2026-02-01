from fastapi import FastAPI, Request, HTTPException
import os
import logging

from app.bot import get_telegram_app, ensure_started
from app.storage.db import init_db
from app.utils.logging import setup_logging

app = FastAPI()
log = logging.getLogger(__name__)


@app.on_event("startup")
async def on_startup():
    setup_logging()

    # Init DB
    db_path = os.getenv("DATABASE_PATH", "bot.sqlite3")
    init_db(db_path)

    # Start Telegram app
    tg_app = get_telegram_app()
    await ensure_started(tg_app)

    # ✅ Auto-set webhook on Render
    public_url = os.getenv("RENDER_EXTERNAL_URL")
    secret_path = os.getenv("WEBHOOK_SECRET_PATH")

    if public_url and secret_path:
        webhook_url = f"{public_url.rstrip('/')}/{secret_path}"
        await tg_app.bot.set_webhook(url=webhook_url)
        log.info(f"✅ Webhook set to: {webhook_url}")
    else:
        log.warning("⚠️ RENDER_EXTERNAL_URL or WEBHOOK_SECRET_PATH not set. Webhook not configured.")


# ✅ секретный endpoint вместо /webhook
@app.post("/{secret_path}")
async def telegram_webhook(secret_path: str, req: Request):
    expected = os.getenv("WEBHOOK_SECRET_PATH")

    if not expected or secret_path != expected:
        raise HTTPException(status_code=404, detail="Not found")

    tg_app = get_telegram_app()
    payload = await req.json()

    from telegram import Update
    update = Update.de_json(payload, tg_app.bot)
    await tg_app.process_update(update)

    return {"ok": True}


@app.get("/")
async def root():
    return {"status": "ok"}
