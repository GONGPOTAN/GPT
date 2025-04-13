# storage/alert_cache/alert_cache.py

import sqlite3
from datetime import datetime

DB_PATH = "storage/alert_cache/alert_cache.db"

def create_alert_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            timeframe TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """)
        conn.commit()

def save_alert(symbol: str, timeframe: str, alert_type: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alerts (symbol, timeframe, alert_type, created_at)
            VALUES (?, ?, ?, ?)
        """, (symbol, timeframe, alert_type, datetime.utcnow().isoformat()))
        conn.commit()

def alert_exists(symbol: str, timeframe: str, alert_type: str) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM alerts
            WHERE symbol = ? AND timeframe = ? AND alert_type = ?
        """, (symbol, timeframe, alert_type))
        return cursor.fetchone()[0] > 0