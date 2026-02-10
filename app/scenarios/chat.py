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
        dub = int(user.get("dub_interface_for_low_levels") or 0)

        # 1️⃣ сохраняем юзера
        self.chat.add(ctx.user_id, "user", user_text)

        # 2️⃣ история
        msgs = self.chat.get_last_pairs(ctx.user_id, pairs=20)

        # 3️⃣ системка Мэтта
        system_prompt = get_system_prompt(
            style=style,
            level=level,
            interface_lang=il,
            target_lang=target,
            mode=mode,
            task_mode="chat",
            translator_cfg=None,
        )

        # 4️⃣ основной ответ
        reply = ask_openai_chat(system_prompt=system_prompt, messages=msgs)

        # 5️⃣ сохраняем
        self.chat.add(ctx.user_id, "assistant", reply)
        self.chat.trim_to_pairs(ctx.user_id, pairs=20)

        # 6️⃣ отправляем основной ответ
        await ctx.update.message.reply_text(reply, parse_mode="HTML")

        # ---------------------------------------------------
        # ⭐ НОВОЕ: ДУБЛЯЖ ДЛЯ A0/A1
        # ---------------------------------------------------
        if dub and level in ("A0", "A1") and il != target:

            translate_prompt = (
                f"Translate the following message to {il}. "
                f"Return ONLY translation.\n\n{reply}"
            )

            translated = ask_openai_chat(
                system_prompt="You are a translator.",
                messages=[{"role": "user", "content": translate_prompt}],
            )

            await ctx.update.message.reply_text(translated)

    async def voice_placeholder(self, ctx):
        await ctx.update.message.reply_text("🎙️ Voice скоро подключим. Пока текстом 🙂")
