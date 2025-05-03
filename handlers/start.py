from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from utils.timeout import reset_timeout

WELCOME_KEYBOARD = ReplyKeyboardMarkup(
    [
        ["Próximos Jogos 🎮", "Resultados 📊"],
        ["Ingressos 🎟️", "Torcida 🐾"],
        ["Jogo Ao Vivo 🔴", "Elenco 👥"],
        ["Redes 📱", "Sair ❌"]
    ],
    resize_keyboard=True,
    input_field_placeholder="Escolha uma opção..."
)

WELCOME_TEXT = (
    "🐾 Bem-vindo ao Bot Oficial da FURIA CS!\n\n"
    "Aqui você encontra:\n"
    "• Próximos jogos e resultados\n"
    "• Elenco completo\n"
    "• Ingressos e transmissões\n"
    "• Link das Redes Sociais\n"
    "• Stickers da torcida\n\n"
    "VAMOS COM OS FURIOSOS! 🖤🔥"
)

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    await reset_timeout(update, context)
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=WELCOME_KEYBOARD
    )
    context.user_data['iniciado'] = True