# Uzbek Motivation Telegram Bot

Telegram bot that sends original daily motivational messages in Uzbek. Users
choose one of 12 moods from an inline keyboard, and Anthropic Claude generates
a fresh message for that mood. Active users receive a daily message at 07:00
in the `Asia/Tashkent` timezone by default.

## Run

The project uses the secure Replit Secrets `TELEGRAM_BOT_TOKEN` and
`ANTHROPIC_API_KEY`. Start the bot with:

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

User records are written atomically to `data/users.json`. If a user blocks the
bot or their chat becomes unavailable, that user is automatically deactivated.