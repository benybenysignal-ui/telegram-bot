import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes

# ===== Logging =====
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("autojoin-bot")

# ===== Config =====
TOKEN = os.environ.get("BOT_TOKEN")

async def auto_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req = update.chat_join_request
    try:
        await context.bot.approve_chat_join_request(chat_id=req.chat.id, user_id=req.from_user.id)
        log.info("👍 Approved | chat='%s' | user_id=%s | username=%s",
                 getattr(req.chat, "title", req.chat.id),
                 req.from_user.id,
                 f"@{req.from_user.username}" if req.from_user.username else "-")
    except Exception as e:
        log.exception("❌ Failed approving: %s", e)

async def main():
    if not TOKEN:
        log.error("Missing BOT_TOKEN env var.")
        raise SystemExit(1)

    log.info("✅ Bot starting… waiting for join requests")
    app = Application.builder().token(TOKEN).build()

    # נקה webhook ישן
    await app.bot.delete_webhook(drop_pending_updates=True)
    log.info("Webhook deleted (drop_pending_updates=True)")

    # הוסף Handler להצטרפויות
    app.add_handler(ChatJoinRequestHandler(auto_approve))

    # הרץ Polling עם סינון רק להצטרפויות
    await app.run_polling(allowed_updates=["chat_join_request"])

if __name__ == "__main__":
    asyncio.run(main())
