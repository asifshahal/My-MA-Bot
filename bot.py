from telegram.ext import ApplicationBuilder, CommandHandler
from coingecko import fetch_daily_prices
from indicators import last_ma_breakouts
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

    ma50, ma200 = last_ma_breakouts(df)

    lines = [symbol]

    if ma50:
        arrow = "🟢 ABOVE" if ma50[0] == "ABOVE" else "🔴 BELOW"
        lines.append(f"{arrow} MA50  — {ma50[1].date()}")

    if ma200:
        arrow = "🟢 ABOVE" if ma200[0] == "ABOVE" else "🔴 BELOW"
        lines.append(f"{arrow} MA200 — {ma200[1].date()}")

    if len(lines) == 1:
        await update.message.reply_text("No MA50 or MA200 breakout found.")
        return

    await update.message.reply_text("\n".join(lines))



def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("last", last))
    app.run_polling()

if __name__ == "__main__":
    main()



