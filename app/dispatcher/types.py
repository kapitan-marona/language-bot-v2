from dataclasses import dataclass
from telegram import Update
from telegram.ext import ContextTypes


@dataclass
class DispatchContext:
    update: Update
    tg: ContextTypes.DEFAULT_TYPE
    user_id: int
    user: dict
    onboarding: dict
