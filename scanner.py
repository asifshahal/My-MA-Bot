def check_breakout(df, ma):
    df[f"ma{ma}"] = df["close"].rolling(ma).mean()

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    if prev["close"] < prev[f"ma{ma}"] and curr["close"] > curr[f"ma{ma}"]:
        return "break_above"

    if prev["close"] > prev[f"ma{ma}"] and curr["close"] < curr[f"ma{ma}"]:
        return "break_below"

    return None
