def check_volume_spike(symbol):
    url = "https://api.bybit.com/v5/market/kline"
    params = {
        "category": "linear",
        "symbol": symbol,
        "interval": "1",
        "limit": 2,
    }
    try:
        res = requests.get(url, params=params, timeout=5)
        print(f"[DEBUG] Status: {res.status_code}")
        print(f"[DEBUG] Text: {res.text[:200]}")  # Print first 200 chars for preview

        data = res.json()

        if data.get("retCode") != 0:
            print(f"Bybit API error for {symbol}: {data.get('retMsg')}")
            return None

        candles = data["result"]["list"]
        if len(candles) < 2:
            print(f"Not enough data for {symbol}")
            return None

        vol_prev = float(candles[-2][5])
        vol_now = float(candles[-1][5])

        if vol_prev > 0 and vol_now > vol_prev * THRESHOLD:
            return f"📈 Volume Spike (Bybit): {symbol}\nPrev: {vol_prev:.2f}, Now: {vol_now:.2f}"
    except Exception as e:
        print(f"[!] Exception checking {symbol}: {e}")
    return None
