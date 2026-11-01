"""WAJID AI GOLD - initial MT5 + Telegram integration scaffold.

This version intentionally does not generate trading signals yet.
It verifies live MT5 candles and Telegram connectivity only.
"""
import logging
import os
import time
from datetime import datetime, timezone

import MetaTrader5 as mt5
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()
SYMBOL = os.getenv("MT5_SYMBOL", "XAUUSD").strip()
TERMINAL_PATH = os.getenv("MT5_TERMINAL_PATH", "").strip()
POLL_SECONDS = int(os.getenv("POLL_SECONDS", "15"))

TIMEFRAMES = {
    "1H": mt5.TIMEFRAME_H1,
    "15M": mt5.TIMEFRAME_M15,
    "5M": mt5.TIMEFRAME_M5,
}


def telegram_send(message: str) -> None:
    if not TOKEN or not CHAT_ID:
        raise RuntimeError("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env")
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(url, json={"chat_id": CHAT_ID, "text": message}, timeout=20)
    response.raise_for_status()
    payload = response.json()
    if not payload.get("ok"):
        raise RuntimeError(f"Telegram API rejected message: {payload}")


def mt5_connect() -> None:
    kwargs = {"path": TERMINAL_PATH} if TERMINAL_PATH else {}
    if not mt5.initialize(**kwargs):
        raise RuntimeError(f"MT5 initialize failed: {mt5.last_error()}")
    info = mt5.symbol_info(SYMBOL)
    if info is None:
        raise RuntimeError(f"Symbol {SYMBOL!r} not found. Set MT5_SYMBOL to the exact Market Watch symbol.")
    if not info.visible and not mt5.symbol_select(SYMBOL, True):
        raise RuntimeError(f"Could not select {SYMBOL}: {mt5.last_error()}")
    logging.info("Connected to MT5; symbol=%s", SYMBOL)


def closed_candles(label: str, timeframe: int, count: int = 120) -> pd.DataFrame:
    # Position 1 skips the currently-forming candle; only closed candles are analyzed.
    rates = mt5.copy_rates_from_pos(SYMBOL, timeframe, 1, count)
    if rates is None or len(rates) < 60:
        raise RuntimeError(f"Insufficient {label} candles: {mt5.last_error()}")
    frame = pd.DataFrame(rates)
    frame["time"] = pd.to_datetime(frame["time"], unit="s", utc=True)
    return frame


def health_check() -> str:
    blocks = []
    for label, timeframe in TIMEFRAMES.items():
        frame = closed_candles(label, timeframe)
        last = frame.iloc[-1]
        age = (datetime.now(timezone.utc) - last["time"].to_pydatetime()).total_seconds()
        if age > int(os.getenv("STALE_DATA_SECONDS", "180")) * (12 if label == "1H" else 1):
            raise RuntimeError(f"{label} feed is stale ({int(age)} seconds old)")
        blocks.append(f"{label}: {last['time'].isoformat()} | close={last['close']}")
    return "\n".join(blocks)


def main() -> None:
    mt5_connect()
    logging.info("Health-check mode started. No BUY/SELL alerts are generated in this scaffold.")
    last_report = 0.0
    while True:
        try:
            if time.time() - last_report >= 3600:
                report = health_check()
                logging.info("Market data OK\n%s", report)
                if TOKEN and CHAT_ID:
                    telegram_send("WAJID AI GOLD — data connection OK\n" + report)
                last_report = time.time()
        except Exception:
            logging.exception("Health check failed")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
