# 🧠 GPT Trading Bot

Binance 실시간 시세를 기반으로 RSI, MA, 다우이론 등 기술적 지표를 분석하고  
자동으로 알림/시각화를 처리하는 Python 기반 실시간 트레이딩 시스템입니다.

---

## 📦 프로젝트 구조

```bash
GPT/
├── backend/                  # FastAPI 기반 백엔드 앱
├── core/                     # 핵심 로직 (worker, cache, signal 등)
├── storage/                  # SQLite 기반 캐시 시스템
├── utils/                    # 입출력, 스케줄러, 데이터 유틸
├── indicators/               # RSI, MA, 다우이론 등 기술적 지표
├── wsclient/                 # Binance 실시간 캔들 WebSocket 클라이언트
├── alert/                    # 텔레그램 알림 시스템
├── config/                   # 종목 목록(symbols.json) 관리
├── data/                     # 실시간 저장되는 CSV 가격 데이터
<<<<<<< HEAD
└── frontend/                 # Next.js 기반 실시간 대시보드
=======
<<<<<<< HEAD
└── frontend/                 # Next.js 기반 실시간 대시보드
=======
└── frontend/                 # Next.js 기반 실시간 대시보드
>>>>>>> ca5ac79 (chore: 추가 정비)
>>>>>>> 65e604e (🚀 시스템 전체 수정 반영: 실시간 캔들 저장, RSI/MA 시그널, 텔레그램 알림, JST 변환 등)
