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
<<<<<<< HEAD
    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all_messages)
=======
    
    await update.message.reply_text(
        "🐾 Bem-vindo ao Bot Oficial da FURIA CS!\n\n"
        "Aqui você encontra:\n"
        "• Próximos jogos e resultados\n"
        "• Elenco completo\n"
        "• Ingressos e transmissões\n"
        "• Link das Redes Sociais\n"
        "• Stickers da torcida\n\n"
        "VAMOS COM OS FURIOSOS! 🖤🔥",
        reply_markup=teclado
>>>>>>> 699442bd1c3b3c4521ab000d547ac238cc7da4ec
    )
    logger.info("Bot iniciado")
    app.run_polling()

<<<<<<< HEAD
if __name__ == "__main__":
    main()
=======
async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler principal"""
    await reset_timeout(update, context)  # Reseta o timer
    
    if not context.user_data.get('iniciado'):
        await start(update, context)
        return
    
    await handle_menu(update, context)

import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, Any

async def fetch_draft5_data(equipe_id: int = 330) -> Dict[str, Any]:
    """
    Obtém dados estruturados do site Draft5.gg para uma equipe específica
    
    Args:
        equipe_id: ID da equipe no Draft5 (padrão: 330 para FURIA)
    
    Returns:
        Dicionário com os dados parseados
        
    Raises:
        Exception: Em caso de falha na requisição ou parsing
    """
    url = f"https://draft5.gg/equipe/{equipe_id}-FURIA"  # Padrão FURIA, mas pode ser generalizado
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # 1. Faz a requisição
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Levanta exceção para status 4XX/5XX
        
        # 2. Parseia o HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        script = soup.find("script", id="__NEXT_DATA__")
        
        if not script:
            raise ValueError("Dados NEXT_DATA não encontrados no HTML")
            
        # 3. Converte JSON
        return json.loads(script.string)
        
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        raise
    except Exception as e:
        print(f"Erro inesperado: {e}")
        raise

async def lineup(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await reset_timeout(context, update.effective_chat.id)

    try:
        data = await fetch_draft5_data()

        titulares = [
            p["playerNickname"] for p in data["props"]["pageProps"]["data"]["playerData"]
            if any(h["status"] == "Titular" for h in p["playerHistory"])
        ]

        coachs = [
            c["playerNickname"] for c in data["props"]["pageProps"]["data"]["playerData"]
            if any(h["status"] == "Coach" for h in c["playerHistory"])
        ]

        await update.message.reply_text(
            "🔥 Titulares da FURIA:\n" + "\n".join([f"• {p}" for p in titulares]) + 
            "\n\n👔 Coach:\n" + "\n".join([f"• {c}" for c in coachs])
        )
    except Exception as e:
        await update.message.reply_text("❌ Erro ao buscar a line-up. Tente novamente mais tarde.")

async def ultimos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await reset_timeout(context, update.effective_chat.id)
    
    try:
        data = await fetch_draft5_data()

        for resultado in data["props"]["pageProps"]["results"][:4]:
            torneio = resultado["tournament"]["tournamentName"]
            adversario = resultado["teamB"]["teamName"]
            placar = f"{resultado['seriesScoreA']}-{resultado['seriesScoreB']}"
            mapas = ", ".join([
                f"{MAP_TRANSLATION.get(s['map']['mapName'], s['map']['mapName'])} ({s['scoreA']}-{s['scoreB']})" 
                for s in resultado["scores"]
            ])
            await update.message.reply_text(
                f"🏆 {torneio} \nFURIA vs {adversario}: {placar} \n 📍Mapas: {mapas}"
            )

    except Exception as e:
        await update.message.reply_text("❌ Erro ao buscar resultados. Tente novamente mais tarde.")

async def prox_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await reset_timeout(context, update.effective_chat.id)

    try:
        data = await fetch_draft5_data()

        def timestamp_to_date(timestamp):
            return datetime.utcfromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M')

        # Obter as próximas partidas da Furia
        proximas_partidas = []
        for match in data['props']['pageProps']['matches']:
            if not match['isFinished']:
                adversario = match['teamB']['teamName'] if match['teamA']['teamId'] == 330 else match['teamA']['teamName']
                
                partida = {
                    'adversario': adversario,
                    'data': timestamp_to_date(match['matchDate']),
                    'torneio': match['tournament']['tournamentName'],
                }
                proximas_partidas.append(partida)

        # Construir mensagem
        if not proximas_partidas:
            await update.message.reply_text("ℹ️ Não há partidas agendadas para a Furia no momento.")
            return

        mensagem = "🗓️ **Próximas Partidas da Furia**\n\n"
        
        for partida in proximas_partidas:
            mensagem += (
                f"🆚 **{partida['adversario']}**\n"
                f"📅 {partida['data']}\n"
                f"🏆 {partida['torneio']}\n"
            )
            
            mensagem += "──────────────────\n"

        await update.message.reply_text(mensagem, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("❌ Erro ao buscar próximas partidas. Tente novamente mais tarde.")


async def send_furia_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await reset_timeout(context, update.effective_chat.id)

    furia_stickers = [
        "CAACAgEAAxkBAAPuaBROOR1letve8eBCCBRaj-Jhu2UAAh4FAAKgp6BEFCIRKl9Du0s2BA",
        "CAACAgEAAxkBAAP3aBRTQMHzdVIrVk1mKqchXb7OzocAAmgFAAIhvKlEq3sovViQnNI2BA",
        "CAACAgEAAxkBAAP5aBRTW25VK-ZAykMOMltZxeTUxpYAAncEAAIklahEtWEdUO2RUCU2BA"
    ]
    
    chosen_sticker = random.choice(furia_stickers)
    await update.message.reply_sticker(sticker=chosen_sticker)
    await update.message.reply_text("🔥 VAMOS FURIA! 🔥")

async def sair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Função sair corrigida"""
    try:
        # 1. Cancela timeout
        if 'timeout_job' in context.user_data:
            try:
                context.user_data['timeout_job'].schedule_removal()
            except Exception:
                pass

        # 2. Envia mensagem de forma segura
        if update.effective_chat:  # Verifica se é uma mensagem real
            await context.bot.send_message(  # Usa context.bot diretamente
                chat_id=update.effective_chat.id,
                text="🐾 Até logo! Mande qualquer mensagem para voltar.",
                reply_markup=ReplyKeyboardRemove()
            )

        # 3. Limpa estado
        context.user_data.clear()

    except Exception as e:
        print(f"Erro no /sair: {e}")

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    
    if texto == "Elenco 👥":
        await lineup(update, context)
    elif texto == "Ingressos 🎟️":
        await update.message.reply_text("🎟️ Compre ingressos: https://furia.gg/ingressos")
    elif texto == "Resultados 📊":
        await ultimos_jogos(update, context)
    elif texto == "Próximos Jogos 🎮":
        await prox_jogos(update, context)
    elif texto == "Jogo Ao Vivo 🔴":
        await update.message.reply_text("🔴 Assista ao vivo: https://twitch.tv/furia")
    elif texto == "Redes 📱":
        await update.message.reply_text(
            "📱 Redes oficiais:\n"
            "• Twitter: @furiagg\n"
            "• Instagram: @furia\n"
            "• Site: https://furia.gg"
        )
    elif texto == "Torcida 🐾":
        await send_furia_sticker(update, context)
    elif texto == "Sair ❌":
        await sair(update, context)
    else:
        await update.message.reply_text("❌ Opção inválida. Use os botões abaixo.")

# Configuração do bot
application = (
    ApplicationBuilder()
    .token("7756865402:AAH2yOMIYrmQdVZ9QepkmQ9YIlsjPeqE3Sk")
    .concurrent_updates(True)
    .build()
)

# Handlers simplificados
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all_messages))

application.run_polling()
>>>>>>> 699442bd1c3b3c4521ab000d547ac238cc7da4ec
