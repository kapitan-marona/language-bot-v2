import os
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from app.dispatcher.dispatcher import Dispatcher

_TG_APP: Application | None = None
_DISPATCHER: Dispatcher | None = None


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

    # ✅ Commands: перечисляем явно, чтобы PTB точно маршрутизировал /команды
    application.add_handler(CommandHandler(
        ["start", "help", "settings", "translator_on", "translator_off", "promo", "debug_user"],
        dispatcher.handle_command,
    ))

    # ✅ Text (не команды) → central dispatcher
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, dispatcher.handle_text))

    # ✅ Voice / Audio → central dispatcher
    application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, dispatcher.handle_voice))

    # ✅ Callbacks → central dispatcher
    application.add_handler(CallbackQueryHandler(dispatcher.handle_callback))

    _TG_APP = application
    return _TG_APP


async def ensure_started(app: Application) -> None:
    # Start PTB internals without polling (webhook mode)
    if not app.running:
        await app.initialize()
        await app.start()
