import os
from telegram.ext import Application, MessageHandler, CallbackQueryHandler, CommandHandler, filters

from app.dispatcher.dispatcher import Dispatcher

_TG_APP = None
_DISPATCHER = None


def get_dispatcher() -> Dispatcher:
    global _DISPATCHER
    if _DISPATCHER is None:
        _DISPATCHER = Dispatcher()
    return _DISPATCHER


def get_telegram_app() -> Application:
    global _TG_APP
    if _TG_APP is not None:
        return _TG_APP

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set")

    application = Application.builder().token(token).build()
    dispatcher = get_dispatcher()

    # Commands (system) — still go through dispatcher (to keep one brain),
    # but PTB requires explicit handlers for /commands if we want.
    application.add_handler(CommandHandler("start", dispatcher.handle_command))
    application.add_handler(CommandHandler("help", dispatcher.handle_command))
    application.add_handler(CommandHandler("settings", dispatcher.handle_command))
    application.add_handler(CommandHandler("translator_on", dispatcher.handle_command))
    application.add_handler(CommandHandler("translator_off", dispatcher.handle_command))
    application.add_handler(CommandHandler("promo", dispatcher.handle_command))

    # One text handler → central dispatcher
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, dispatcher.handle_text))

    # Voice/audio handler → central dispatcher
    application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, dispatcher.handle_voice))

    # Callbacks → central dispatcher
    application.add_handler(CallbackQueryHandler(dispatcher.handle_callback))

    _TG_APP = application
    return _TG_APP


async def ensure_started(app: Application) -> None:
    # Start PTB internals without polling (webhook mode)
    if not app.running:
        await app.initialize()
        await app.start()
