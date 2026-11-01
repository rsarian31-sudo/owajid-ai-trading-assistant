# WAJID AI GOLD SIGNAL SYSTEM

Signal-only XAUUSD alert service. Initial integration scaffold; no trading signals are enabled yet.

## Design
- Exness MT5 terminal on a Windows VPS supplies broker-matched XAUUSD candles.
- 1H determines direction, 15M detects a setup, and 5M confirms only after candle close.
- Telegram delivers BUY/SELL with entry, SL and TP1-TP4.
- News blackout, deduplication, backtest and demo validation are required before live alerts.

## Setup
1. Install MetaTrader 5 on a Windows VPS and log in to Exness there. Never send credentials in chat or commit them.
2. Create a Telegram bot with @BotFather, add it to your private channel/group with permission to post, and obtain the chat ID.
3. Copy `.env.example` to `.env` and fill the Telegram token, chat ID, MT5 terminal path and exact Market Watch symbol.
4. Install Python 3.11+, then `pip install -r requirements.txt`.
5. Run `python main.py`.

This scaffold only checks MT5 candle connectivity and Telegram delivery. It deliberately does not generate trading signals until the strategy and news filter have been implemented and tested. Keep `.env` secret.