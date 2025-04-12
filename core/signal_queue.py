# core/signal_queue.py

import asyncio

# 전역 큐 인스턴스 생성 (다양한 시그널이 이 큐로 들어감)
signal_queue = asyncio.Queue()