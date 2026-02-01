from telegram import Update
from telegram.ext import ContextTypes

from app.storage.users_repo import UsersRepo
from app.storage.onboarding_repo import OnboardingRepo
from app.domain.usage_gate import UsageGate
from app.scenarios.onboarding import OnboardingScenario
from app.scenarios.chat import ChatScenario
from app.scenarios.translator import TranslatorScenario
from app.scenarios.settings import SettingsScenario
from app.dispatcher.types import DispatchContext


class Dispatcher:
    def __init__(self):
        self.users = UsersRepo()
        self.onboarding_repo = OnboardingRepo()
        self.usage_gate = UsageGate()

        self.onboarding = OnboardingScenario()
        self.chat = ChatScenario()
        self.translator = TranslatorScenario()
        self.settings = SettingsScenario()

    async def _build_ctx(self, update: Update, tg: ContextTypes.DEFAULT_TYPE) -> DispatchContext:
        user_id = update.effective_user.id
        self.users.ensure_user(user_id)
        user = self.users.get_user(user_id)
        onboarding = self.onboarding_repo.get(user_id)
        return DispatchContext(update=update, tg=tg, user_id=user_id, user=user, onboarding=onboarding)

    async def handle_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        ctx = await self._build_ctx(update, context)
        text = update.message.text.strip()

        # System commands priority
        if text.startswith("/start"):
            return await self.onboarding.start(ctx)

        if text.startswith("/help"):
            return await self.settings.help(ctx)

        if text.startswith("/settings"):
            return await self.settings.open(ctx)

        if text.startswith("/translator_on"):
            return await self.settings.translator_on(ctx)

        if text.startswith("/translator_off"):
            return await self.settings.translator_off(ctx)

        if text.startswith("/promo"):
            # We'll wire PromoScenario later; for now show placeholder
            return await self.settings.promo_placeholder(ctx)

        # Fallback: show help
        return await self.settings.help(ctx)

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        ctx = await self._build_ctx(update, context)

        # Onboarding capture
        if not ctx.onboarding or int(ctx.onboarding["completed"]) == 0:
            return await self.onboarding.handle(ctx)

        # Usage gate (counts all user requests in any mode)
        decision = self.usage_gate.can_consume(ctx.user_id)
        if not decision.ok:
            return await self.settings.limit_reached(ctx, decision)

        # Route by task_mode
        if ctx.user.get("task_mode") == "translator":
            self.usage_gate.consume(ctx.user_id)
            return await self.translator.handle(ctx)

        # default chat
        self.usage_gate.consume(ctx.user_id)
        return await self.chat.handle(ctx)

    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        ctx = await self._build_ctx(update, context)

        if not ctx.onboarding or int(ctx.onboarding["completed"]) == 0:
            return await self.onboarding.voice_not_allowed(ctx)

        decision = self.usage_gate.can_consume(ctx.user_id)
        if not decision.ok:
            return await self.settings.limit_reached(ctx, decision)

        # For now: placeholder (we will add STT/TTS later)
        self.usage_gate.consume(ctx.user_id)
        if ctx.user.get("task_mode") == "translator":
            return await self.translator.voice_placeholder(ctx)
        return await self.chat.voice_placeholder(ctx)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        ctx = await self._build_ctx(update, context)

        # Onboarding callbacks should be handled during onboarding
        if not ctx.onboarding or int(ctx.onboarding["completed"]) == 0:
            return await self.onboarding.handle_callback(ctx)

        # Otherwise settings callbacks (later)
        return await self.settings.handle_callback(ctx)
