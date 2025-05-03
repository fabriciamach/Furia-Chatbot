from telegram import Update
from telegram.ext import ContextTypes
from utils.timeout import reset_timeout
from handlers.start import start
from handlers.lineup import lineup
from handlers.results import ultimos_jogos, prox_jogos
from handlers.stickers import send_furia_sticker
from handlers.exit import sair
import logging

logger = logging.getLogger(__name__)

async def handle_all_messages(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    if not context.user_data.get("iniciado"):
        await start(update, context)
        return
    await reset_timeout(update, context)
    await handle_menu(update, context)

async def handle_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    text = update.message.text
    if text == "Elenco 👥":
        await lineup(update, context)
    elif text == "Ingressos 🎟️":
        await update.message.reply_text("🎟️ Compre ingressos: https://furia.gg/ingressos")
    elif text == "Resultados 📊":
        await ultimos_jogos(update, context)
    elif text == "Próximos Jogos 🎮":
        await prox_jogos(update, context)
    elif text == "Jogo Ao Vivo 🔴":
        await update.message.reply_text("🔴 Assista ao vivo: https://twitch.tv/furia")
    elif text == "Redes 📱":
        await update.message.reply_text(
            "📱 Redes oficiais:\n"
            "• Twitter: @furiagg\n"
            "• Instagram: @furia\n"
            "• Site: https://furia.gg"
        )
    elif text == "Torcida 🐾":
        await send_furia_sticker(update, context)
    elif text == "Sair ❌":
        await sair(update, context)
    else:
        await update.message.reply_text(
            "❌ Opção inválida. Use os botões abaixo."
        )