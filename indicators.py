def last_ma_breakout(df, period):
    df[f"ma{period}"] = df["close"].rolling(period).mean()

    for i in range(len(df) - 1, period, -1):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]

        if prev["close"] < prev[f"ma{period}"] and curr["close"] > curr[f"ma{period}"]:
            return curr["date"].date()

    return None
