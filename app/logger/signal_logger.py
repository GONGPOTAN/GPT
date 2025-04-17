import os
import json
from datetime import datetime, timedelta

SIGNAL_LOG_FILE = "logs/sent_signals.json"
TIME_LIMIT_MINUTES = 60  # 중복 방지 시간 (분)

def _load_logged_signals():
    if not os.path.exists(SIGNAL_LOG_FILE):
        return {}

    try:
        with open(SIGNAL_LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {
                k: datetime.fromisoformat(v)
                for k, v in data.items()
            }
    except Exception:
        return {}

def _save_logged_signals(data: dict):
    os.makedirs(os.path.dirname(SIGNAL_LOG_FILE), exist_ok=True)
    serializable = {k: v.isoformat() for k, v in data.items()}
    with open(SIGNAL_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)

def _generate_signal_key(signal: dict) -> str:
    return f"{signal['market_type']}-{signal['symbol']}-{signal['interval']}-{signal['type']}"

def is_duplicate_signal(signal: dict) -> bool:
    key = _generate_signal_key(signal)
    logged = _load_logged_signals()
    now = datetime.now()
    if key in logged:
        if now - logged[key] < timedelta(minutes=TIME_LIMIT_MINUTES):
            return True
    return False

def log_signal(signal: dict):
    key = _generate_signal_key(signal)
    logged = _load_logged_signals()
    logged[key] = datetime.now()

    # 오래된 로그 정리
    cutoff = datetime.now() - timedelta(minutes=TIME_LIMIT_MINUTES)
    logged = {k: v for k, v in logged.items() if v >= cutoff}
    _save_logged_signals(logged)

def get_continuation_signal(signal: dict):
    key = _generate_signal_key(signal)
    logged = _load_logged_signals()
    now = datetime.now()

    if key in logged:
        elapsed = now - logged[key]
        if timedelta(minutes=60) < elapsed < timedelta(minutes=120):
            return {
                "type": signal["type"],
                "market_type": signal["market_type"],
                "symbol": signal["symbol"],
                "interval": signal["interval"],
                "detail": f"{signal['detail']} 상태 유지 중 ({int(elapsed.total_seconds() // 60)}분 경과)"
            }
    return None
