import requests
import os
import time

# List of symbols to monitor
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]

# Bybit USDT Perpetual Kline endpoint
BASE_URL = "https://api.bybit.com/v5/market/kline"

# Volume spike threshold
VOLUME_SPIKE_MULTIPLIER = 2.5

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("[ERROR] Telegram credentials not set.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        res = requests.post(url, data=payload)
        if res.status_code != 200:
            print(f"[TELEGRAM ERROR] {res.status_code}: {res.text}")
        else:
            print(f"[TELEGRAM] Sent: {message}")
    except Exception as e:
        print(f"[TELEGRAM EXCEPTION] {e}")

def fetch_kline(symbol):
    try:
        params = {
            "category": "linear",
            "symbol": symbol,
            "interval": "1",
            "limit": 2
        }
        res = requests.get(BASE_URL, params=params)
        if res.status_code != 200:
            print(f"[ERROR] Bybit API error for {symbol}: {res.text}")
            return None

        result = res.json()
        return result.get("result", {}).get("list", [])
    except Exception as e:
        print(f"[EXCEPTION] {symbol}: {e}")
        return None

def check_volume_spike(symbol):
    print(f"[INFO] Checking {symbol}")
    data = fetch_kline(symbol)
    if not data or len(data) < 2:
        print(f"[WARN] Not enough data for {symbol}")
        return

    # Parse volume from the 2 latest candles
    prev = data[0]
    curr = data[1]

    prev_vol = float(prev[5])
    curr_vol = float(curr[5])

    if curr_vol >= prev_vol * VOLUME_SPIKE_MULTIPLIER:
        msg = f"🚨 Volume spike on {symbol}!\nPrevious: {prev_vol:.2f}\nCurrent: {curr_vol:.2f}"
        print(f"[ALERT] {msg}")
        send_telegram(msg)
    else:
        print(f"[OK] No spike on {symbol} ({curr_vol:.2f} vs {prev_vol:.2f})")

def main():
    print("🔥 Bot starting...")
    print("✅ Inside main(). Running checks...")
    for symbol in SYMBOLS:
        check_volume_spike(symbol)
        time.sleep(1)  # be polite with the API

    print("✅ All checks complete.")
    print("✅ Bot finished.")

if __name__ == "__main__":
    main()
