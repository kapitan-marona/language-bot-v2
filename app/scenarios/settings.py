from app.storage.users_repo import UsersRepo
from app.ui.texts import t
from app.ui.keyboards import (
    kb_settings,
    kb_translator_direction,
    kb_translator_style,
    kb_translator_output,
)


class SettingsScenario:
    def __init__(self):
        self.users = UsersRepo()

    def _get_settings_state(self, user: dict) -> dict:
        return {
            "task_mode": (user.get("task_mode") or "chat").lower(),
            "translator_direction": (user.get("translator_direction") or "ui_to_target").lower(),
            "translator_style": (user.get("translator_style") or "casual").lower(),
            "translator_output": (user.get("translator_output") or "text").lower(),
        }

    async def open(self, ctx):
        user = self.users.get_user(ctx.user_id) or (ctx.user or {})
        il = (user.get("interface_lang") or "ru").lower()
        s = self._get_settings_state(user)

        await ctx.update.message.reply_text(
            t("settings_title", il),
            reply_markup=kb_settings(
                il,
                task_mode=s["task_mode"],
                translator_direction=s["translator_direction"],
                translator_style=s["translator_style"],
                translator_output=s["translator_output"],
            ),
        )

    async def help(self, ctx):
        il = (ctx.user.get("interface_lang") or "ru")
        await ctx.update.message.reply_text(t("help", il))

    async def translator_on(self, ctx):
        self.users.update_user(ctx.user_id, task_mode="translator")
        il = (ctx.user.get("interface_lang") or "ru")
        await ctx.update.message.reply_text(t("translator_on", il))

    async def translator_off(self, ctx):
        self.users.update_user(ctx.user_id, task_mode="chat")
        il = (ctx.user.get("interface_lang") or "ru")
        await ctx.update.message.reply_text(t("translator_off", il))

    async def promo_placeholder(self, ctx):
        il = (ctx.user.get("interface_lang") or "ru")
        await ctx.update.message.reply_text(t("promo_stub", il))

    async def limit_reached(self, ctx, decision):
        il = (ctx.user.get("interface_lang") or "ru")
        await ctx.update.message.reply_text(t("limit_reached", il))

    async def handle_callback(self, ctx):
        q = ctx.update.callback_query
        await q.answer()

        data = q.data or ""
        user = self.users.get_user(ctx.user_id) or (ctx.user or {})
        il = (user.get("interface_lang") or "ru").lower()
        s = self._get_settings_state(user)

        # Close
        if data == "set:close":
            try:
                await q.message.delete()
            except Exception:
                pass
            return

        # Back to main settings
        if data == "set:back:settings":
            user = self.users.get_user(ctx.user_id) or (ctx.user or {})
            s = self._get_settings_state(user)
            await q.message.edit_text(
                t("settings_title", il),
                reply_markup=kb_settings(
                    il,
                    task_mode=s["task_mode"],
                    translator_direction=s["translator_direction"],
                    translator_style=s["translator_style"],
                    translator_output=s["translator_output"],
                ),
            )
            return

        # Toggle translator mode
        if data == "set:mode:toggle":
            new_mode = "chat" if s["task_mode"] == "translator" else "translator"
            self.users.update_user(ctx.user_id, task_mode=new_mode)

            user = self.users.get_user(ctx.user_id) or (ctx.user or {})
            s = self._get_settings_state(user)
            await q.message.edit_text(
                t("settings_title", il),
                reply_markup=kb_settings(
                    il,
                    task_mode=s["task_mode"],
                    translator_direction=s["translator_direction"],
                    translator_style=s["translator_style"],
                    translator_output=s["translator_output"],
                ),
            )
            return

        # Open submenus
        if data == "set:open:direction":
            await q.message.edit_text(
                t("settings_direction", il),
                reply_markup=kb_translator_direction(il, s["translator_direction"]),
            )
            return

        if data == "set:open:style":
            await q.message.edit_text(
                t("settings_tstyle", il),
                reply_markup=kb_translator_style(il, s["translator_style"]),
            )
            return

        if data == "set:open:output":
            await q.message.edit_text(
                t("settings_toutput", il),
                reply_markup=kb_translator_output(il, s["translator_output"]),
            )
            return

        # Apply values
        if data.startswith("set:tdir:"):
            v = data.split(":")[-1]
            if v in ("ui_to_target", "target_to_ui"):
                self.users.update_user(ctx.user_id, translator_direction=v)
            await self.handle_callback(ctx)  # refresh via back-to-settings path
            return

        if data.startswith("set:tstyle:"):
            v = data.split(":")[-1]
            if v in ("casual", "business"):
                self.users.update_user(ctx.user_id, translator_style=v)
            await self.handle_callback(ctx)
            return

        if data.startswith("set:tout:"):
            v = data.split(":")[-1]
            if v in ("text", "voice"):
                self.users.update_user(ctx.user_id, translator_output=v)
            await self.handle_callback(ctx)
            return

        # Default fallback: reopen settings
        await q.message.edit_text(
            t("settings_title", il),
            reply_markup=kb_settings(
                il,
                task_mode=s["task_mode"],
                translator_direction=s["translator_direction"],
                translator_style=s["translator_style"],
                translator_output=s["translator_output"],
            ),
        )

    async def debug_user(self, ctx):
        user = self.users.get_user(ctx.user_id) or (ctx.user or {})
        text = (
            f"user_id = {ctx.user_id}\n"
            f"level = {user.get('level')}\n"
            f"dub_interface_for_low_levels = {user.get('dub_interface_for_low_levels')}\n"
            f"interface_lang = {user.get('interface_lang')}\n"
            f"target_lang = {user.get('target_lang')}\n"
            f"task_mode = {user.get('task_mode')}\n"
            f"translator_direction = {user.get('translator_direction')}\n"
            f"translator_style = {user.get('translator_style')}\n"
            f"translator_output = {user.get('translator_output')}\n"
        )
        await ctx.update.message.reply_text(text)
