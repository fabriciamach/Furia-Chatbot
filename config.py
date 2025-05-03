import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("FURIA_BOT_TOKEN")
DRAFT5_TEAM_ID = int(os.getenv("DRAFT5_TEAM_ID", 330))
TIMEOUT_MINUTES = int(os.getenv("TIMEOUT_MINUTES", 10))
USER_AGENT = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ..."
)