from app.storage.onboarding_repo import OnboardingRepo
from app.storage.users_repo import UsersRepo
from app.ui.keyboards import kb_interface_lang, kb_target_lang, kb_level, kb_dup_interface
from app.ui.texts import t


class OnboardingScenario:
    """
    Onboarding (step-by-step):

    Step 1: interface language (buttons)
    Step 2: promo ask (text)
    Step 3: welcome message
    Step 4: choose target language (buttons)
    Step 5: choose level (buttons + help)
    Step 6: if A0/A1 -> ask duplication (buttons)
    Step 7: choose style (next commit)
    Step 8: final message + start chat (later)
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

        # STEP 1
        if stage == "interface_lang":
            await ctx.update.message.reply_text(
                t("choose_interface_lang", il),
                reply_markup=kb_interface_lang(),
            )
            return

        # STEP 2
        if stage == "promo_ask":
            raw = (ctx.update.message.text or "").strip()
            low = raw.lower()

            no_words = {"нет", "не", "неа", "нету", "no", "nope", "none"}
            _promo = None if low in no_words else raw
            # PromoArbiter подключим позже

            self.onb.set_stage(ctx.user_id, "target_lang")
            await ctx.update.message.reply_text(t("welcome_after_promo", il))
            await ctx.update.message.reply_text(
                t("choose_target_lang", il),
                reply_markup=kb_target_lang(),
            )
            return

        # STEP 4
        if stage == "target_lang":
            await ctx.update.message.reply_text(
                t("choose_target_lang", il),
                reply_markup=kb_target_lang(),
            )
            return

        # STEP 5
        if stage == "level_choose":
            await ctx.update.message.reply_text(
                t("choose_level", il),
                reply_markup=kb_level(),
            )
            return

        # STEP 6
        if stage == "dup_choose":
            await ctx.update.message.reply_text(
                t("ask_dup_interface", il),
                reply_markup=kb_dup_interface(),
            )
            return

        # STEP 7 (пока заглушка)
        if stage == "style_choose":
            await ctx.update.message.reply_text(t("choose_style_stub", il))
            return

        # Unknown state fallback
        await ctx.update.message.reply_text(t("onboarding_unknown_state", il))

    async def handle_callback(self, ctx):
        q = ctx.update.callback_query
        await q.answer()
        data = q.data or ""
        il = ctx.user.get("interface_lang", "ru")

        # STEP 1: interface lang
        if data.startswith("onb:iface:"):
            lang = data.split(":")[-1]  # ru/en
            self.users.update_user(ctx.user_id, interface_lang=lang)

            # hide buttons
            try:
                await q.edit_message_reply_markup(reply_markup=None)
            except Exception:
                pass

            self.onb.set_stage(ctx.user_id, "promo_ask")
            await q.message.reply_text(t("ask_promo", lang))
            return

        # STEP 4: target language
        if data.startswith("onb:target:"):
            target = data.split(":")[-1]
            self.users.update_user(ctx.user_id, target_lang=target)

            # hide buttons
            try:
                await q.edit_message_reply_markup(reply_markup=None)
            except Exception:
                pass

            self.onb.set_stage(ctx.user_id, "level_choose")
            await q.message.reply_text(
                t("choose_level", il),
                reply_markup=kb_level(),
            )
            return

        # STEP 5: level help
        if data == "onb:level_help":
            # Не убираем клавиатуру — это не выбор, а подсказка
            await q.message.reply_text(t("level_help", il))
            return

        # STEP 5: level selected
        if data.startswith("onb:level:"):
            level = data.split(":")[-1]  # A0..C2
            self.users.update_user(ctx.user_id, level=level)

            # hide buttons
            try:
                await q.edit_message_reply_markup(reply_markup=None)
            except Exception:
                pass

            if level in {"A0", "A1"}:
                self.onb.set_stage(ctx.user_id, "dup_choose")
                await q.message.reply_text(
                    t("ask_dup_interface", il),
                    reply_markup=kb_dup_interface(),
                )
                return

            # A2+ -> next step: style (будет в следующем коммите)
            self.onb.set_stage(ctx.user_id, "style_choose")
            await q.message.reply_text(t("choose_style_stub", il))
            return

        # STEP 6: duplication selected
        if data.startswith("onb:dub:"):
            v = data.split(":")[-1]  # yes/no
            dub = 1 if v == "yes" else 0
            self.users.update_user(ctx.user_id, dub_interface_for_low_levels=dub)

            # hide buttons
            try:
                await q.edit_message_reply_markup(reply_markup=None)
            except Exception:
                pass

            # next step: style (следующий коммит)
            self.onb.set_stage(ctx.user_id, "style_choose")
            await q.message.reply_text(t("choose_style_stub", il))
            return

        # Unknown callback fallback
        await q.message.reply_text(t("onboarding_unknown_state", il))

    async def voice_not_allowed(self, ctx):
        il = ctx.user.get("interface_lang", "ru")
        await ctx.update.message.reply_text(t("voice_not_in_onboarding", il))
