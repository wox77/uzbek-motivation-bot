"""Gemini-powered Uzbek bot content with bounded concurrency and retries."""

from __future__ import annotations

import asyncio
import logging
import os
from functools import lru_cache

from google import genai
from google.genai import types

logger = logging.getLogger("uzbek-motivation-bot.gemini")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
_REQUEST_LIMITER = asyncio.Semaphore(2)
_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


@lru_cache(maxsize=1)
def _client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured")
    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=20_000),
    )


def _prompt(content_type: str, mood: str | None) -> str:
    rules = (
        "Write in simple, natural Uzbek using Latin script. Make the text original, "
        "clear, warm, calming, and hopeful, so the reader feels understood and more "
        "confident. Draw inspiration from broad, widely known ideas associated with "
        "respected thinkers, scientists, psychologists, and well-known books, then "
        "express those ideas in your own words. Never copy or closely paraphrase a "
        "specific passage. Do not invent quotations, authors, sources, research, or "
        "scientific claims, and do not attribute generated text to a real person or "
        "book. Avoid forced positivity or dismissing difficult feelings. Return only "
        "the finished text, without a title, explanation, or markdown."
    )
    if content_type == "mood":
        if not mood:
            raise ValueError("A mood is required for mood content")
        return (
            f"{rules}\n\nWrite 2 or 3 supportive sentences for a person feeling: {mood}. "
            "Acknowledge the feeling without minimizing it, offer one gentle practical "
            "thought, and avoid diagnoses or promises."
        )
    if content_type == "iqtibos":
        return (
            f"{rules}\n\nWrite one short, memorable original motivational thought. "
            "Do not include an author or source."
        )
    if content_type == "hazil":
        return (
            f"{rules}\n\nWrite one brief, friendly everyday joke in Uzbek. Keep it "
            "light and kind; do not mock a person or group."
        )
    if content_type == "sheriy":
        return (
            f"{rules}\n\nWrite an original short Uzbek poem of 4 to 6 lines. "
            "Do not imitate a known poet or quote existing lyrics."
        )
    raise ValueError(f"Unsupported Gemini content type: {content_type}")


def _generate_once(prompt: str) -> str:
    response = _client().models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.9,
            max_output_tokens=8192,
        ),
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response")
    if len(text) > 3000:
        text = text[:2997].rsplit(" ", 1)[0].rstrip() + "..."
    return text


async def generate_gemini_content(
    content_type: str,
    mood: str | None = None,
) -> str:
    """Generate one Uzbek response without blocking Telegram's event loop."""
    prompt = _prompt(content_type, mood)
    async with _REQUEST_LIMITER:
        for attempt in range(2):
            try:
                return await asyncio.to_thread(_generate_once, prompt)
            except Exception as error:
                status_code = getattr(error, "code", None)
                retryable = (
                    status_code is None or status_code in _RETRYABLE_STATUS_CODES
                )
                if not retryable or attempt == 1:
                    raise
                delay = 0.5 * (2**attempt)
                logger.warning(
                    "Gemini request failed (%s); retrying in %.1fs",
                    type(error).__name__,
                    delay,
                )
                await asyncio.sleep(delay)

    raise RuntimeError("Gemini generation failed after retries")
