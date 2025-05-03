from telegram import Update
from telegram.ext import ContextTypes
from utils.timeout import reset_timeout
import random
import logging

logger = logging.getLogger(__name__)

FURIA_STICKERS = [
    "CAACAgEAAxkBAAPuaBROOR1letve8eBCCBRaj-Jhu2UAAh4FAAKgp6BEFCIRKl9Du0s2BA",
    "CAACAgEAAxkBAAP3aBRTQMHzdVIrVk1mKqchXb7OzocAAmgFAAIhvKlEq3sovViQnNI2BA",
    "CAACAgEAAxkBAAP5aBRTW25VK-ZAykMOMltZxeTUxpYAAncEAAIklahEtWEdUO2RUCU2BA"
]

async def send_furia_sticker(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    await reset_timeout(update, context)
    sticker = random.choice(FURIA_STICKERS)
    try:
        await update.message.reply_sticker(sticker=sticker)
        await update.message.reply_text("🔥 VAMOS FURIA! 🔥")
    except Exception:
        logger.exception("Erro ao enviar figurinha")
        await update.message.reply_text(
            "❌ Não foi possível enviar a figurinha."
        )