print("🔥 Bot starting...", flush=True)

import requests
import functools
print = functools.partial(print, flush=True)

def main():
    print("✅ Inside main(). Running checks...")

    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    for symbol in symbols:
        print(f"[INFO] Checking {symbol}")
        # Simulated logic
        print(f"[MOCK] {symbol} volume check complete.")

    print("✅ All checks complete.")

if __name__ == "__main__":
    import traceback
    try:
        main()
    except Exception as e:
        print("❌ Unhandled Exception:")
        traceback.print_exc()

print("✅ Bot finished.", flush=True)
