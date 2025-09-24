import requests

# 🧾 CONFIG - set these via GitHub secrets
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
THRESHOLD = 1.5  # 50% increase in volume

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

def check_volume_spike(symbol):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": "1m", "limit": 2}
    try:
        res = requests.get(url, params=params, timeout=5)
        data = res.json()
        vol_prev = float(data[-2][5])
        vol_now = float(data[-1][5])
        if vol_prev > 0 and vol_now > vol_prev * THRESHOLD:
            return f"📈 Volume Spike: {symbol}\nPrev: {vol_prev:.2f}, Now: {vol_now:.2f}"
    except Exception as e:
        print(f"Error checking {symbol}: {e}")
    return None

# 🔁 Run check
for symbol in SYMBOLS:
    alert = check_volume_spike(symbol)
    if alert:
        print(alert)
        send_telegram_alert(alert)
