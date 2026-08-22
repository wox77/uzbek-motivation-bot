---
name: Anthropic credit fallback
description: Behavior when direct Anthropic API access is blocked by account credits.
---

When Anthropic returns a credit-balance `400`, the bot should keep the user flow
working with a local Uzbek fallback message and log the billing cause clearly.

**Why:** Account billing state is external to the bot and cannot be repaired by
changing Telegram handlers.

**How to apply:** Catch only the recognized credit-balance error, preserve other
API errors for investigation, and retry Claude automatically once credits are
available.