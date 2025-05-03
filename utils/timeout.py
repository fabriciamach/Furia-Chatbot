from datetime import timedelta
from telegram import Update
from telegram.ext import ContextTypes
from config import TIMEOUT_MINUTES
from logging_cfg import logger

async def _timeout_callback(context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = context.job.chat_id
    await context.bot.send_message(chat_id, "⏰ Sessão encerrada por AFK!")
    # opcional: chamar cleanup de sessão

async def reset_timeout(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    chat_id = update.effective_chat.id
    job = context.user_data.get("timeout_job")
    if job:
        job.schedule_removal()
    context.user_data["timeout_job"] = context.job_queue.run_once(
        _timeout_callback,
        timedelta(minutes=TIMEOUT_MINUTES),
        chat_id=chat_id,
        name=f"timeout_{chat_id}"
    )
    logger.debug(f"Timeout reset para chat {chat_id}")