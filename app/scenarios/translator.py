from app.domain.llm import ask_openai_chat
from app.domain.prompt_templates import get_system_prompt
from app.storage.translator_repo import TranslatorRepo


class TranslatorScenario:
    def __init__(self):
        self.tr = TranslatorRepo()

    async def handle(self, ctx):
        user_text = (ctx.update.message.text or "").strip()
        if not user_text:
            return

        user = ctx.user or {}
        il = (user.get("interface_lang") or "ru").lower()
        target = (user.get("target_lang") or "en").lower()
        level = (user.get("level") or "A2").upper()
        style = (user.get("style") or "casual").lower()
        mode = (user.get("input_mode") or "text").lower()

        direction_db = (user.get("translator_direction") or "ui_to_target").lower()
        translator_style = (user.get("translator_style") or "casual").lower()
        translator_output = (user.get("translator_output") or "text").lower()

        # Map DB value -> system prompt expected values
        direction = "ui→target" if direction_db == "ui_to_target" else "target→ui"

        # Save translator input (separate history)
        self.tr.add(ctx.user_id, "user", user_text)
        self.tr.trim_to_pairs(ctx.user_id, pairs=20)

        system_prompt = get_system_prompt(
            style=style,                 # persona irrelevant in translator, but keep signature stable
            level=level,
            interface_lang=il,
            target_lang=target,
            mode=mode,
            task_mode="translator",
            translator_cfg={
                "direction": direction,
                "output": translator_output,
                "style": translator_style,
            },
        )

        # Translator should be stateless: we do NOT pass chat history
        reply = ask_openai_chat(
            system_prompt=system_prompt,
            messages=[{"role": "user", "content": user_text}],
        )

        # Save output
        self.tr.add(ctx.user_id, "assistant", reply)
        self.tr.trim_to_pairs(ctx.user_id, pairs=20)

        await ctx.update.message.reply_text(reply)

    async def voice_placeholder(self, ctx):
        # Пока не подключали STT/TTS: просто заглушка, но отдельно от chat
        await ctx.update.message.reply_text("TRANSLATOR MODE (voice): stub. STT/TTS will be added soon.")
