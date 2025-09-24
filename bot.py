from telegram import Update
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes
import os

TOKEN = os.environ.get("BOT_TOKEN")

async def auto_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req = update.chat_join_request
    await context.bot.approve_chat_join_request(
        chat_id=req.chat.id,
        user_id=req.from_user.id
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(auto_approve))
    app.run_polling()

if __name__ == "__main__":
    main()
