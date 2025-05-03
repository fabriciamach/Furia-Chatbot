from telegram import Update
from telegram.ext import ContextTypes
from services.draft5 import fetch_draft5_data
from utils.timeout import reset_timeout
import logging

logger = logging.getLogger(__name__)

async def lineup(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    await reset_timeout(update, context)
    try:
        data = await fetch_draft5_data()
        players = data["props"]["pageProps"]["data"]["playerData"]
        titulares = [
            p["playerNickname"]
            for p in players
            if any(h["status"] == "Titular" for h in p["playerHistory"])
        ]
        coaches = [
            p["playerNickname"]
            for p in players
            if any(h["status"] == "Coach" for h in p["playerHistory"])
        ]
        text = (
            "🔥 Titulares da FURIA:\n" + "\n".join(f"• {p}" for p in titulares)
            + "\n\n👔 Coach:\n" + "\n".join(f"• {c}" for c in coaches)
        )
        await update.message.reply_text(text)
    except Exception:
        logger.exception("Erro ao buscar lineup")
        await update.message.reply_text(
            "❌ Erro ao buscar a line-up. Tente novamente mais tarde."
        )