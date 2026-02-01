from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def kb_interface_lang() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data="onb:iface:ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="onb:iface:en"),
        ]
    ])


def kb_target_lang() -> InlineKeyboardMarkup:
    # label -> target_lang code
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

def kb_level() -> InlineKeyboardMarkup:
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
            InlineKeyboardButton("❓ Какой у меня уровень?", callback_data="onb:level_help"),
        ],
    ]
    return InlineKeyboardMarkup(rows)


def kb_dup_interface() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Да", callback_data="onb:dub:yes"),
            InlineKeyboardButton("Нет", callback_data="onb:dub:no"),
        ]
    ])
