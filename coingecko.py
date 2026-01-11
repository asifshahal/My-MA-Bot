import requests
import pandas as pd
import os

API_KEY = os.getenv("COINGECKO_API_KEY")

HEADERS = {
    "accept": "application/json",
    "x-cg-demo-api-key": API_KEY
}

def fetch_daily_prices(coin_id, days=365):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }

    r = requests.get(url, params=params, headers=HEADERS, timeout=20)
    data = r.json()

    if "prices" not in data:
        raise RuntimeError(data)

    df = pd.DataFrame(data["prices"], columns=["time", "close"])
    df["time"] = df["time"].astype(int)
    df["close"] = df["close"].astype(float)
    return df

