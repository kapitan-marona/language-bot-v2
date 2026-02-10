from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from app.ui.levels_texts import LEVEL_GUIDE_BUTTON, LEVEL_GUIDE_CLOSE_BUTTON


# -------------------------
# Onboarding keyboards
# -------------------------

def kb_interface_lang() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data="onb:iface:ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="onb:iface:en"),
        ]
    ])


def kb_target_lang() -> InlineKeyboardMarkup:
    items = [
        ("🇷🇺 Русский", "ru"),
        ("🇬🇧 English", "en"),
        ("🇫🇷 Français", "fr"),
        ("🇪🇸 Español", "es"),
        ("🇩🇪 Deutsch", "de"),
        ("🇸🇪 Svenska", "sv"),
        ("🇫🇮 Suomi", "fi"),
    ]

    rows = []
    row = []
    for label, code in items:
        row.append(InlineKeyboardButton(label, callback_data=f"onb:target:{code}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)

    return InlineKeyboardMarkup(rows)


def kb_level(lang="ru"):
    L = "ru" if lang == "ru" else "en"

    buttons = [
        [
            InlineKeyboardButton("A0", callback_data="onb:level:A0"),
            InlineKeyboardButton("A1", callback_data="onb:level:A1"),
            InlineKeyboardButton("A2", callback_data="onb:level:A2"),
        ],
        [
            InlineKeyboardButton("B1", callback_data="onb:level:B1"),
            InlineKeyboardButton("B2", callback_data="onb:level:B2"),
        ],
        [
            InlineKeyboardButton("C1", callback_data="onb:level:C1"),
            InlineKeyboardButton("C2", callback_data="onb:level:C2"),
        ],
        [
            InlineKeyboardButton(LEVEL_GUIDE_BUTTON[L], callback_data="onb:level_help")
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def kb_level_guide_close(lang: str = "ru") -> InlineKeyboardMarkup:
    lang = lang if lang in ("ru", "en") else "ru"
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(
            LEVEL_GUIDE_CLOSE_BUTTON.get(lang, LEVEL_GUIDE_CLOSE_BUTTON["ru"]),
            callback_data="onb:level_help_close",
        )
    ]])


def kb_dup_interface(lang: str = "ru") -> InlineKeyboardMarkup:
    lang = lang if lang in ("ru", "en") else "ru"
    yes = "Да" if lang == "ru" else "Yes"
    no = "Нет" if lang == "ru" else "No"
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(yes, callback_data="onb:dub:yes"),
            InlineKeyboardButton(no, callback_data="onb:dub:no"),
        ]
    ])


def kb_style(lang: str = "ru") -> InlineKeyboardMarkup:
    lang = lang if lang in ("ru", "en") else "ru"
    if lang == "en":
        casual = "😎 Casual"
        business = "🧑‍💼 Business"
    else:
        casual = "😎 Разговорный"
        business = "🧑‍💼 Деловой"

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(casual, callback_data="onb:style:casual"),
            InlineKeyboardButton(business, callback_data="onb:style:business"),
        ]
    ])


# -------------------------
# Translator panel (NEW)
# callback prefix: tr:...
# -------------------------

def kb_translator_panel(lang: str, direction_db: str, output: str) -> InlineKeyboardMarkup:
    """
    direction_db: ui_to_target | target_to_ui
    output: text | voice
    """
    lang = lang if lang in ("ru", "en") else "ru"
    direction_db = direction_db if direction_db in ("ui_to_target", "target_to_ui") else "ui_to_target"
    output = output if output in ("text", "voice") else "text"

    if lang == "en":
        off = "⏹ Translator OFF"
        toggle = "🔁 Toggle direction"
        text_btn = "⌨️ /text"
        voice_btn = "🎙 /voice"
    else:
        off = "⏹ Выключить"
        toggle = "🔁 Сменить направление"
        text_btn = "⌨️ /text"
        voice_btn = "🎙 /voice"

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(off, callback_data="tr:off")],
        [InlineKeyboardButton(toggle, callback_data="tr:dir:toggle")],
        [
            InlineKeyboardButton(text_btn, callback_data="tr:out:text"),
            InlineKeyboardButton(voice_btn, callback_data="tr:out:voice"),
        ],
    ])
