"""Daily Uzbek motivation Telegram bot.

Required secrets:
    TELEGRAM_BOT_TOKEN  - token from @BotFather
    ANTHROPIC_API_KEY   - Anthropic API key
"""

from __future__ import annotations

import json
import logging
import os
import random
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from anthropic import AsyncAnthropic
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction
from telegram.error import BadRequest, Forbidden, TelegramError
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
)
logger = logging.getLogger("uzbek-motivation-bot")
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)

TIMEZONE = ZoneInfo(os.getenv("BOT_TIMEZONE", "Asia/Tashkent"))
DATA_FILE = Path(os.getenv("USERS_FILE", "data/users.json"))
MODEL = "claude-sonnet-4-6"

MOODS: dict[str, str] = {
    "umidsizlik": "umidsizlik",
    "tanhalilik": "tanhalilik",
    "xavfxona": "xavfxona",
    "charchalik": "charchalik",
    "ayblanish": "ayblanish",
    "xushyaliq": "xushyaliq",
    "muvaffaqiyat": "gʻoyat muvaffaqiyat",
    "stres": "stres",
    "murakkab": "oʻziga nisbatan murakkab",
    "gazab": "gʻazab",
    "kelajak": "kelajak",
    "sevgi": "sevgi",
}


class UserStore:
    """Small atomic JSON store for subscribers and their latest mood."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.users: dict[str, dict[str, Any]] = {}
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            return
        try:
            parsed = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(parsed, dict):
                self.users = parsed
        except (OSError, json.JSONDecodeError):
            logger.exception("Could not read user data; starting with an empty store")

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(
            prefix=f"{self.path.name}.", dir=self.path.parent, text=True
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as temp_file:
                json.dump(self.users, temp_file, ensure_ascii=False, indent=2)
                temp_file.write("\n")
            os.replace(temp_name, self.path)
        except BaseException:
            try:
                os.unlink(temp_name)
            except OSError:
                pass
            raise

    def upsert(self, chat_id: int, **fields: Any) -> None:
        user = self.users.setdefault(str(chat_id), {"chat_id": chat_id, "active": True})
        user.update(fields)
        self.save()

    def set_active(self, chat_id: int, active: bool) -> None:
        self.upsert(chat_id, active=active)

    def active_users(self) -> list[dict[str, Any]]:
        return [user for user in self.users.values() if user.get("active", True)]


def mood_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(label, callback_data=f"mood:{key}")
        for key, label in MOODS.items()
    ]
    return InlineKeyboardMarkup(
        [buttons[index : index + 2] for index in range(0, len(buttons), 2)]
    )


def menu_text() -> str:
    return (
        "Bugun qalbingizga qaysi mavzuda dalda kerak?\n\n"
        "Holatingizni tanlang — siz uchun o‘zbek tilida maxsus motivatsion xabar "
        "tayyorlayman."
    )


class MotivationService:
    def __init__(self) -> None:
        self.client = AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    async def generate(self, mood: str, recipient_hint: str = "") -> str:
        prompt = f"""
Siz o‘zbek tilida yozadigan mehribon va ilhomlantiruvchi motivatsion murabbiy
bo‘ling. Foydalanuvchining hozirgi holati: “{mood}”.
{recipient_hint}
Shu holatga mos, samimiy va noyob motivatsion xabar yozing.
Talablar:
- Faqat o‘zbek tilida yozing.
- 2–4 qisqa paragraf bo‘lsin, jami 80–140 so‘zdan oshmasin.
- Birinchi gap e’tiborli va iliq bo‘lsin.
- Amaliy, kichik bir qadam yoki fikrlash mashqini taklif qiling.
- Haddan tashqari balandparvoz, hukm qiluvchi yoki takroriy iboralardan qoching.
- Emoji va hashtaglardan foydalanmang.
- Tibbiy tashxis yoki professional yordam o‘rniga maslahat bermang.
"""
        response = await self.client.messages.create(
            model=MODEL,
            max_tokens=8192,
            messages=[{"role": "user", "content": prompt}],
        )
        text_parts = [
            block.text for block in response.content if getattr(block, "type", "") == "text"
        ]
        message = "\n".join(text_parts).strip()
        if not message:
            raise RuntimeError("Anthropic returned an empty message")
        return message


def now_iso() -> str:
    return datetime.now(TIMEZONE).isoformat()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_chat:
        return
    user = update.effective_user
    store: UserStore = context.application.bot_data["store"]
    store.upsert(
        update.effective_chat.id,
        first_name=user.first_name if user else "",
        username=user.username if user else "",
        active=True,
        last_seen=now_iso(),
    )
    await update.effective_message.reply_text(menu_text(), reply_markup=mood_keyboard())


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_chat:
        return
    store: UserStore = context.application.bot_data["store"]
    store.set_active(update.effective_chat.id, False)
    await update.effective_message.reply_text(
        "Kunlik xabarlar to‘xtatildi. Qayta boshlash uchun /start yuboring."
    )


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_message:
        await update.effective_message.reply_text(menu_text(), reply_markup=mood_keyboard())


async def mood_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not update.effective_chat:
        return
    await query.answer()
    mood_key = query.data.removeprefix("mood:")
    mood = MOODS.get(mood_key)
    if not mood:
        await query.edit_message_text("Bu tanlov topilmadi. /start orqali qayta urinib ko‘ring.")
        return

    store: UserStore = context.application.bot_data["store"]
    service: MotivationService = context.application.bot_data["motivation"]
    store.upsert(update.effective_chat.id, active=True, last_mood=mood_key, last_seen=now_iso())
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    try:
        message = await service.generate(mood)
        await query.edit_message_text(
            f"“{mood}” uchun sizga:\n\n{message}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Boshqa kayfiyatni tanlash", callback_data="menu")]]
            ),
        )
    except Exception:
        logger.exception("Could not generate a message for chat %s", update.effective_chat.id)
        await query.edit_message_text(
            "Hozir xabar tayyorlashda kichik muammo yuz berdi. Iltimos, birozdan so‘ng yana urinib ko‘ring."
        )


async def daily_broadcast(application: Application) -> None:
    store: UserStore = application.bot_data["store"]
    service: MotivationService = application.bot_data["motivation"]
    users = store.active_users()
    logger.info("Starting daily broadcast to %d users", len(users))
    for user in users:
        chat_id = int(user["chat_id"])
        mood_key = user.get("last_mood") or random.choice(list(MOODS))
        mood = MOODS[mood_key]
        try:
            message = await service.generate(
                mood,
                f"Bu kundalik xabar {now_iso()[:10]} sanasida yuborilmoqda; avvalgi xabarlardan "
                "farqli, yangi mazmun yarating.",
            )
            await application.bot.send_message(
                chat_id=chat_id,
                text=f"Assalomu alaykum! Bugungi ilhom:\n\n{message}",
            )
        except Forbidden:
            logger.info("Chat %s blocked the bot; deactivating", chat_id)
            store.set_active(chat_id, False)
        except BadRequest as error:
            logger.warning("Chat %s is unavailable: %s", chat_id, error)
            store.set_active(chat_id, False)
        except Exception:
            logger.exception("Daily message failed for chat %s", chat_id)


async def on_error(update: object, context: CallbackContext[Any, Any, Any, Any]) -> None:
    logger.error("Unhandled Telegram error: %s", context.error, exc_info=context.error)


def build_application() -> Application:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN secret is not configured")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("ANTHROPIC_API_KEY secret is not configured")

    application = ApplicationBuilder().token(token).build()
    application.bot_data["store"] = UserStore(DATA_FILE)
    application.bot_data["motivation"] = MotivationService()
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    application.bot_data["scheduler"] = scheduler
    scheduler.add_job(
        daily_broadcast,
        trigger="cron",
        hour=int(os.getenv("DAILY_MESSAGE_HOUR", "7")),
        minute=int(os.getenv("DAILY_MESSAGE_MINUTE", "0")),
        args=[application],
        id="daily-motivation-broadcast",
        replace_existing=True,
        misfire_grace_time=3600,
    )

    async def post_init(_: Application) -> None:
        scheduler.start()
        logger.info("Bot ready; daily messages scheduled for 07:00 %s", TIMEZONE)

    async def post_shutdown(_: Application) -> None:
        if scheduler.running:
            scheduler.shutdown(wait=False)

    application.post_init = post_init
    application.post_shutdown = post_shutdown
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
    application.add_handler(CommandHandler("mood", show_menu))
    application.add_handler(CallbackQueryHandler(mood_selected, pattern=r"^mood:"))
    application.add_handler(CallbackQueryHandler(show_menu, pattern=r"^menu$"))
    application.add_error_handler(on_error)
    return application


def main() -> None:
    build_application().run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()