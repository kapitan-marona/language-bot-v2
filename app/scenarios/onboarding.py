from app.storage.onboarding_repo import OnboardingRepo
from app.storage.users_repo import UsersRepo
from app.ui.keyboards import (
    kb_interface_lang,
    kb_target_lang,
    kb_level,
    kb_level_guide_close,
    kb_dup_interface,
    kb_style,
)
from app.ui.texts import t
from app.ui.levels_texts import get_level_guide
from app.domain.prompt_templates import START_MESSAGE, MATT_INTRO, pick_intro_question, PROMO_ASK


class OnboardingScenario:
    def __init__(self):
        self.onb = OnboardingRepo()
        self.users = UsersRepo()

    async def _safe_delete(self, msg):
        try:
            await msg.delete()
        except Exception:
            pass

    async def start(self, ctx):
        self.onb.set_stage(ctx.user_id, "interface_lang")
        await ctx.update.message.reply_text(
            t("choose_interface_lang", "ru"),
            reply_markup=kb_interface_lang(),
        )

    async def handle(self, ctx):
        stage = (ctx.onboarding or {}).get("stage", "interface_lang")
        il = ctx.user.get("interface_lang", "ru")

        if stage == "interface_lang":
            await ctx.update.message.reply_text(
                t("choose_interface_lang", il),
                reply_markup=kb_interface_lang(),
            )
            return

        if stage == "promo_ask":
            # promo вводим текстом; применим позже через PromoArbiter
            self.onb.set_stage(ctx.user_id, "target_lang")

            # ✅ стартовое сообщение из prompt_templates
            msg = START_MESSAGE.get(il, START_MESSAGE["ru"])
            await ctx.update.message.reply_text(msg)

            await ctx.update.message.reply_text(
                t("choose_target_lang", il),
                reply_markup=kb_target_lang(),
            )
            return

        if stage == "target_lang":
            await ctx.update.message.reply_text(
                t("choose_target_lang", il),
                reply_markup=kb_target_lang(),
            )
            return

        if stage == "level_choose":
            await ctx.update.message.reply_text(
                t("choose_level", il),
                reply_markup=kb_level(il),
            )
            return

        if stage == "dup_choose":
            await ctx.update.message.reply_text(
                t("ask_dup_interface", il),
                reply_markup=kb_dup_interface(il),
            )
            return

        if stage == "style_choose":
            await ctx.update.message.reply_text(
                t("choose_style", il),
                reply_markup=kb_style(il),
            )
            return

        await ctx.update.message.reply_text(t("onboarding_unknown_state", il))

    async def handle_callback(self, ctx):
        q = ctx.update.callback_query
        await q.answer()

        data = q.data or ""
        il = ctx.user.get("interface_lang", "ru")

        # Step 1: interface language
        if data.startswith("onb:iface:"):
            lang = data.split(":")[-1]
            self.users.update_user(ctx.user_id, interface_lang=lang)

            await self._safe_delete(q.message)

            self.onb.set_stage(ctx.user_id, "promo_ask")
            await q.message.chat.send_message(PROMO_ASK.get(lang, PROMO_ASK["ru"]))
            return

        # Step 4: target language
        if data.startswith("onb:target:"):
            target = data.split(":")[-1]
            self.users.update_user(ctx.user_id, target_lang=target)

            await self._safe_delete(q.message)

            self.onb.set_stage(ctx.user_id, "level_choose")
            await q.message.chat.send_message(
                t("choose_level", il),
                reply_markup=kb_level(il),
            )
            return

        # Step 5: level guide
        if data == "onb:level_help":
            guide_text = get_level_guide(il)
            await q.message.chat.send_message(
                guide_text,
                reply_markup=kb_level_guide_close(il),
                parse_mode="Markdown",
            )
            return

        if data == "onb:level_help_close":
            await self._safe_delete(q.message)
            return

        # Step 5: level selected
        if data.startswith("onb:level:"):
            level = data.split(":")[-1]
            self.users.update_user(ctx.user_id, level=level)

            await self._safe_delete(q.message)

            if level in {"A0", "A1"}:
                self.onb.set_stage(ctx.user_id, "dup_choose")
                await q.message.chat.send_message(
                    t("ask_dup_interface", il),
                    reply_markup=kb_dup_interface(il),
                )
                return

            self.onb.set_stage(ctx.user_id, "style_choose")
            await q.message.chat.send_message(
                t("choose_style", il),
                reply_markup=kb_style(il),
            )
            return

        # Step 5: level done
        if data == "onb:level_done":
            user = self.users.get_user(ctx.user_id)
            level = (user or {}).get("level")

            if not level:
                await q.message.chat.send_message(
                    t("choose_level", il),
                    reply_markup=kb_level(il),
                )
                return

            await self._safe_delete(q.message)

            if level in {"A0", "A1"}:
                self.onb.set_stage(ctx.user_id, "dup_choose")
                await q.message.chat.send_message(
                    t("ask_dup_interface", il),
                    reply_markup=kb_dup_interface(il),
                )
                return

            self.onb.set_stage(ctx.user_id, "style_choose")
            await q.message.chat.send_message(
                t("choose_style", il),
                reply_markup=kb_style(il),
            )
            return

        # Step 6: duplication selected
        if data.startswith("onb:dub:"):
            v = data.split(":")[-1]
            dub = 1 if v == "yes" else 0
            self.users.update_user(ctx.user_id, dub_interface_for_low_levels=dub)

            await self._safe_delete(q.message)

            self.onb.set_stage(ctx.user_id, "style_choose")
            await q.message.chat.send_message(
                t("choose_style", il),
                reply_markup=kb_style(il),
            )
            return

        # Step 7–8: style selected -> complete onboarding + intro + question
        if data.startswith("onb:style:"):
            style = data.split(":")[-1]  # casual|business
            self.users.update_user(ctx.user_id, style=style)

            await self._safe_delete(q.message)

            # ✅ complete onboarding
            self.onb.complete(ctx.user_id)

            # Fetch latest user settings for question
            user = self.users.get_user(ctx.user_id) or {}
            target = (user.get("target_lang") or "en").lower()
            level = (user.get("level") or "A2").upper()

            # 1) Matt intro in UI language
            intro = MATT_INTRO.get(il, MATT_INTRO["ru"])
            await q.message.chat.send_message(intro)

            # 2) First question in target language
            first_q = pick_intro_question(level=level, style=style, lang=target)
            await q.message.chat.send_message(first_q)
            return

        await q.message.chat.send_message(t("onboarding_unknown_state", il))

    async def voice_not_allowed(self, ctx):
        il = ctx.user.get("interface_lang", "ru")
        await ctx.update.message.reply_text(t("voice_not_in_onboarding", il))
