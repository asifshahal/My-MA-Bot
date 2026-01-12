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
async def check_cmd(update, context):
    if not context.args:
        await update.message.reply_text("Usage: /check btc")
        return

    symbol = context.args[0].lower()

    if symbol not in COINS:
        await update.message.reply_text("Unknown coin symbol")
        return

    df = fetch_daily_prices(COINS[symbol])

    messages = []

    for ma in (50, 200):
        signal = check_breakout(df, ma)
        if signal:
            messages.append(
                f"{symbol.upper()} {signal.replace('_', ' ')} MA{ma} (Daily)"
            )

    if not messages:
        await update.message.reply_text(
            f"No MA50 or MA200 breakout for {symbol.upper()}"
        )
    else:
        await update.message.reply_text("\n".join(messages))

async def alerts_cmd(update, context):
    alerts = load_alerts()
    chat = str(update.effective_chat.id)

    if not context.args:
        await update.message.reply_text(
            "Usage:\n"
            "/alerts on btc\n"
            "/alerts on all\n"
            "/alerts off btc\n"
            "/alerts status"
        )
        return

    action = context.args[0].lower()
    alerts.setdefault(chat, [])

    # STATUS
    if action == "status":
        if not alerts[chat]:
            await update.message.reply_text("No active alerts")
        else:
            coins = ", ".join(s.upper() for s in alerts[chat])
            await update.message.reply_text(f"Active alerts:\n{coins}")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Missing coin symbol")
        return

    symbol = context.args[1].lower()

    # ALL COINS
    if symbol == "all":
        if action == "on":
            alerts[chat] = list(COINS.keys())
            save_alerts(alerts)
            await update.message.reply_text(
                "Alerts enabled for ALL popular coins"
            )
            return

        if action == "off":
            alerts[chat] = []
            save_alerts(alerts)
            await update.message.reply_text("All alerts disabled")
            return

    if symbol not in COINS:
        await update.message.reply_text("Unknown coin symbol")
        return

    # SINGLE COIN
    if action == "on":
        if symbol not in alerts[chat]:
            alerts[chat].append(symbol)
        save_alerts(alerts)
        await update.message.reply_text(
            f"Alerts enabled for {symbol.upper()}"
        )

    elif action == "off":
        alerts[chat] = [s for s in alerts[chat] if s != symbol]
        save_alerts(alerts)
        await update.message.reply_text(
            f"Alerts disabled for {symbol.upper()}"
        )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("last", last))
    app.add_handler(CommandHandler("alerts", alerts_cmd))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("alerts", alerts_cmd))
    app.add_handler(CommandHandler("check", check_cmd))


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





