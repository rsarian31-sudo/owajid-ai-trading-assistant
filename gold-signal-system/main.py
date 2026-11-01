"""Initial connectivity scaffold. Does not create trading signals yet."""
import logging, os, time
from datetime import datetime, timezone
import MetaTrader5 as mt5
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
TOKEN=os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID=os.getenv("TELEGRAM_CHAT_ID", "").strip()
SYMBOL=os.getenv("MT5_SYMBOL", "XAUUSD").strip()
TERMINAL_PATH=os.getenv("MT5_TERMINAL_PATH", "").strip()
POLL_SECONDS=int(os.getenv("POLL_SECONDS", "15"))
TIMEFRAMES={"1H": mt5.TIMEFRAME_H1, "15M": mt5.TIMEFRAME_M15, "5M": mt5.TIMEFRAME_M5}

def telegram_send(message):
    if not TOKEN or not CHAT_ID: raise RuntimeError("Set Telegram token and chat ID in .env")
    r=requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id":CHAT_ID,"text":message}, timeout=20)
    r.raise_for_status()
    if not r.json().get("ok"): raise RuntimeError("Telegram sendMessage failed")

def connect_mt5():
    kwargs={"path":TERMINAL_PATH} if TERMINAL_PATH else {}
    if not mt5.initialize(**kwargs): raise RuntimeError(f"MT5 initialize failed: {mt5.last_error()}")
    info=mt5.symbol_info(SYMBOL)
    if info is None: raise RuntimeError(f"Unknown MT5 symbol {SYMBOL}; use exact Market Watch symbol")
    if not info.visible and not mt5.symbol_select(SYMBOL, True): raise RuntimeError(f"Cannot select symbol: {mt5.last_error()}")

def get_closed_candles(label, timeframe, count=120):
    rates=mt5.copy_rates_from_pos(SYMBOL, timeframe, 1, count) # skip forming candle
    if rates is None or len(rates)<60: raise RuntimeError(f"Insufficient {label} data: {mt5.last_error()}")
    df=pd.DataFrame(rates); df["time"]=pd.to_datetime(df["time"], unit="s", utc=True)
    return df

def health_check():
    rows=[]
    for label, tf in TIMEFRAMES.items():
        df=get_closed_candles(label, tf); last=df.iloc[-1]
        age=(datetime.now(timezone.utc)-last["time"].to_pydatetime()).total_seconds()
        max_age=int(os.getenv("STALE_DATA_SECONDS", "180"))*(20 if label=="1H" else 1)
        if age>max_age: raise RuntimeError(f"Stale {label} feed ({int(age)} seconds)")
        rows.append(f"{label}: {last['time'].isoformat()} close={last['close']}")
    return "\n".join(rows)

def main():
    connect_mt5(); logging.info("Connected. Connectivity-only mode; BUY/SELL signal engine is disabled.")
    last=0
    while True:
        try:
            if time.time()-last>=3600:
                report=health_check(); logging.info("Market data OK\n%s", report)
                if TOKEN and CHAT_ID: telegram_send("WAJID AI GOLD — market data connection OK\n"+report)
                last=time.time()
        except Exception: logging.exception("Health check failed")
        time.sleep(POLL_SECONDS)

if __name__=="__main__": main()
