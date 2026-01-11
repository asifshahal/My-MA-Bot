import requests
import pandas as pd
from config import COINGECKO_API_KEY

BASE = "https://api.coingecko.com/api/v3"

HEADERS = {
    "accept": "application/json",
    "x-cg-demo-api-key": COINGECKO_API_KEY
}

def fetch_daily_prices(coin_id):
    url = f"{BASE}/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": 365,
        "interval": "daily"
    }

    r = requests.get(url, headers=HEADERS, params=params, timeout=15)
    data = r.json()

    if "prices" not in data:
        raise RuntimeError(data)

    df = pd.DataFrame(data["prices"], columns=["ts", "close"])
    df["date"] = pd.to_datetime(df["ts"], unit="ms")

    return df[["date", "close"]]
