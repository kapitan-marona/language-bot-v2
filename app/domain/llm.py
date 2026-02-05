# app/domain/llm.py
from __future__ import annotations
import os

from openai import OpenAI


def ask_openai_chat(system_prompt: str, messages: list[dict], model: str | None = None) -> str:
    """
    messages: [{"role": "user"/"assistant", "content": "..."}...]
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "⚠️ OPENAI_API_KEY не задан. Сейчас я работаю в режиме заглушки."

    client = OpenAI(api_key=api_key)
    mdl = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    resp = client.chat.completions.create(
        model=mdl,
        messages=[{"role": "system", "content": system_prompt}] + messages,
        temperature=0.7,
    )
    return (resp.choices[0].message.content or "").strip()
