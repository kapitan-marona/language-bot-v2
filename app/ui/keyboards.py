from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def kb_interface_lang() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Русский", callback_data="onb:iface:ru"),
            InlineKeyboardButton("English", callback_data="onb:iface:en"),
        ]
    ])


def kb_target_lang() -> InlineKeyboardMarkup:
    # Минимальный набор, как у тебя в онбординге на скринах
    # code — это то, что мы будем хранить в users.target_lang
    items = [
        ("Русский", "ru"),
        ("English", "en"),
        ("Français", "fr"),
        ("Español", "es"),
        ("Deutsch", "de"),
        ("Svenska", "sv"),
        ("Suomi", "fi"),
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

