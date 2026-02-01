from app.storage.onboarding_repo import OnboardingRepo
from app.storage.users_repo import UsersRepo
from app.ui.keyboards import kb_interface_lang
from app.ui.texts import t


class OnboardingScenario:
    """
    Minimal onboarding v1:

    Step 1: Interface language selection (buttons)
    Step 2: Promo code ask (text input: code or "нет"/"no")

    For now, after promo step we complete onboarding immediately.
    Full 8-step onboarding will be added next.
    """

    def __init__(self):
        self.onb = OnboardingRepo()
        self.users = UsersRepo()

    # =========================
    # START (/start)
    # =========================
    async def start(self, ctx):
        """
        Always restart onboarding from step 1.
        """
        self.onb.set_stage(ctx.user_id, "interface_lang")

        await ctx.update.message.reply_text(
            t("choose_interface_lang", "ru"),
            reply_markup=kb_interface_lang(),
        )

    # =========================
    # TEXT HANDLER (Onboarding)
    # =========================
    async def handle(self, ctx):
        """
        Called when onboarding is not completed yet
        and user sends a normal text message.
        """
        stage = (ctx.onboarding or {}).get("stage", "interface_lang")
        il = ctx.user.get("interface_lang", "ru")

        # -------------------------
        # STEP 1: Interface language
        # -------------------------
        if stage == "interface_lang":
            await ctx.update.message.reply_text(
                t("choose_interface_lang", il),
                reply_markup=kb_interface_lang(),
            )
            return

        # -------------------------
        # STEP 2: Promo ask (text)
        # -------------------------
        if stage == "promo_ask":
            raw = (ctx.update.message.text or "").strip()
            low = raw.lower()

            # User says "no promo"
            no_words = {"нет", "не", "неа", "нету", "no", "nope", "none"}

            if low in no_words:
                # Finish onboarding (temporary stub)
                self.onb.complete(ctx.user_id)

                await ctx.update.message.reply_text(
                    t("onboarding_done_stub", il)
                )
                return

            # User entered some promo code
            # (PromoArbiter will be подключён следующим шагом)
            self.onb.complete(ctx.user_id)

            await ctx.update.message.reply_text(
                t("promo_received_stub", il).format(code=raw)
            )
            return

        # -------------------------
        # FUTURE STEPS (fallback)
        # -------------------------
        await ctx.update.message.reply_text(
            t("onboarding_use_buttons", il),
            reply_markup=kb_interface_lang(),
        )

    # =========================
    # CALLBACK HANDLER (Buttons)
    # =========================
    async def handle_callback(self, ctx):
        """
        Handles inline button clicks during onboarding.
        """
        q = ctx.update.callback_query
        await q.answer()

        data = q.data or ""

        # -------------------------
        # Interface language selected
        # -------------------------
        if data.startswith("onb:iface:"):
            lang = data.split(":")[-1]  # ru / en

            # Save interface language
            self.users.update_user(ctx.user_id, interface_lang=lang)

            # Move to promo step
            self.onb.set_stage(ctx.user_id, "promo_ask")

            await q.message.reply_text(
                t("ask_promo", lang)
            )
            return

        # Unknown callback fallback
        il = ctx.user.get("interface_lang", "ru")
        await q.message.reply_text(
            t("onboarding_use_buttons", il),
            reply_markup=kb_interface_lang(),
        )

    # =========================
    # VOICE NOT ALLOWED IN ONBOARDING
    # =========================
    async def voice_not_allowed(self, ctx):
        il = ctx.user.get("interface_lang", "ru")
        await ctx.update.message.reply_text(
            t("voice_not_in_onboarding", il)
        )
