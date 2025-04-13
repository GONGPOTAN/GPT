# alert/alert_cache.py

import aiosqlite
import os
import asyncio

DB_PATH = "storage/alert_cache.db"

async def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id TEXT PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def is_alert_sent(alert_id: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT 1 FROM alerts WHERE id = ?", (alert_id,)) as cursor:
            return await cursor.fetchone() is not None

async def mark_alert_sent(alert_id: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR REPLACE INTO alerts (id) VALUES (?)", (alert_id,))
        await db.commit()