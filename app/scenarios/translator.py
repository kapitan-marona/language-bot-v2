from app.domain.llm import ask_openai_chat
from app.domain.prompt_templates import get_system_prompt
from app.storage.users_repo import UsersRepo
from app.storage.translator_repo import TranslatorRepo
from app.ui.texts import t
from app.ui.keyboards import kb_translator_panel


class TranslatorScenario:
    def __init__(self):
        self.users = UsersRepo()
        self.tr = TranslatorRepo()

    def _render_direction_label(self, il: str, direction_db: str) -> str:
        if direction_db == "target_to_ui":
            return t("translator_direction_target_to_ui", il)
        return t("translator_direction_ui_to_target", il)

    def _render_output_label(self, il: str, output: str) -> str:
        if output == "voice":
            return t("translator_output_voice", il)
        return t("translator_output_text", il)

    async def enter(self, ctx):
        user = self.users.get_user(ctx.user_id) or (ctx.user or {})
        il = (user.get("interface_lang") or "ru").lower()
        direction_db = (user.get("translator_direction") or "ui_to_target").lower()
        output = (user.get("translator_output") or "text").lower()

        text = t("translator_panel_title", il).format(
            direction=self._render_direction_label(il, direction_db),
            output=self._render_output_label(il, output),
        )
        await ctx.update.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=kb_translator_panel(il, direction_db, output),
        )

    async def handle_callback(self, ctx):
        q = ctx.update.callback_query
        await q.answer()

        data = q.data or ""
        user = self.users.get_user(ctx.user_id) or (ctx.user or {})
        il = (user.get("interface_lang") or "ru").lower()

        if data == "tr:off":
            self.users.update_user(ctx.user_id, task_mode="chat")
            await q.message.edit_text(t("translator_off", il))
            return

        if data == "tr:dir:toggle":
            cur = (user.get("translator_direction") or "ui_to_target").lower()
            new = "target_to_ui" if cur == "ui_to_target" else "ui_to_target"
            self.users.update_user(ctx.user_id, translator_direction=new)
            user = self.users.get_user(ctx.user_id) or user
            direction_db = (user.get("translator_direction") or new).lower()
            output = (user.get("translator_output") or "text").lower()

            text = t("translator_panel_title", il).format(
                direction=self._render_direction_label(il, direction_db),
                output=self._render_output_label(il, output),
            )
            await q.message.edit_text(
                text,
                parse_mode="HTML",
                reply_markup=kb_translator_panel(il, direction_db, output),
            )
            return

        if data.startswith("tr:out:"):
            v = data.split(":")[-1]
            if v in ("text", "voice"):
                self.users.update_user(ctx.user_id, translator_output=v)
            user = self.users.get_user(ctx.user_id) or user
            direction_db = (user.get("translator_direction") or "ui_to_target").lower()
            output = (user.get("translator_output") or "text").lower()

            text = t("translator_panel_title", il).format(
                direction=self._render_direction_label(il, direction_db),
                output=self._render_output_label(il, output),
            )
            await q.message.edit_text(
                text,
                parse_mode="HTML",
                reply_markup=kb_translator_panel(il, direction_db, output),
            )
            return

    async def handle(self, ctx):
        user_text = (ctx.update.message.text or "").strip()
        if not user_text:
            return

        user = ctx.user or {}
        il = (user.get("interface_lang") or "ru").lower()
        target = (user.get("target_lang") or "en").lower()

        direction_db = (user.get("translator_direction") or "ui_to_target").lower()
        output = (user.get("translator_output") or "text").lower()

        direction = "ui→target" if direction_db == "ui_to_target" else "target→ui"

        # Separate history for translator
        self.tr.add(ctx.user_id, "user", user_text)
        self.tr.trim_to_pairs(ctx.user_id, pairs=20)

        system_prompt = get_system_prompt(
            style="casual",          # irrelevant for translator, keep stable
            level="B1",              # irrelevant for translator, keep stable
            interface_lang=il,
            target_lang=target,
            mode=output,             # text|voice
            task_mode="translator",
            translator_cfg={
                "direction": direction,
                "output": output,
                "style": "neutral",
            },
        )

        reply = ask_openai_chat(
            system_prompt=system_prompt,
            messages=[{"role": "user", "content": user_text}],
        )

        self.tr.add(ctx.user_id, "assistant", reply)
        self.tr.trim_to_pairs(ctx.user_id, pairs=20)

        await ctx.update.message.reply_text(reply)

    async def voice_placeholder(self, ctx):
        il = (ctx.user.get("interface_lang") or "ru").lower()
        await ctx.update.message.reply_text(t("voice_translator_stub", il))
