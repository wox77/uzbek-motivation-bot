---
name: Telegram bot logging
description: Logging constraints for Telegram bot services using HTTP clients.
---

Telegram Bot API clients may include the bot token in request URLs when HTTP
logging is enabled at INFO. Keep `httpx` and Telegram transport logs at WARNING
or quieter in long-running bot workflows.

**Why:** A successful connectivity check can otherwise turn a secret into
workflow log output.

**How to apply:** Set transport logger levels before starting polling and
inspect startup logs for request URLs.