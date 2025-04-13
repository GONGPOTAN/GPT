# alert/telegram_alert.py

import aiohttp
import asyncio
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_telegram_message(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("[텔레그램] 설정이 누락되었습니다.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    print("[텔레그램] 메시지 전송 성공")
                else:
                    error_text = await response.text()
                    print(f"[텔레그램] 실패: {response.status}, {error_text}")
    except Exception as e:
        print(f"[텔레그램] 예외 발생: {e}")

    await asyncio.sleep(0.5)  # 메시지 연속 발송 제한