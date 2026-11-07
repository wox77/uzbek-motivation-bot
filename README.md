# Uzbek Motivation Telegram Bot

Telegram bot that generates Uzbek motivational messages with Gemini. Users
choose one of 12 moods from an inline keyboard; the menu also offers quotes,
daily humor, and poetic lines. Active users receive a randomly selected daily
message at 07:00 in the `Asia/Tashkent` timezone by default. If Gemini is
unavailable, the bot uses its local Uzbek content generators.

## Run

Set `TELEGRAMTOKEN` as a required Replit Secret. `GEMINI_API_KEY` is optional;
without it, the bot uses its local Uzbek content. Gemini API usage may be
billed separately by Google; a Gemini app subscription does not automatically
cover API usage. Start the bot with:

```bash
python main.py
```

Optional environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `GEMINI_MODEL` | `gemini-3.5-flash-lite` | Gemini model used for new content |
| `BOT_TIMEZONE` | `Asia/Tashkent` | IANA timezone used for scheduling |
| `DAILY_MESSAGE_HOUR` | `7` | Daily broadcast hour |
| `DAILY_MESSAGE_MINUTE` | `0` | Daily broadcast minute |
| `USERS_FILE` | `data/users.json` | JSON persistence location |
| `LOG_LEVEL` | `INFO` | Python logging level |

## Bot commands

- `/start` subscribes the user and displays the mood keyboard.
- `/mood` displays the mood keyboard again.
- `/stop` pauses daily broadcasts for the user.

The daily broadcast rotates between AI-generated quotes, humor, and poetic
lines, and avoids repeating the same text within one broadcast when possible.
Local content remains available as a fallback if the Gemini API is unavailable.

User records are written atomically to `data/users.json`. If a user blocks the
bot or their chat becomes unavailable, that user is automatically deactivated.