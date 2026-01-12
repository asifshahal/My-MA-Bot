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

from alerts import load_alerts, save_alerts
from coingecko import fetch_daily_prices
from scanner import check_breakout
from coins import COINS

async def daily_alerts(context):
    alerts = load_alerts()

    for chat_id, symbols in alerts.items():
        for sym in symbols:
            df = fetch_daily_prices(COINS[sym])

            for ma in (50, 200):
                signal = check_breakout(df, ma)
                if signal:
                    await context.bot.send_message(
                        chat_id=int(chat_id),
                        text=f"{sym.upper()} {signal.replace('_', ' ')} MA{ma} (Daily)"
                    )

async def alerts_cmd(update, context):
    alerts = load_alerts()
    chat = str(update.effective_chat.id)

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /alerts on btc")
        return

    action, symbol = context.args[0], context.args[1].lower()

    if symbol not in COINS:
        await update.message.reply_text("Unknown coin")
        return

    alerts.setdefault(chat, [])

    if action == "on":
        if symbol not in alerts[chat]:
            alerts[chat].append(symbol)
        await update.message.reply_text(f"Alerts enabled for {symbol.upper()}")

    elif action == "off":
        alerts[chat] = [s for s in alerts[chat] if s != symbol]
        await update.message.reply_text(f"Alerts disabled for {symbol.upper()}")

    save_alerts(alerts)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("last", last))
    app.add_handler(CommandHandler("alerts", alerts_cmd))

    app.job_queue.run_repeating(
    daily_alerts,
    interval=86400,
    first=10
    )
    app.run_polling()


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("PONG")

if __name__ == "__main__":
    main()




