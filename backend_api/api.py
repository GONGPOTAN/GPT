# backend_api/api.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.status_cache import (
    get_all_status,
    get_price,
    get_rsi,
    get_trend,
    get_volume_spike,
    get_signal_events
)

app = FastAPI()

# CORS 설정 (전체 허용: 배포 시에는 실제 도메인으로 제한 추천)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 기본 루트 경로: 브라우저에서 / 접속 시 확인 가능
@app.get("/")
async def root():
    return {"message": "🚀 GPT-Trading-Bot API is running!"}

# ✅ 전체 상태 캐시 확인용
@app.get("/api/status")
async def get_status():
    return get_all_status()

# ✅ 종목별 실시간 가격 조회
@app.get("/api/price/{symbol}")
async def price(symbol: str):
    return get_price(symbol)

# ✅ 종목별 RSI 정보 조회 (H1, H4, D)
@app.get("/api/rsi/{symbol}")
async def rsi(symbol: str):
    return get_rsi(symbol)

# ✅ 종목별 다우이론 기반 추세 정보 조회
@app.get("/api/trend/{symbol}")
async def trend(symbol: str):
    return get_trend(symbol)

# ✅ 거래량 급등 종목 리스트
@app.get("/api/volume_spike")
async def volume_spike():
    return get_volume_spike()

# ✅ 최근 시그널 이벤트 목록
@app.get("/api/signal_events")
async def signal_events():
    return get_signal_events()