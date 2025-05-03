from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from logging_cfg import logger

async def sair(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    job = context.user_data.pop("timeout_job", None)
    if job:
        try:
            job.schedule_removal()
        except Exception:
            logger.exception("Erro ao remover job de timeout")
    if update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="🐾 Até logo! Mande qualquer mensagem para voltar.",
            reply_markup=ReplyKeyboardRemove()
        )
    context.user_data.clear()