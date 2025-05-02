from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, JobQueue
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import random
from apscheduler.jobstores.base import JobLookupError

# Dicionário de tradução de mapas
MAP_TRANSLATION = {
    "de_anubis": "Anubis",
    "de_inferno": "Inferno",
    "de_mirage": "Mirage",
    "de_nuke": "Nuke",
    "de_overpass": "Overpass",
    "de_ancient": "Ancient",
    "de_vertigo": "Vertigo",
    "de_dust2": "Dust 2",
    "de_train": "Train",
    "de_cache": "Cache",
    "de_cbble": "Cobblestone",
    "de_tuscan": "Tuscan",
    "de_season": "Season"
}

def translate_map(map_name):
    return MAP_TRANSLATION.get(map_name, map_name)

# ... (mantenha suas constantes e funções de tradução como estão)

async def timeout_callback(context: ContextTypes.DEFAULT_TYPE):
    """Função chamada quando o tempo acabar"""
    job = context.job
    await context.bot.send_message(
        chat_id=job.chat_id,
        text="⏰ Parece que você ficou inativo por muito tempo. "
             "Digite /start para começar novamente!",
        reply_markup=ReplyKeyboardRemove()
    )

async def reset_timeout(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    """Reseta o timeout para o chat específico"""
    try:
        # Verifica se existe um job antigo e tenta removê-lo
        if 'job' in context.chat_data and context.chat_data['job'] is not None:
            try:
                old_job = context.chat_data['job']
                if old_job:
                    old_job.schedule_removal()
            except JobLookupError:
                # O job já foi removido, podemos ignorar o erro
                pass
            except Exception as e:
                print(f"Erro ao remover job antigo: {e}")
    
    except KeyError:
        # Não há job no chat_data, podemos prosseguir
        pass
    
    # Agenda um novo job
    context.chat_data['job'] = context.job_queue.run_once(
        callback=timeout_callback,
        when=timedelta(minutes=1),  # Teste com 1 minuto
        chat_id=chat_id,
        name=str(chat_id)
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para o comando /start"""
    await reset_timeout(context, update.effective_chat.id)
    
    teclado = ReplyKeyboardMarkup(
        [
            ["Próximos Jogos 🎮", "Resultados 📊"],
            ["Ingressos 🎟️", "Torcida 🐾"],
            ["Jogo Ao Vivo 🔴", "Elenco 👥"],
            ["Redes 📱", "Sair ❌"]
        ],
        resize_keyboard=True,
        input_field_placeholder="Escolha uma opção..."
    )
    
    await update.message.reply_text(
        "🐾 Bem-vindo ao Bot Oficial da FURIA!\n\n"
        "Aqui você encontra:\n"
        "• Próximos jogos e resultados\n"
        "• Elenco completo\n"
        "• Ingressos e transmissões\n"
        "• Stickers da torcida\n\n"
        "VAMOS COM OS FURIOSOS! 🖤🔥",
        reply_markup=teclado
    )
    context.user_data['iniciado'] = True

async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para todas as mensagens"""
    # Resetar o timeout
    await reset_timeout(context, update.effective_chat.id)
    
    # Se for primeira mensagem
    if not context.user_data.get('iniciado'):
        await start(update, context)
        return
    
    # Encaminhar para o handler de menu
    await handle_menu(update, context)

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler para as opções do menu"""
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
    
async def lineup(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await reset_timeout(context, update.effective_chat.id)

    url = "https://draft5.gg/equipe/330-FURIA"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        script = soup.find("script", id="__NEXT_DATA__")
        data = json.loads(script.string)
        
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

    url = "https://draft5.gg/equipe/773-Vitality"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        script = soup.find("script", id="__NEXT_DATA__")
        data = json.loads(script.string)

        for resultado in data["props"]["pageProps"]["results"][:4]:
            adversario = resultado["teamB"]["teamName"]
            placar = f"{resultado['seriesScoreA']}-{resultado['seriesScoreB']}"
            mapas = ", ".join([
                f"{MAP_TRANSLATION.get(s['map']['mapName'], s['map']['mapName'])} ({s['scoreA']}-{s['scoreB']})" 
                for s in resultado["scores"]
            ])
            await update.message.reply_text(
                f"FURIA vs {adversario}: {placar} | Mapas: {mapas}"
            )

    except Exception as e:
        await update.message.reply_text("❌ Erro ao buscar resultados. Tente novamente mais tarde.")

async def prox_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await reset_timeout(context, update.effective_chat.id)

    url = "https://draft5.gg/equipe/330-FURIA"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find("script", id="__NEXT_DATA__")
    data = json.loads(script.string)

    def timestamp_to_date(timestamp):
        return datetime.utcfromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M')

    # Obter as próximas partidas do Vitality
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
    if 'job' in context.chat_data:
        context.chat_data['job'].schedule_removal()
    await update.message.reply_text(
        "🐾 Até logo! Dá uma call se precisar de mais alguma coisa.",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data.clear()

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    
    await reset_timeout(context, update.effective_chat.id)
    # Resetar o timer a cada mensagem recebida
    if 'job' in context.chat_data:
        context.chat_data['job'].schedule_removal()
    
    context.chat_data['job'] = context.job_queue.run_once(
        callback=timeout_callback,
        when=timedelta(minutes=5),
        chat_id=update.effective_chat.id,
        name=str(update.effective_chat.id)
    )

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