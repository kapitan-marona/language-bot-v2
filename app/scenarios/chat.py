from app.storage.chat_repo import ChatRepo
from app.ui.texts import t


class ChatScenario:
    def __init__(self):
        self.chat = ChatRepo()

    async def handle(self, ctx):
        il = ctx.user.get("interface_lang", "ru")
        user_text = ctx.update.message.text

        # Save user msg
        self.chat.add(ctx.user_id, "user", user_text)

        # TODO: replace with OpenAI call using last 20 pairs
        reply = t("chat_stub_reply", il)

        self.chat.add(ctx.user_id, "assistant", reply)
        self.chat.trim_to_pairs(ctx.user_id, pairs=20)

        await ctx.update.message.reply_text(reply)

    async def voice_placeholder(self, ctx):
        il = ctx.user.get("interface_lang", "ru")
        await ctx.update.message.reply_text(t("voice_stub", il))
