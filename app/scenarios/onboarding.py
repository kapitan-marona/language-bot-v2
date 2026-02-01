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
    Step 5: choose level (next)
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

            # Пока промо-логику не применяем (подключим PromoArbiter позже),
            # но шаг должен двигаться дальше.
            _promo = None if low in no_words else raw

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

        # STEP 5: Level (пока заглушка — следующий коммит сделаем кнопки)
        if stage == "level_choose":
            await ctx.update.message.reply_text(t("choose_level_stub", il))
            return

        # Unknown state fallback (без кнопок и без языков интерфейса)
        await ctx.update.message.reply_text(t("onboarding_unknown_state", il))

    async def handle_callback(self, ctx):
        q = ctx.update.callback_query
        await q.answer()
        data = q.data or ""
        il = ctx.user.get("interface_lang", "ru")

        # STEP 1: interface language selected
        if data.startswith("onb:iface:"):
            lang = data.split(":")[-1]  # ru / en
            self.users.update_user(ctx.user_id, interface_lang=lang)

            # ✅ убрать кнопки у сообщения с выбором языка интерфейса
            try:
                await q.edit_message_reply_markup(reply_markup=None)
            except Exception:
                pass

            self.onb.set_stage(ctx.user_id, "promo_ask")
            await q.message.reply_text(t("ask_promo", lang))
            return

        # STEP 4: target language selected
        if data.startswith("onb:target:"):
            target = data.split(":")[-1]  # en/de/fi/...
            self.users.update_user(ctx.user_id, target_lang=target)

            # ✅ убрать кнопки у сообщения с выбором языка изучения
            try:
                await q.edit_message_reply_markup(reply_markup=None)
            except Exception:
                pass

            # Следующий шаг будет выбор уровня (кнопки добавим следующим коммитом)
            self.onb.set_stage(ctx.user_id, "level_choose")
            await q.message.reply_text(t("choose_level_stub", il))
            return

        # Unknown callback fallback (без кнопок)
        await q.message.reply_text(t("onboarding_unknown_state", il))

    async def voice_not_allowed(self, ctx):
        il = ctx.user.get("interface_lang", "ru")
        await ctx.update.message.reply_text(t("voice_not_in_onboarding", il))
