from datetime import datetime

def last_ma200_breakout(df):
    df["ma200"] = df["close"].rolling(200).mean()
    df = df.dropna()

    for i in range(len(df) - 1, 0, -1):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]

        if prev.close < prev.ma200 and curr.close > curr.ma200:
            return "ABOVE", datetime.fromtimestamp(curr.time / 1000)

        if prev.close > prev.ma200 and curr.close < curr.ma200:
            return "BELOW", datetime.fromtimestamp(curr.time / 1000)

    return None, None
