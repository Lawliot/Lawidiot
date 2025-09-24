import requests

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
THRESHOLD = 1.5  # 50% volume spike

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

def check_volume_spike(symbol):
    url = "https://fapi.binance.com/fapi/v1/klines"
    params = {"symbol": symbol, "interval": "1m", "limit": 2}
    try:
        res = requests.get(url, params=params, timeout=5)
        data = res.json()

        if isinstance(data, dict) and "code" in data:
            print(f"Binance API error for {symbol}: {data['msg']}")
            return None

        if len(data) < 2:
            print(f"Not enough data for {symbol}")
            return None

        vol_prev = float(data[-2][5])
        vol_now = float(data[-1][5])

        if vol_prev > 0 and vol_now > vol_prev * THRESHOLD:
            return f"📈 Volume Spike (Futures): {symbol}\nPrev: {vol_prev:.2f}, Now: {vol_now:.2f}"
    except Exception as e:
        print(f"[!] Exception checking {symbol}: {e}")
    return None

for symbol in SYMBOLS:
    alert = check_volume_spike(symbol)
    if alert:
        print(alert)
        send_telegram_alert(alert)
