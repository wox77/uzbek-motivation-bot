# Uzbek Motivation Telegram Bot

Telegram bot that generates Uzbek motivational messages for selected moods and broadcasts a daily message to active users.

## Run & Operate

- `pnpm --filter @workspace/api-server run dev` — run the API server (port 5000)
- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from the OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- Required env: `DATABASE_URL` — Postgres connection string
- `python main.py` — run the Telegram bot
- Required secrets: `TELEGRAM_BOT_TOKEN`, `ANTHROPIC_API_KEY`

## Stack

- pnpm workspaces, Node.js 24, TypeScript 5.9
- API: Express 5
- DB: PostgreSQL + Drizzle ORM
- Validation: Zod (`zod/v4`), `drizzle-zod`
- API codegen: Orval (from OpenAPI spec)
- Build: esbuild (CJS bundle)

## Where things live

- `main.py` — Telegram handlers, Claude generation, scheduler, and JSON storage
- `data/users.json` — runtime user records (created automatically and ignored by git)
- `README.md` — setup and command reference

## Architecture decisions

- Anthropic's async Python SDK is used with `claude-sonnet-4-6` for unique messages.
- APScheduler's `AsyncIOScheduler` runs in the Telegram application's event loop.
- User records are stored in an atomically replaced JSON file to avoid partial writes.
- Default scheduling timezone is `Asia/Tashkent`, configurable via `BOT_TIMEZONE`.

## Product

Users select one of 12 mood categories and receive a short, practical motivational message in Uzbek. Active subscribers receive a fresh daily message at 07:00.

## User preferences

Messages are in Uzbek and should be warm, concise, unique, and related to the selected mood.

## Gotchas

- Never put `TELEGRAM_BOT_TOKEN` or `ANTHROPIC_API_KEY` in source files.
- Run the bot as a long-lived process; APScheduler broadcasts only while the process is running.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
