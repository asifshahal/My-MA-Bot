from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN
from coingecko import fetch_daily_prices
from indicators import last_ma_breakout

COINS = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "sol": "solana",
}

async def last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /last btc")
        return

    symbol = context.args[0].lower()
    if symbol not in COINS:
        await update.message.reply_text("Unsupported coin")
        return

    df = fetch_daily_prices(COINS[symbol])

    ma50 = last_ma_breakout(df, 50)
    ma200 = last_ma_breakout(df, 200)

    msg = f"{symbol.upper()} (Daily)\n"
    msg += f"50 MA breakout: {ma50 or 'Not in last 365 days'}\n"
    msg += f"200 MA breakout: {ma200 or 'Not in last 365 days'}"

    await update.message.reply_text(msg)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("last", last))
    app.run_polling()

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("PONG")

if __name__ == "__main__":
    main()
