from app.storage.onboarding_repo import OnboardingRepo
from app.storage.users_repo import UsersRepo
from app.ui.keyboards import kb_interface_lang
from app.ui.texts import t


class OnboardingScenario:
    def __init__(self):
        self.onb = OnboardingRepo()
        self.users = UsersRepo()

    async def start(self, ctx):
        self.onb.set_stage(ctx.user_id, "interface_lang")
        await ctx.update.message.reply_text(
            t("choose_interface_lang", "ru"),
            reply_markup=kb_interface_lang(),
        )

    async def handle(self, ctx):
        stage = ctx.onboarding["stage"]
        il = ctx.user.get("interface_lang", "ru")
        # For now: if user typed instead of pressing buttons, re-show
        await ctx.update.message.reply_text(
            t("onboarding_use_buttons", il),
            reply_markup=kb_interface_lang(),
        )

    async def handle_callback(self, ctx):
        q = ctx.update.callback_query
        await q.answer()
        data = q.data or ""

        # Step 1: interface lang
        if data.startswith("onb:iface:"):
            lang = data.split(":")[-1]  # ru/en
            self.users.update_user(ctx.user_id, interface_lang=lang)
            self.onb.set_stage(ctx.user_id, "promo_ask")
            await q.message.reply_text(t("ask_promo", lang))
            return

        # Later steps will be added as we implement each stage.
        await q.message.reply_text(t("onboarding_use_buttons", ctx.user.get("interface_lang", "ru")))

    async def voice_not_allowed(self, ctx):
        il = ctx.user.get("interface_lang", "ru")
        await ctx.update.message.reply_text(t("voice_not_in_onboarding", il))
