from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .levels_texts import LEVEL_GUIDE_BUTTON, LEVEL_GUIDE_CLOSE_BUTTON, LEVEL_DONE_BUTTON


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


def kb_level(lang: str = "ru") -> InlineKeyboardMarkup:
    lang = lang if lang in ("ru", "en") else "ru"

    rows = [
        [
            InlineKeyboardButton("A0", callback_data="onb:level:A0"),
            InlineKeyboardButton("A1", callback_data="onb:level:A1"),
            InlineKeyboardButton("A2", callback_data="onb:level:A2"),
        ],
        [
            InlineKeyboardButton("B1", callback_data="onb:level:B1"),
            InlineKeyboardButton("B2", callback_data="onb:level:B2"),
            InlineKeyboardButton("C1", callback_data="onb:level:C1"),
            InlineKeyboardButton("C2", callback_data="onb:level:C2"),
        ],
        [
            InlineKeyboardButton(LEVEL_GUIDE_BUTTON.get(lang, LEVEL_GUIDE_BUTTON["ru"]), callback_data="onb:level_help"),
            InlineKeyboardButton(LEVEL_DONE_BUTTON.get(lang, LEVEL_DONE_BUTTON["ru"]), callback_data="onb:level_done"),
        ],
    ]
    return InlineKeyboardMarkup(rows)


def kb_level_guide_close(lang: str = "ru") -> InlineKeyboardMarkup:
    lang = lang if lang in ("ru", "en") else "ru"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(LEVEL_GUIDE_CLOSE_BUTTON.get(lang, LEVEL_GUIDE_CLOSE_BUTTON["ru"]), callback_data="onb:level_help_close")]
    ])


def kb_dup_interface(lang: str = "ru") -> InlineKeyboardMarkup:
    # оставляем RU/EN как было — позже сделаем локализацию, если захочешь
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Да", callback_data="onb:dub:yes"),
            InlineKeyboardButton("Нет", callback_data="onb:dub:no"),
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

