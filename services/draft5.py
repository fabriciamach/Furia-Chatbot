import json
from bs4 import BeautifulSoup
import httpx
from config import DRAFT5_TEAM_ID, USER_AGENT
from logging_cfg import logger

async def fetch_draft5_data(
    team_id: int = DRAFT5_TEAM_ID
) -> dict:
    url = f"https://draft5.gg/equipe/{team_id}-FURIA"
    headers = {"User-Agent": USER_AGENT}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        script = soup.find("script", id="__NEXT_DATA__")
        if not script:
            raise ValueError("Dados NEXT_DATA não encontrados no HTML")
        return json.loads(script.string)
    except Exception as e:
        logger.exception("Erro ao buscar dados do Draft5")
        raise