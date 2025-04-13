# backend_api/api.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GPT Trading Bot API")

# CORS 설정 (필요 시 수정 가능)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 보안상 배포 시 제한 필요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 예시 라우트 (추후 상태 조회 등 추가 가능)
@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.get("/")
async def root():
    return {"status": "✅ GPT Trading Bot 백엔드 작동 중"}