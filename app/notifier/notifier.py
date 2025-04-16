from app.notifier.telegram_notifier import send_telegram_message
from app.notifier.formatter import format_message
import pprint

def notify_signal(signals: list):
    for signal_data in signals:
        if not isinstance(signal_data, dict):
            continue  # Skip if signal_data is not a dict

        required_keys = ["type", "market_type", "symbol", "interval", "detail"]
        if not all(key in signal_data for key in required_keys):
            continue  # Skip if any required key is missing

        message = format_message(
            signal_type=signal_data["type"],
            market_type=signal_data["market_type"],
            symbol=signal_data["symbol"],
            interval=signal_data["interval"],
            detail=signal_data["detail"]
        )
        send_telegram_message(message)
