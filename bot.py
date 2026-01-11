from telegram.ext import ApplicationBuilder, CommandHandler
from coingecko import fetch_daily_prices
from indicators import last_ma200_breakout
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

COINS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana"
}

async def start(update, context):
    await update.message.reply_text(
        "Send:\n/last BTC\n/last ETH\n/last SOL"
    )

async def last(update, context):
    if not context.args:
        await update.message.reply_text("Usage: /last BTC")
        return

    symbol = context.args[0].upper()
    if symbol not in COINS:
        await update.message.reply_text("Unsupported coin.")
        return

    df = fetch_daily_prices(COINS[symbol])
    direction, time = last_ma200_breakout(df)

    if not direction:
        await update.message.reply_text("No MA200 breakout found.")
        return

    arrow = "🟢 ABOVE" if direction == "ABOVE" else "🔴 BELOW"

    await update.message.reply_text(
        f"{symbol}\n{arrow} MA200\nDate: {time.date()}"
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("last", last))
    app.run_polling()

if __name__ == "__main__":
    main()
