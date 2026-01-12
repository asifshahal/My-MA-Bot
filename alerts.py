async def alerts_cmd(update, context):
    alerts = load_alerts()
    chat = str(update.effective_chat.id)

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n/alerts on btc\n/alerts on all\n/alerts off btc"
        )
        return

    action = context.args[0].lower()
    symbol = context.args[1].lower()

    alerts.setdefault(chat, [])

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
            await update.message.reply_text(
                "All alerts disabled"
            )
            return

    if symbol not in COINS:
        await update.message.reply_text("Unknown coin symbol")
        return

    if action == "on":
        if symbol not in alerts[chat]:
            alerts[chat].append(symbol)
        await update.message.reply_text(
            f"Alerts enabled for {symbol.upper()}"
        )

    elif action == "off":
        alerts[chat] = [s for s in alerts[chat] if s != symbol]
        await update.message.reply_text(
            f"Alerts disabled for {symbol.upper()}"
        )

    save_alerts(alerts)
