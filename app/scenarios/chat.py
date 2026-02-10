from app.storage.chat_repo import ChatRepo
from app.domain.llm import ask_openai_chat
from app.domain.prompt_templates import get_system_prompt


def _looks_like_mixed_language(text: str, target: str, ui: str) -> bool:
    # очень простой сигнал: если модель сама вставила явный перевод/две версии
    low = (text or "").lower()
    if "do you" in low and any(x in low for x in ["ты ", "вы ", "любишь", "предпочитаешь"]):
        return True
    if "translation:" in low or "перевод:" in low or "ui:" in low:
        return True
    return False


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

        # 1) сохраняем юзера
        self.chat.add(ctx.user_id, "user", user_text)

        # 2) история
        msgs = self.chat.get_last_pairs(ctx.user_id, pairs=20)

        # 3) системка Мэтта (TARGET-only)
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

        # 5) если модель всё равно намешала языки/переводы — “выровнять” одним коротким перегеном
        if _looks_like_mixed_language(reply, target=target, ui=il):
            repair_prompt = (
                f"Rewrite the message below so it is ONLY in the TARGET language ({target}). "
                f"No translation, no second language, no labels. Keep meaning.\n\n{reply}"
            )
            reply = ask_openai_chat(
                system_prompt="You are a strict rewriter.",
                messages=[{"role": "user", "content": repair_prompt}],
            )

        # 6) сохраняем и режем
        self.chat.add(ctx.user_id, "assistant", reply)
        self.chat.trim_to_pairs(ctx.user_id, pairs=20)

        # 7) отправляем TARGET-ответ
        await ctx.update.message.reply_text(reply, parse_mode="HTML")

        # 8) дубляж: переводим TARGET-ответ на UI (строго)
        if dub and level in ("A0", "A1") and il != target:
            translate_prompt = (
                f"Translate to {il}. Output ONLY the translation in {il}. "
                f"No extra text, no second language, no quotes.\n\n{reply}"
            )
            translated = ask_openai_chat(
                system_prompt="You are a strict translator. Output only the translation.",
                messages=[{"role": "user", "content": translate_prompt}],
            )
            await ctx.update.message.reply_text(translated)

    async def voice_placeholder(self, ctx):
        await ctx.update.message.reply_text("🎙️ Voice скоро подключим. Пока текстом 🙂")
