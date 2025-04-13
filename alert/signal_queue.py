# alert/signal_queue.py

import asyncio

# 전역 큐 객체 (asyncio 기반)
signal_queue = asyncio.Queue()

# 시그널 추가 함수
async def enqueue_signal(signal: dict):
    await signal_queue.put(signal)

# 시그널 가져오기 함수
async def dequeue_signal():
    return await signal_queue.get()