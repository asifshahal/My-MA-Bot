from datetime import datetime

def last_ma_breakouts(df):
    df["ma50"] = df["close"].rolling(50).mean()
    df["ma200"] = df["close"].rolling(200).mean()
    df = df.dropna()

    last_50 = None
    last_200 = None

    for i in range(len(df) - 1, 0, -1):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]

        # MA50 breakout
        if last_50 is None:
            if prev.close < prev.ma50 and curr.close > curr.ma50:
                last_50 = ("ABOVE", datetime.fromtimestamp(curr.time / 1000))
            elif prev.close > prev.ma50 and curr.close < curr.ma50:
                last_50 = ("BELOW", datetime.fromtimestamp(curr.time / 1000))

        # MA200 breakout
        if last_200 is None:
            if prev.close < prev.ma200 and curr.close > curr.ma200:
                last_200 = ("ABOVE", datetime.fromtimestamp(curr.time / 1000))
            elif prev.close > prev.ma200 and curr.close < curr.ma200:
                last_200 = ("BELOW", datetime.fromtimestamp(curr.time / 1000))

        if last_50 and last_200:
            break

    return last_50, last_200
