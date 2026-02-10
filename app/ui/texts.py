TEXTS = {
    "ru": {
        # Onboarding UI
        "choose_interface_lang": "Выбери язык интерфейса:\nChoose your interface language:",
        "choose_target_lang": "Выбери язык для изучения:",
        "choose_level": "🧠 Выбери свой уровень:",
        "ask_dup_interface": "Хочешь, я буду дублировать свои сообщения на языке интерфейса?",
        "choose_style": "🎭 Выбери стиль общения:",
        "onboarding_unknown_state": "⚠️ Похоже, я потерял шаг онбординга. Нажми /start, чтобы начать заново.",
        "voice_not_in_onboarding": "Голосовые сообщения будут доступны после онбординга.",

        # System / commands
        "help": "Команды: /start, /settings, /translator_on, /translator_off, /promo, /text, /voice",
        "limit_reached": "Лимит бесплатных сообщений на сегодня исчерпан (15/день). Активируй промокод или премиум.",

        # Modes
        "translator_on": "Переводчик включён. Чтобы выйти: /translator_off",
        "translator_off": "Чат-режим включён. Чтобы включить переводчик: /translator_on",

        # Translator panel (NEW)
        "translator_panel_title": "🧾 <b>TRANSLATOR MODE</b>\n\nОтправь текст — я верну <b>только перевод</b>.\n\nКоманды:\n/translator_off — выйти\n/text — текстовый режим\n/voice — голосовой режим (позже)\n\nНаправление: {direction}\nВывод: {output}",
        "translator_direction_ui_to_target": "Интерфейс → Язык",
        "translator_direction_target_to_ui": "Язык → Интерфейс",
        "translator_output_text": "Текст",
        "translator_output_voice": "Голос",

        "translator_settings_blocked": "⚠️ В режиме переводчика настройки скрыты. Выйди: /translator_off",

        # Settings (existing)
        "settings_title": "⚙️ Настройки",
        "settings_direction": "↔️ Направление перевода",
        "settings_tstyle": "🎭 Стиль перевода",
        "settings_toutput": "🎙 Формат вывода",

        # Stubs
        "promo_stub": "Промокоды подключим следующим шагом через единый PromoArbiter.",
        "chat_stub_reply": "Я на месте 🙂 (пока это заглушка). Следующий шаг — подключить модель и контекст 20 пар.",
        "translator_stub": "TRANSLATOR MODE: (заглушка) — сюда подключим чистый перевод без смайлов и пояснений.",
        "voice_stub": "Голосовой режим скоро подключим (STT/TTS). Пока можно писать текстом.",
        "voice_translator_stub": "TRANSLATOR MODE (voice): заглушка. Скоро добавим распознавание/озвучку.",
        "settings_stub": "Настройки: (заглушка) — скоро будут кнопки языка/уровня/стиля/переводчика.",
        "input_mode_text": "✅ Режим ввода: текст",
        "input_mode_voice": "✅ Режим ввода: голос (скоро)",
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
        "help": "Commands: /start, /settings, /translator_on, /translator_off, /promo, /text, /voice",
        "limit_reached": "Daily free limit reached (15/day). Activate a promo code or premium.",

        # Modes
        "translator_on": "Translator enabled. Exit: /translator_off",
        "translator_off": "Chat mode enabled. Enable translator: /translator_on",

        # Translator panel (NEW)
        "translator_panel_title": "🧾 <b>TRANSLATOR MODE</b>\n\nSend text — I will return <b>only the translation</b>.\n\nCommands:\n/translator_off — exit\n/text — text mode\n/voice — voice mode (later)\n\nDirection: {direction}\nOutput: {output}",
        "translator_direction_ui_to_target": "UI → Target",
        "translator_direction_target_to_ui": "Target → UI",
        "translator_output_text": "Text",
        "translator_output_voice": "Voice",

        "translator_settings_blocked": "⚠️ Settings are hidden in translator mode. Exit: /translator_off",

        # Settings
        "settings_title": "⚙️ Settings",
        "settings_direction": "↔️ Translation direction",
        "settings_tstyle": "🎭 Translation style",
        "settings_toutput": "🎙 Output format",

        # Stubs
        "promo_stub": "Promo codes will be implemented next via a single PromoArbiter.",
        "chat_stub_reply": "I’m here 🙂 (stub). Next: connect the model + 20-pair context.",
        "translator_stub": "TRANSLATOR MODE: (stub) — we’ll add clean translation (no emojis, no explanations).",
        "voice_stub": "Voice mode is coming (STT/TTS). For now, please use text.",
        "voice_translator_stub": "TRANSLATOR MODE (voice): stub. STT/TTS will be added soon.",
        "settings_stub": "Settings: (stub) — language/level/style/translator toggles soon.",
        "input_mode_text": "✅ Input mode: text",
        "input_mode_voice": "✅ Input mode: voice (soon)",
    },
}


def t(key: str, lang: str) -> str:
    lang = lang if lang in TEXTS else "ru"
    return TEXTS[lang].get(key, TEXTS["ru"].get(key, key))
