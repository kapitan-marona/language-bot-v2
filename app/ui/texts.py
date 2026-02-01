TEXTS = {
    "ru": {
        "choose_interface_lang": "Выбери язык интерфейса:",
        "onboarding_use_buttons": "Пожалуйста, используй кнопки ниже 🙂",
        "ask_promo": "У тебя есть промокод?\n👉 Введи его или напиши 'нет'",
        "promo_received_stub": "✅ Принял промокод: {code}\n(Сейчас логика промо в разработке — подключим дальше.)\nМожешь писать сообщение 🙂",
        "voice_not_in_onboarding": "Голосовые сообщения будут доступны после онбординга.",
        "chat_stub_reply": "Я на месте 🙂 (пока это заглушка). Следующий шаг — подключим модель и контекст 20 пар.",
        "translator_stub": "TRANSLATOR MODE: (заглушка) — сюда подключим чистый перевод без смайлов и пояснений.",
        "voice_stub": "Голосовой режим скоро подключим (STT/TTS). Пока можно писать текстом.",
        "voice_translator_stub": "TRANSLATOR MODE (voice): заглушка. Скоро добавим распознавание/озвучку.",
        "settings_stub": "Настройки: (заглушка) — скоро будут кнопки языка/уровня/стиля/переводчика.",
        "help": "Команды: /start, /settings, /translator_on, /translator_off, /promo",
        "translator_on": "Переводчик включён. Чтобы выйти: /translator_off",
        "translator_off": "Чат-режим включён. Чтобы включить переводчик: /translator_on",
        "promo_stub": "Промокоды подключим следующим шагом через единый PromoArbiter.",
        "limit_reached": "Лимит бесплатных сообщений на сегодня исчерпан (15/день). Активируй промокод или премиум.",
        "onboarding_done_stub": "✅ Ок! Онбординг продолжаем допиливать, но ты уже можешь общаться со мной. Напиши любое сообщение 🙂",
    },
    "en": {
        "choose_interface_lang": "Choose your interface language:",
        "onboarding_use_buttons": "Please use the buttons below 🙂",
        "ask_promo": "Do you have a promo code?\n👉 Enter it or type 'no'",
        "onboarding_done_stub": "✅ Okay! Onboarding is still being finalized, but you can already chat with me. Send any message 🙂",
        "voice_not_in_onboarding": "Voice messages will be available after onboarding.",
        "chat_stub_reply": "I’m here 🙂 (stub). Next: connect the model + 20-pair context.",
        "translator_stub": "TRANSLATOR MODE: (stub) — we’ll add clean translation (no emojis, no explanations).",
        "voice_stub": "Voice mode is coming (STT/TTS). For now, please use text.",
        "voice_translator_stub": "TRANSLATOR MODE (voice): stub. STT/TTS will be added soon.",
        "settings_stub": "Settings: (stub) — language/level/style/translator toggles soon.",
        "help": "Commands: /start, /settings, /translator_on, /translator_off, /promo",
        "translator_on": "Translator enabled. Exit: /translator_off",
        "translator_off": "Chat mode enabled. Enable translator: /translator_on",
        "promo_stub": "Promo codes will be implemented next via a single PromoArbiter.",
        "limit_reached": "Daily free limit reached (15/day). Activate a promo code or premium.",
        "promo_received_stub": "✅ Promo code received: {code}\n(Promo logic is being implemented next.)\nYou can chat now 🙂",
    },
}


def t(key: str, lang: str) -> str:
    lang = lang if lang in TEXTS else "ru"
    return TEXTS[lang].get(key, TEXTS["ru"].get(key, key))
