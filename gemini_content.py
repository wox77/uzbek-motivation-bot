"""Gemini-powered Uzbek bot content with bounded concurrency and retries."""

from __future__ import annotations

import asyncio
import logging
import os
import re
from functools import lru_cache

from google import genai
from google.genai import types

logger = logging.getLogger("uzbek-motivation-bot.gemini")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
_REQUEST_LIMITER = asyncio.Semaphore(2)
_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
_MAX_CHARS = {
    "mood": 360,
    "iqtibos": 180,
    "hazil": 180,
    "sheriy": 300,
}


class InvalidGeneratedContent(ValueError):
    """Raised when Gemini ignores the requested content format."""


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
        "clear, and respectful. Follow the requested content type exactly; do not "
        "combine it with another type. Where relevant, draw on broad, widely known "
        "ideas associated with respected thinkers, scientists, psychologists, and "
        "well-known books, expressed in your own words. Never copy or closely "
        "paraphrase a specific passage. Do not invent quotations, authors, sources, "
        "research, or scientific claims, and do not attribute generated text to a real "
        "person or book. Avoid forced positivity or dismissing difficult feelings. "
        "Return only the finished text, without a title, explanation, or markdown."
    )
    if content_type == "mood":
        if not mood:
            raise ValueError("A mood is required for mood content")
        return (
            f"{rules}\n\nWrite exactly 2 or 3 short supportive sentences for a person "
            f"feeling: {mood}. Keep the response under 360 characters. "
            "Acknowledge the feeling without minimizing it, offer one gentle practical "
            "thought, and avoid diagnoses or promises. Do not add a joke or a second topic."
        )
    if content_type == "iqtibos":
        return (
            f"{rules}\n\nWrite one short, memorable original motivational thought in "
            "one sentence, under 180 characters. Do not include an author or source."
        )
    if content_type == "hazil":
        return (
            f"{rules}\n\nWrite only one brief, friendly everyday joke in Uzbek, in one "
            "or two short sentences and under 180 characters. Do not add advice, "
            "motivation, emotional support, a second topic, or a separate paragraph. "
            "Keep it light and kind; do not mock a person or group."
        )
    if content_type == "sheriy":
        return (
            f"{rules}\n\nWrite only an original short Uzbek poem of 4 to 6 lines, "
            "under 300 characters total. Do not add prose before or after it, imitate "
            "a known poet, or quote existing lyrics."
        )
    raise ValueError(f"Unsupported Gemini content type: {content_type}")


def _validate_output(content_type: str, text: str) -> None:
    if len(text) > _MAX_CHARS[content_type]:
        raise InvalidGeneratedContent("Gemini response exceeded the requested length")

    sentence_count = len(re.findall(r"[.!?]+(?=\s|$)", text))
    if content_type == "mood" and not 2 <= sentence_count <= 3:
        raise InvalidGeneratedContent("Mood response must contain 2 or 3 sentences")
    if content_type == "iqtibos" and sentence_count > 1:
        raise InvalidGeneratedContent("Quote response must contain one sentence")
    if content_type == "hazil" and (
        sentence_count > 2 or "\n\n" in text
    ):
        raise InvalidGeneratedContent("Humor response must be one short joke")
    if content_type == "sheriy":
        line_count = len([line for line in text.splitlines() if line.strip()])
        if not 4 <= line_count <= 6:
            raise InvalidGeneratedContent("Poem response must contain 4 to 6 lines")


def _generate_once(prompt: str, content_type: str) -> str:
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
    _validate_output(content_type, text)
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
                return await asyncio.to_thread(_generate_once, prompt, content_type)
            except Exception as error:
                status_code = getattr(error, "code", None)
                retryable = (
                    not isinstance(error, InvalidGeneratedContent)
                    and (
                        status_code is None
                        or status_code in _RETRYABLE_STATUS_CODES
                    )
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
