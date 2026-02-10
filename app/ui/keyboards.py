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
            InlineKeyboardButton(
                LEVEL_GUIDE_BUTTON[L],
                callback_data="onb:level_help"
            )
        ],
    ]

    return InlineKeyboardMarkup(buttons)


def kb_level_guide_close(lang: str = "ru") -> InlineKeyboardMarkup:
    lang = lang if lang in ("ru", "en") else "ru"
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(
            LEVEL_GUIDE_CLOSE_BUTTON.get(lang, LEVEL_GUIDE_CLOSE_BUTTON["ru"]),
            callback_data="onb:level_help_close"
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
# Settings keyboards (NEW)
# callback prefix: set:...
# -------------------------

def kb_settings(
    lang: str,
    *,
    task_mode: str,
    translator_direction: str,
    translator_style: str,
    translator_output: str,
) -> InlineKeyboardMarkup:
    """
    task_mode: chat|translator
    translator_direction: ui_to_target|target_to_ui
    translator_style: casual|business
    translator_output: text|voice
    """
    lang = lang if lang in ("ru", "en") else "ru"

    # Toggle label
    if lang == "en":
        mode_label = "🟢 Translator: ON" if task_mode == "translator" else "⚪️ Translator: OFF"
        dir_label = "↔️ Direction"
        style_label = "🎭 Style"
        out_label = "🎙 Output"
        close_label = "✖️ Close"
    else:
        mode_label = "🟢 Переводчик: ВКЛ" if task_mode == "translator" else "⚪️ Переводчик: ВЫКЛ"
        dir_label = "↔️ Направление"
        style_label = "🎭 Стиль"
        out_label = "🎙 Вывод"
        close_label = "✖️ Закрыть"

    # Current values (small, readable)
    if lang == "en":
        dir_val = "UI → Target" if translator_direction == "ui_to_target" else "Target → UI"
        style_val = "Casual" if translator_style == "casual" else "Business"
        out_val = "Text" if translator_output == "text" else "Voice"
    else:
        dir_val = "Интерфейс → Язык" if translator_direction == "ui_to_target" else "Язык → Интерфейс"
        style_val = "Разговорный" if translator_style == "casual" else "Деловой"
        out_val = "Текст" if translator_output == "text" else "Голос"

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(mode_label, callback_data="set:mode:toggle")],
        [
            InlineKeyboardButton(f"{dir_label}: {dir_val}", callback_data="set:open:direction"),
        ],
        [
            InlineKeyboardButton(f"{style_label}: {style_val}", callback_data="set:open:style"),
        ],
        [
            InlineKeyboardButton(f"{out_label}: {out_val}", callback_data="set:open:output"),
        ],
        [InlineKeyboardButton(close_label, callback_data="set:close")],
    ])


def kb_translator_direction(lang: str, current: str) -> InlineKeyboardMarkup:
    lang = lang if lang in ("ru", "en") else "ru"
    current = current if current in ("ui_to_target", "target_to_ui") else "ui_to_target"

    if lang == "en":
        a = "UI → Target"
        b = "Target → UI"
        back = "← Back"
    else:
        a = "Интерфейс → Язык"
        b = "Язык → Интерфейс"
        back = "← Назад"

    a_mark = " ✅" if current == "ui_to_target" else ""
    b_mark = " ✅" if current == "target_to_ui" else ""

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(a + a_mark, callback_data="set:tdir:ui_to_target")],
        [InlineKeyboardButton(b + b_mark, callback_data="set:tdir:target_to_ui")],
        [InlineKeyboardButton(back, callback_data="set:back:settings")],
    ])


def kb_translator_style(lang: str, current: str) -> InlineKeyboardMarkup:
    lang = lang if lang in ("ru", "en") else "ru"
    current = current if current in ("casual", "business") else "casual"

    if lang == "en":
        a = "😎 Casual"
        b = "🧑‍💼 Business"
        back = "← Back"
    else:
        a = "😎 Разговорный"
        b = "🧑‍💼 Деловой"
        back = "← Назад"

    a_mark = " ✅" if current == "casual" else ""
    b_mark = " ✅" if current == "business" else ""

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(a + a_mark, callback_data="set:tstyle:casual")],
        [InlineKeyboardButton(b + b_mark, callback_data="set:tstyle:business")],
        [InlineKeyboardButton(back, callback_data="set:back:settings")],
    ])


def kb_translator_output(lang: str, current: str) -> InlineKeyboardMarkup:
    lang = lang if lang in ("ru", "en") else "ru"
    current = current if current in ("text", "voice") else "text"

    if lang == "en":
        a = "Text"
        b = "Voice"
        back = "← Back"
    else:
        a = "Текст"
        b = "Голос"
        back = "← Назад"

    a_mark = " ✅" if current == "text" else ""
    b_mark = " ✅" if current == "voice" else ""

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(a + a_mark, callback_data="set:tout:text")],
        [InlineKeyboardButton(b + b_mark, callback_data="set:tout:voice")],
        [InlineKeyboardButton(back, callback_data="set:back:settings")],
    ])
