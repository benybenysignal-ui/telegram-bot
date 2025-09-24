import os
import logging
from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes

# ===== Logging =====
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
log = logging.getLogger("autojoin-bot")

# ===== Config =====
TOKEN = os.environ.get("BOT_TOKEN")

async def auto_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Approve every join request to the channel."""
    req = update.chat_join_request
    try:
        await context.bot.approve_chat_join_request(chat_id=req.chat.id, user_id=req.from_user.id)
        log.info(
            "👍 Approved join request | chat='%s' | user_id=%s | username=%s",
            getattr(req.chat, "title", req.chat.id),
            req.from_user.id,
            f"@{req.from_user.username}" if req.from_user.username else "-",
        )
    except Exception as e:
        log.exception("❌ Failed approving join request: %s", e)

def main():
    if not TOKEN:
        log.error("Missing BOT_TOKEN env var. Set it in Railway → Variables.")
        raise SystemExit(1)

    log.info("✅ Bot starting… waiting for join requests")
    app = Application.builder().token(TOKEN).build()

    # Handle channel join requests
    app.add_handler(ChatJoinRequestHandler(auto_approve))

    # Start polling (async-safe, PTB v21)
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
