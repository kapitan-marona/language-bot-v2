from app.storage.onboarding_repo import OnboardingRepo
from app.storage.users_repo import UsersRepo
from app.ui.keyboards import kb_interface_lang, kb_target_lang
from app.ui.texts import t


class OnboardingScenario:
    """
    Onboarding (step-by-step, expanding):

    Step 1: interface language (buttons)
    Step 2: promo ask (text: code or "нет"/"no")
    Step 3: welcome message
    Step 4: choose target language (buttons)

    Next steps (later):
    Step 5: choose level
    Step 6: duplicate interface for A0/A1
    Step 7: choose style
    Step 8: final message + start chat
    """

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
        stage = (ctx.onboarding or {}).get("stage", "interface_lang")
        il = ctx.user.get("interface_lang", "ru")

        # STEP 1: Interface language selection
        if stage == "interface_lang":
            await ctx.update.message.reply_text(
                t("choose_interface_lang", il),
                reply_markup=kb_interface_lang(),
            )
            return

        # STEP 2: Promo ask (text input)
        if stage == "promo_ask":
            raw = (ctx.update.message.text or "").strip()
            low = raw.lower()

            no_words = {"нет", "не", "неа", "нету", "no", "nope", "none"}
            # Пока промо-логику не применяем (PromoArbiter будет позже),
            # но шаг онбординга должен идти дальше.
            # В будущем здесь будет apply_promo(raw).
            _ = raw  # placeholder, чтобы не терять смысл

            # Переходим к шагу 3–4: welcome + выбор языка
            self.onb.set_stage(ctx.user_id, "target_lang")

            await ctx.update.message.reply_text(t("welcome_after_promo", il))
            await ctx.update.message.reply_text(
                t("choose_target_lang", il),
                reply_markup=kb_target_lang(),
            )
            return

        # STEP 4: Waiting for target language via buttons
        if stage == "target_lang":
            await ctx.update.message.reply_text(
                t("choose_target_lang", il),
                reply_markup=kb_target_lang(),
            )
            return

        # Fallback
        await ctx.update.message.reply_text(
            t("onboarding_use_buttons", il),
            reply_markup=kb_interface_lang(),
        )

    async def handle_callback(self, ctx):
        q = ctx.update.callback_query
        await q.answer()
        data = q.data or ""
        il = ctx.user.get("interface_lang", "ru")

        # STEP 1: interface language selected
        if data.startswith("onb:iface:"):
            lang = data.split(":")[-1]  # ru / en
            self.users.update_user(ctx.user_id, interface_lang=lang)
            self.onb.set_stage(ctx.user_id, "promo_ask")
            await q.message.reply_text(t("ask_promo", lang))
            return

        # STEP 4: target language selected
        if data.startswith("onb:target:"):
            target = data.split(":")[-1]  # en/de/fi/...
            self.users.update_user(ctx.user_id, target_lang=target)

            # Следующий шаг будет выбор уровня
            self.onb.set_stage(ctx.user_id, "level_choose")

            await q.message.reply_text(t("target_lang_saved_stub", il))
            return

        # Unknown callback
        await q.message.reply_text(
            t("onboarding_use_buttons", il),
            reply_markup=kb_interface_lang(),
        )

    async def voice_not_allowed(self, ctx):
        il = ctx.user.get("interface_lang", "ru")
        await ctx.update.message.reply_text(t("voice_not_in_onboarding", il))
