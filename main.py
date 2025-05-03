from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
from logging_cfg import logger
from handlers.start import start
from handlers.menu import handle_all_messages

def main() -> None:
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .concurrent_updates(True)
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all_messages)
    )
    logger.info("Bot iniciado")
    app.run_polling()

if __name__ == "__main__":
    main()