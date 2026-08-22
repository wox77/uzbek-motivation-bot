# Uzbek Motivation Telegram Bot

Telegram bot that sends original daily motivational messages in Uzbek. Users
choose one of 12 moods from an inline keyboard, and the offline local quote
generator creates a fresh combination for that mood. The menu also includes
famous quotes, daily humor, and poetic lines. Active users receive a random
daily message at 07:00 in the `Asia/Tashkent` timezone by default.

## Run

The project uses the secure Replit Secret `TELEGRAM_BOT_TOKEN`. Start the bot
with:

```bash
python main.py
```

Optional environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `BOT_TIMEZONE` | `Asia/Tashkent` | IANA timezone used for scheduling |
| `DAILY_MESSAGE_HOUR` | `7` | Daily broadcast hour |
| `DAILY_MESSAGE_MINUTE` | `0` | Daily broadcast minute |
| `USERS_FILE` | `data/users.json` | JSON persistence location |
| `LOG_LEVEL` | `INFO` | Python logging level |

## Bot commands

- `/start` subscribes the user and displays the mood keyboard.
- `/mood` displays the mood keyboard again.
- `/stop` pauses daily broadcasts for the user.

The daily broadcast rotates between quotes, humor, and poetic lines and avoids
repeating the same content for users within one broadcast when possible.

User records are written atomically to `data/users.json`. If a user blocks the
bot or their chat becomes unavailable, that user is automatically deactivated.