import pandas as pd
import pandas_ta as ta


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    for n in [5, 10, 20, 60, 120, 250]:
        df[f"SMA_{n}"] = ta.sma(df.close, length=n)

    macd = ta.macd(df.close, fast=12, slow=26, signal=9)
    if macd is not None:
        df["MACD_12_26_9"] = macd["MACD_12_26_9"]
        df["MACDh_12_26_9"] = macd["MACDh_12_26_9"]
        df["MACDs_12_26_9"] = macd["MACDs_12_26_9"]

    adx = ta.adx(df.high, df.low, df.close, length=14)
    if adx is not None:
        df["ADX_14"] = adx["ADX_14"]
        df["DMP_14"] = adx["DMP_14"]
        df["DMN_14"] = adx["DMN_14"]

    df["RSI_6"] = ta.rsi(df.close, length=6)
    df["RSI_14"] = ta.rsi(df.close, length=14)

    stoch = ta.stoch(df.high, df.low, df.close, k=9, d=3)
    if stoch is not None:
        df["STOCHk_9_3"] = stoch["STOCHk_9_3_3"]
        df["STOCHd_9_3"] = stoch["STOCHd_9_3_3"]

    df["WILLR_14"] = ta.willr(df.high, df.low, df.close, length=14)

    bb = ta.bbands(df.close, length=20, std=2)
    if bb is not None:
        df["BBL_20_2.0"] = bb["BBL_20_2.0_2.0"]
        df["BBM_20_2.0"] = bb["BBM_20_2.0_2.0"]
        df["BBU_20_2.0"] = bb["BBU_20_2.0_2.0"]

    df["ATRr_14"] = ta.atr(df.high, df.low, df.close, length=14)
    df["OBV"] = ta.obv(df.close, df.volume)
    df["VOL_SMA_5"] = ta.sma(df.volume, length=5)
    df["VOL_SMA_20"] = ta.sma(df.volume, length=20)

    return df


def resample_ohlcv(df: pd.DataFrame, freq: str) -> pd.DataFrame:
    return df.resample(freq).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()


def _valid(*vals) -> bool:
    """Check all values are not None and not NaN."""
    return all(v is not None and pd.notna(v) for v in vals)


def _na(dimension: str, name: str) -> dict:
    return {"dimension": dimension, "name": name, "value": "数据不足", "signal": "中性", "note": "数据不足"}


def generate_signals(indicators_df: pd.DataFrame) -> list[dict]:
    signals = []
    latest = indicators_df.iloc[-1]
    close = latest.get("close")

    # MA
    sma5 = latest.get("SMA_5")
    sma20 = latest.get("SMA_20")
    sma60 = latest.get("SMA_60")
    if _valid(close, sma20, sma60):
        if close > sma20 > sma60:
            s = "多头"; n = "均线多头排列"
        elif close < sma20 < sma60:
            s = "空头"; n = "均线空头排列"
        else:
            s = "中性"; n = "均线交织"
        signals.append({"dimension": "趋势", "name": "均线系统", "value": f"收盘 {close:.2f}, MA20 {sma20:.2f}, MA60 {sma60:.2f}", "signal": s, "note": n})
    else:
        signals.append(_na("趋势", "均线系统"))

    # MACD
    dif = latest.get("MACD_12_26_9")
    dea = latest.get("MACDs_12_26_9")
    if _valid(dif, dea):
        if dif > dea:
            s = "多头"; n = "金叉"
        else:
            s = "空头"; n = "死叉"
        signals.append({"dimension": "趋势", "name": "MACD", "value": f"DIF {dif:.4f}, DEA {dea:.4f}", "signal": s, "note": n})
    else:
        signals.append(_na("趋势", "MACD"))

    # ADX
    adx = latest.get("ADX_14")
    dmp = latest.get("DMP_14")
    dmn = latest.get("DMN_14")
    if _valid(adx, dmp, dmn):
        if adx > 25 and dmp > dmn:
            s = "多头"; n = "趋势向上 (+DI > -DI)"
        elif adx > 25 and dmn > dmp:
            s = "空头"; n = "趋势向下 (-DI > +DI)"
        else:
            s = "中性"; n = "趋势不明 (ADX<25)"
        signals.append({"dimension": "趋势", "name": "ADX", "value": f"ADX {adx:.2f}, +DI {dmp:.2f}, -DI {dmn:.2f}", "signal": s, "note": n})
    else:
        signals.append(_na("趋势", "ADX"))

    # RSI
    rsi14 = latest.get("RSI_14")
    if _valid(rsi14):
        if rsi14 > 70:
            s = "空头"; n = f"超买区 {rsi14:.1f}"
        elif rsi14 < 30:
            s = "多头"; n = f"超卖区 {rsi14:.1f}"
        else:
            s = "中性"; n = f"{rsi14:.1f}"
        signals.append({"dimension": "动量", "name": "RSI(14)", "value": f"{rsi14:.1f}", "signal": s, "note": n})
    else:
        signals.append(_na("动量", "RSI(14)"))

    # KDJ
    k = latest.get("STOCHk_9_3")
    d = latest.get("STOCHd_9_3")
    if _valid(k, d):
        cross = "金叉" if k > d else "死叉"
        zone = ""
        if k > 80 and d > 80:
            zone = ", 超买"
        elif k < 20 and d < 20:
            zone = ", 超卖"
        s = "多头" if k > d else "空头"
        signals.append({"dimension": "动量", "name": "KDJ", "value": f"K {k:.1f}, D {d:.1f}", "signal": s, "note": f"K>D {cross}{zone}" if k > d else f"K<D {cross}{zone}"})
    else:
        signals.append(_na("动量", "KDJ"))

    # Williams %R
    willr = latest.get("WILLR_14")
    if _valid(willr):
        if willr > -20:
            s = "空头"; n = f"超买区 ({willr:.1f})"
        elif willr < -80:
            s = "多头"; n = f"超卖区 ({willr:.1f})"
        else:
            s = "中性"; n = f"{willr:.1f}"
        signals.append({"dimension": "动量", "name": "Williams %R", "value": f"{willr:.1f}", "signal": s, "note": n})
    else:
        signals.append(_na("动量", "Williams %R"))

    # Bollinger Bands
    bbl = latest.get("BBL_20_2.0")
    bbm = latest.get("BBM_20_2.0")
    bbu = latest.get("BBU_20_2.0")
    if _valid(close, bbl, bbm, bbu):
        if close <= bbl:
            s = "多头"; n = "触及下轨 (可能反弹)"
        elif close >= bbu:
            s = "空头"; n = "触及上轨 (可能回落)"
        else:
            s = "中性"; n = "价格在布林带内"
        signals.append({"dimension": "波动率", "name": "布林带", "value": f"上轨 {bbu:.2f}, 中轨 {bbm:.2f}, 下轨 {bbl:.2f}", "signal": s, "note": n})
    else:
        signals.append(_na("波动率", "布林带"))

    # ATR
    atr = latest.get("ATRr_14")
    if _valid(atr):
        s = "中性"; n = f"{atr:.4f}"
        if "ATRr_14" in indicators_df.columns:
            atr_series = indicators_df["ATRr_14"].dropna()
            if len(atr_series) >= 10:
                atr_avg = atr_series.tail(min(20, len(atr_series))).mean()
                if atr < atr_avg * 0.8:
                    s = "多头"; n = "波动率收窄 (可能突破)"
                elif atr > atr_avg * 1.5:
                    s = "空头"; n = "波动率放大 (风险增加)"
        signals.append({"dimension": "波动率", "name": "ATR", "value": f"{atr:.4f}", "signal": s, "note": n})
    else:
        signals.append(_na("波动率", "ATR"))

    # OBV
    obv = latest.get("OBV")
    if _valid(obv) and "OBV" in indicators_df.columns:
        obv_avg = indicators_df["OBV"].tail(min(20, len(indicators_df))).mean()
        if obv > obv_avg:
            s = "多头"; n = "OBV 上升 (资金流入)"
        elif obv < obv_avg:
            s = "空头"; n = "OBV 下降 (资金流出)"
        else:
            s = "中性"; n = f"{obv:.0f}"
        signals.append({"dimension": "成交量", "name": "OBV", "value": f"{obv:.0f}", "signal": s, "note": n})
    else:
        signals.append(_na("成交量", "OBV"))

    # Volume
    vol = latest.get("volume")
    vol_sma20 = latest.get("VOL_SMA_20")
    if _valid(vol, vol_sma20):
        note = "放量" if vol > vol_sma20 * 1.5 else "缩量" if vol < vol_sma20 * 0.5 else "正常"
        signals.append({"dimension": "成交量", "name": "成交量", "value": f"成交量 {vol:.0f}, 20日均量 {vol_sma20:.0f}", "signal": "中性", "note": note})
    else:
        signals.append(_na("成交量", "成交量"))

    return signals


def summarize(daily_signals, weekly_signals) -> dict:
    all_signals = daily_signals + weekly_signals
    bullish = sum(1 for s in all_signals if s["signal"] == "多头")
    bearish = sum(1 for s in all_signals if s["signal"] == "空头")
    neutral = sum(1 for s in all_signals if s["signal"] == "中性")
    total = bullish + bearish + neutral

    if total == 0:
        return {
            "verdict": "中性 ➡",
            "note": "无有效信号",
            "bullish_count": 0,
            "bearish_count": 0,
            "neutral_count": 0
        }

    if bullish / total > 0.5:
        verdict = "偏多 ⬆"
    elif bearish / total > 0.5:
        verdict = "偏空 ⬇"
    else:
        verdict = "中性 ➡"

    def dominant(signals):
        counts = {"多头": 0, "空头": 0, "中性": 0}
        for s in signals:
            counts[s["signal"]] += 1
        max_count = max(counts.values())
        for sig, count in counts.items():
            if count == max_count and count > 0:
                return sig
        return "中性"

    daily_dom = dominant(daily_signals)
    weekly_dom = dominant(weekly_signals)

    if daily_dom == weekly_dom and daily_dom != "中性":
        note = f"日线/周线共振看{'多' if daily_dom == '多头' else '空'}"
    elif verdict == "偏多 ⬆":
        note = f"多头信号{bullish}个, 空头信号{bearish}个"
    elif verdict == "偏空 ⬇":
        note = f"空头信号{bearish}个, 多头信号{bullish}个"
    else:
        note = f"多空信号均衡 (多头{bullish}, 空头{bearish}, 中性{neutral})"

    return {
        "verdict": verdict,
        "note": note,
        "bullish_count": bullish,
        "bearish_count": bearish,
        "neutral_count": neutral
    }


def analyze(df: pd.DataFrame) -> dict:
    daily_indicators = compute_indicators(df.copy())
    daily_signals = generate_signals(daily_indicators)

    weekly_df = resample_ohlcv(df.copy(), 'W')
    weekly_indicators = compute_indicators(weekly_df.copy())
    weekly_signals = generate_signals(weekly_indicators)

    summary = summarize(daily_signals, weekly_signals)

    return {
        "daily": daily_signals,
        "weekly": weekly_signals,
        "summary": summary
    }
