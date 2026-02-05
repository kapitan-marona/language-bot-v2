# app/ui/texts.py

TEXTS = {
    "ru": {
        # Onboarding UI (короткие вопросы/заголовки для экранов)
        "choose_interface_lang": "Выбери язык интерфейса:\nChoose your interface language:",
        "choose_target_lang": "Выбери язык для изучения:",
        "choose_level": "🧠 Выбери свой уровень:",
        "ask_dup_interface": "Хочешь, я буду дублировать свои сообщения на языке интерфейса?",
        "choose_style": "🎭 Выбери стиль общения:",
        "onboarding_unknown_state": "⚠️ Похоже, я потерял шаг онбординга. Нажми /start, чтобы начать заново.",
        "voice_not_in_onboarding": "Голосовые сообщения будут доступны после онбординга.",

        # System / commands
        "help": "Команды: /start, /settings, /translator_on, /translator_off, /promo",
        "limit_reached": "Лимит бесплатных сообщений на сегодня исчерпан (15/день). Активируй промокод или премиум.",

        # Modes
        "translator_on": "Переводчик включён. Чтобы выйти: /translator_off",
        "translator_off": "Чат-режим включён. Чтобы включить переводчик: /translator_on",

        # Stubs (пока не подключили)
        "promo_stub": "Промокоды подключим следующим шагом через единый PromoArbiter.",
        "chat_stub_reply": "Я на месте 🙂 (пока это заглушка). Следующий шаг — подключить модель и контекст 20 пар.",
        "translator_stub": "TRANSLATOR MODE: (заглушка) — сюда подключим чистый перевод без смайлов и пояснений.",
        "voice_stub": "Голосовой режим скоро подключим (STT/TTS). Пока можно писать текстом.",
        "voice_translator_stub": "TRANSLATOR MODE (voice): заглушка. Скоро добавим распознавание/озвучку.",
        "settings_stub": "Настройки: (заглушка) — скоро будут кнопки языка/уровня/стиля/переводчика.",
    },

    "en": {
        # Onboarding UI
        "choose_interface_lang": "Выбери язык интерфейса:\nChoose your interface language:",
        "choose_target_lang": "Choose a language to learn:",
        "choose_level": "🧠 Choose your level:",
        "ask_dup_interface": "Do you want me to duplicate my messages in your interface language?",
        "choose_style": "🎭 Choose your conversation style:",
        "onboarding_unknown_state": "⚠️ Looks like I lost the onboarding step. Send /start to begin again.",
        "voice_not_in_onboarding": "Voice messages will be available after onboarding.",

        # System / commands
        "help": "Commands: /start, /settings, /translator_on, /translator_off, /promo",
        "limit_reached": "Daily free limit reached (15/day). Activate a promo code or premium.",

        # Modes
        "translator_on": "Translator enabled. Exit: /translator_off",
        "translator_off": "Chat mode enabled. Enable translator: /translator_on",

        # Stubs
        "promo_stub": "Promo codes will be implemented next via a single PromoArbiter.",
        "chat_stub_reply": "I’m here 🙂 (stub). Next: connect the model + 20-pair context.",
        "translator_stub": "TRANSLATOR MODE: (stub) — we’ll add clean translation (no emojis, no explanations).",
        "voice_stub": "Voice mode is coming (STT/TTS). For now, please use text.",
        "voice_translator_stub": "TRANSLATOR MODE (voice): stub. STT/TTS will be added soon.",
        "settings_stub": "Settings: (stub) — language/level/style/translator toggles soon.",
    },
}


def t(key: str, lang: str) -> str:
    lang = lang if lang in TEXTS else "ru"
    return TEXTS[lang].get(key, TEXTS["ru"].get(key, key))
