# FURIA ChatBot - Documentação

## 📌 Visão Geral
Bot oficial da FURIA CS para Telegram, fornece informações sobre:
- Próximos jogos e resultados
- Elenco e staff
- Links para transmissões e ingressos
- Links Redes Sociais

## 🛠 Tecnologias
- Python 3.10+
- python-telegram-bot (v20+)
- BeautifulSoup4
- Requests
- APScheduler (para timeouts)

## 🔌 API Externa
O bot consome dados de:
```python
API_URL = "https://draft5.gg/equipe/330-FURIA"
```
## 🚀 Como executar (Windows)

```python
python -m venv .venv
# ou .venv\Scripts\activate
pip install -r requirements.txt
```

## Fluxograma do projeto

<div align="center">
  <img src="https://github.com/user-attachments/assets/440fffc8-11eb-41b6-9a27-07f90b90c58e" width="700px"/>









