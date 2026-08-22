# Uzbek Motivation Telegram Bot

Telegram bot that provides Uzbek motivational messages, quotes, daily humor, and poetic lines, with a random daily broadcast to active users.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the API server (port 5000)
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- Required env: `DATABASE_URL` — Postgres connection string
- `python main.py` — run the Telegram bot
- Required secret: `TELEGRAM_BOT_TOKEN`

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- API: Express 5
- DB: PostgreSQL + Drizzle ORM
- Validation: Zod (`zod/v4`), `drizzle-zod`
- API codegen: Orval (from OpenAPI spec)
- Build: esbuild (CJS bundle)

## Where things live

- `main.py` — Telegram handlers, local quote generation, scheduler, and JSON storage
- `local_quotes.py` — offline Uzbek quote combinations for every mood
- `extended_content.py` — offline quote, humor, and poetic-line content bank
- `data/users.json` — runtime user records (created automatically and ignored by git)
- `README.md` — setup and command reference

## Architecture decisions

- The offline `local_quotes.py` generator creates unique messages without AI or internet access.
- APScheduler's `AsyncIOScheduler` runs in the Telegram application's event loop.
- User records are stored in an atomically replaced JSON file to avoid partial writes.
- Default scheduling timezone is `Asia/Tashkent`, configurable via `BOT_TIMEZONE`.

## Product

Users select one of 12 mood categories and receive a short, practical motivational message in Uzbek. Active subscribers receive a fresh daily message at 07:00.
The bot profile describes its daily unique quote, humor, or poetic-line content.

## User preferences

Messages are in Uzbek and should be warm, concise, unique, and related to the selected mood.

## Gotchas

- Never put `TELEGRAM_BOT_TOKEN` in source files.
- Run the bot as a long-lived process; APScheduler broadcasts only while the process is running.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
