import os
import json
from datetime import datetime

def log_analysis_result(market_type, symbol, interval, result):
    log_path = "logs/analyze_result.json"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "market_type": market_type,
        "symbol": symbol,
        "interval": interval,
        "result": {k: (v.tolist() if hasattr(v, "tolist") else v) for k, v in result.items()}
    }

    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                log_data = json.load(f)
        except json.JSONDecodeError:
            log_data = []
    else:
        log_data = []

    log_data.append(log_entry)

    MAX_ENTRIES = 150
    log_data = log_data[-MAX_ENTRIES:]

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

def log_system_event(event_type, message):
    log_path = "logs/system_log.json"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": event_type,  # e.g., 'signal', 'error', 'info'
        "message": message
    }

    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                log_data = json.load(f)
        except json.JSONDecodeError:
            log_data = []
    else:
        log_data = []

    log_data.append(log_entry)

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

def safe_log(message):
    try:
        print(message)
    except Exception:
        pass
