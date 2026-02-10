from app.storage.users_repo import UsersRepo
from app.ui.texts import t
from app.scenarios.translator import TranslatorScenario


class SettingsScenario:
    def __init__(self):
        self.users = UsersRepo()
        self.translator = TranslatorScenario()

    async def open(self, ctx):
        user = self.users.get_user(ctx.user_id) or (ctx.user or {})
        il = (user.get("interface_lang") or "ru").lower()

        # ✅ Settings hidden in translator mode
        if (user.get("task_mode") or "chat") == "translator":
            await ctx.update.message.reply_text(t("translator_settings_blocked", il))
            return

        await ctx.update.message.reply_text(t("settings_stub", il))

    async def help(self, ctx):
        il = (ctx.user.get("interface_lang") or "ru")
        await ctx.update.message.reply_text(t("help", il))

    async def translator_on(self, ctx):
        self.users.update_user(ctx.user_id, task_mode="translator")
        # show translator panel
        await self.translator.enter(ctx)

    async def translator_off(self, ctx):
        self.users.update_user(ctx.user_id, task_mode="chat")
        il = ctx.user.get("interface_lang", "ru")
        await ctx.update.message.reply_text(t("translator_off", il))

    async def set_text_mode(self, ctx):
        self.users.update_user(ctx.user_id, input_mode="text")
        il = (ctx.user.get("interface_lang") or "ru")
        await ctx.update.message.reply_text(t("input_mode_text", il))

    async def set_voice_mode(self, ctx):
        self.users.update_user(ctx.user_id, input_mode="voice")
        il = (ctx.user.get("interface_lang") or "ru")
        await ctx.update.message.reply_text(t("input_mode_voice", il))

    async def promo_placeholder(self, ctx):
        il = ctx.user.get("interface_lang", "ru")
        await ctx.update.message.reply_text(t("promo_stub", il))

    async def limit_reached(self, ctx, decision):
        il = ctx.user.get("interface_lang", "ru")
        await ctx.update.message.reply_text(t("limit_reached", il))

    async def handle_callback(self, ctx):
        il = ctx.user.get("interface_lang", "ru")
        await ctx.update.callback_query.answer()
        await ctx.update.callback_query.message.reply_text(t("settings_stub", il))

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
            f"translator_output = {user.get('translator_output')}\n"
            f"input_mode = {user.get('input_mode')}\n"
        )
        await ctx.update.message.reply_text(text)
