from telegram import Update
from telegram.ext import ContextTypes
from services.draft5 import fetch_draft5_data
from utils.timeout import reset_timeout
from utils.translations import translate_map
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

async def ultimos_jogos(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    await reset_timeout(update, context)
    try:
        data = await fetch_draft5_data()
        for r in data["props"]["pageProps"]["results"][:4]:
            torneio = r["tournament"]["tournamentName"]
            adversario = r["teamB"]["teamName"]
            placar = f"{r['seriesScoreA']}-{r['seriesScoreB']}"
            mapas = ", ".join(
                f"{translate_map(s['map']['mapName'])} ({s['scoreA']}-{s['scoreB']})"
                for s in r["scores"]
            )
            text = f"🏆 {torneio}\nFURIA vs {adversario}: {placar}\n📍 Mapas: {mapas}"
            await update.message.reply_text(text)
    except Exception:
        logger.exception("Erro ao buscar resultados")
        await update.message.reply_text(
            "❌ Erro ao buscar resultados. Tente novamente mais tarde."
        )

async def prox_jogos(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    await reset_timeout(update, context)
    try:
        data = await fetch_draft5_data()
        ts_to_str = lambda ts: datetime.utcfromtimestamp(ts).strftime("%d/%m/%Y %H:%M")
        proximas = [m for m in data["props"]["pageProps"]["matches"] if not m["isFinished"]]
        if not proximas:
            await update.message.reply_text(
                "ℹ️ Não há partidas agendadas para a Furia no momento."
            )
            return
        text = "🗓️ Próximas Partidas da Furia\n\n"
        for m in proximas:
            adv = m["teamB"]["teamName"] if m["teamA"]["teamId"] == 330 else m["teamA"]["teamName"]
            text += (
                f"🆚 {adv}\n"
                f"📅 {ts_to_str(m['matchDate'])}\n"
                f"🏆 {m['tournament']['tournamentName']}\n"
                "──────────────────\n"
            )
        await update.message.reply_text(text)
    except Exception:
        logger.exception("Erro ao buscar próximas partidas")
        await update.message.reply_text(
            "❌ Erro ao buscar próximas partidas. Tente novamente mais tarde."
        )