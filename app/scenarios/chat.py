from app.storage.chat_repo import ChatRepo
from app.domain.llm import ask_openai_chat
from app.domain.prompt_templates import get_system_prompt


class ChatScenario:
    def __init__(self):
        self.chat = ChatRepo()

    async def handle(self, ctx):
        user_text = (ctx.update.message.text or "").strip()
        if not user_text:
            return

        user = ctx.user or {}
        il = (user.get("interface_lang") or "ru").lower()
        target = (user.get("target_lang") or "en").lower()
        level = (user.get("level") or "A2").upper()
        style = (user.get("style") or "casual").lower()
        mode = (user.get("mode") or "text").lower()

        # 1) сохраняем юзера
        self.chat.add(ctx.user_id, "user", user_text)

        # 2) берём историю (20 пар = 40 сообщений)
        msgs = self.chat.get_last_pairs(ctx.user_id, pairs=20)

        # 3) системка Мэтта
        system_prompt = get_system_prompt(
            style=style,
            level=level,
            interface_lang=il,
            target_lang=target,
            mode=mode,
            task_mode="chat",
            translator_cfg=None,
        )

        # 4) ответ модели
        reply = ask_openai_chat(system_prompt=system_prompt, messages=msgs)

        # 5) сохраняем и режем
        self.chat.add(ctx.user_id, "assistant", reply)
        self.chat.trim_to_pairs(ctx.user_id, pairs=20)

        await ctx.update.message.reply_text(reply, parse_mode="HTML")

    async def voice_placeholder(self, ctx):
        await ctx.update.message.reply_text("🎙️ Voice скоро подключим. Пока текстом 🙂")
