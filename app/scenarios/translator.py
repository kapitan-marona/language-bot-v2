from app.ui.texts import t


class TranslatorScenario:
    async def handle(self, ctx):
        il = ctx.user.get("interface_lang", "ru")
        # Translator is "machine": no emojis, no stickers.
        await ctx.update.message.reply_text(t("translator_stub", il))

    async def voice_placeholder(self, ctx):
        il = ctx.user.get("interface_lang", "ru")
        await ctx.update.message.reply_text(t("voice_translator_stub", il))
