import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

if not COINGECKO_API_KEY:
    raise RuntimeError("COINGECKO_API_KEY is not set")
