from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def kb_interface_lang() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Русский", callback_data="onb:iface:ru"),
            InlineKeyboardButton("English", callback_data="onb:iface:en"),
        ]
    ])
