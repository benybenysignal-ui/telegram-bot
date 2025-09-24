import os
import logging
from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes, Application

# ---- Logging ----
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("autojoin-bot")

TOKEN = os.environ.get("BOT_TOKEN")

async def post_init(app: Application):
    """ניקוי webhook וזריקת עדכונים תלויים למניעת קונפליקטים."""
    try:
        await app.bot.delete_webhook(drop_pending_updates=True)
        log.info("Webhook deleted (drop_pending_updates=True)")
    except Exception as e:
        log.warning("Couldn't delete webhook: %s", e)

async def auto_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """אישור אוטומטי לכל בקשת הצטרפות לערוץ."""
    req = update.chat_join_request
    try:
        await context.bot.approve_chat_join_request(chat_id=req.chat.id, user_id=req.from_user.id)
        log.info(
            "👍 Approved | chat='%s' | user_id=%s | username=%s",
            getattr(req.chat, "title", req.chat.id),
            req.from_user.id,
            f"@{req.from_user.username}" if req.from_user.username else "-",
        )
    except Exception as e:
        # אם הבוט לא אדמין/חסרות הרשאות – תראה כאן שגיאת 400
        log.exception("❌ Failed approving: %s", e)

def main():
    if not TOKEN:
        log.error("Missing BOT_TOKEN env var. Set it in Railway → Variables.")
        raise SystemExit(1)

    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init)   # יופעל בצורה אסינכרונית לפני תחילת ה-polling
        .build()
    )

    app.add_handler(ChatJoinRequestHandler(auto_approve))

    log.info("✅ Bot starting… waiting for join requests")
    # run_polling מנהל את הלולאה בעצמו; מאזין רק לסוג העדכון הנדרש
    app.run_polling(allowed_updates=["chat_join_request"])

if __name__ == "__main__":
    main()
