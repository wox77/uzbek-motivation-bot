---
name: Python Telegram dependency
description: Avoiding package collisions between python-telegram-bot and the unrelated telegram PyPI package.
---

In this workspace, adding Python dependencies can introduce the unrelated `telegram` distribution alongside `python-telegram-bot`. Both write into the `telegram` import namespace, and the placeholder distribution can overwrite the real library's package initializer. An already-running process may hide this until the next restart.

**Why:** The import name `telegram` is not the distribution name; the maintained bot package is `python-telegram-bot`.

**How to apply:** Keep only `python-telegram-bot` as the project dependency, check `pyproject.toml` and `uv.lock` after package changes, and verify a fresh process can import `InlineKeyboardButton` from `telegram`.
