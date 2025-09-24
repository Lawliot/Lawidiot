def check_volume_spike(symbol):
    url = "https://api.bybit.com/v5/market/kline"
    params = {
        "category": "linear",
        "symbol": symbol,
        "interval": "1",
        "limit": 2,
    }

    print(f"[INFO] Checking {symbol}...")
    print(f"[INFO] Request URL: {url}")
    print(f"[INFO] Request Params: {params}")

    try:
        res = requests.get(url, params=params, timeout=10)
        print(f"[DEBUG] Response Status: {res.status_code}")
        print(f"[DEBUG] Response Headers: {res.headers}")
        print(f"[DEBUG] Response Text Preview: {res.text[:300]}")

        data = res.json()

        if data.get("retCode") != 0:
            print(f"[ERROR] Bybit API error for {symbol}: {data.get('retMsg')}")
            return None

        candles = data["result"]["list"]
        if len(candles) < 2:
            print(f"[WARN] Not enough data for {symbol}")
            return None

        vol_prev = float(candles[-2][5])
        vol_now = float(candles[-1][5])

        if vol_prev > 0 and vol_now > vol_prev * THRESHOLD:
            return f"📈 Volume Spike (Bybit): {symbol}\nPrev: {vol_prev:.2f}, Now: {vol_now:.2f}"
    except Exception as e:
        print(f"[EXCEPTION] {symbol} request failed: {e}")
    return None
