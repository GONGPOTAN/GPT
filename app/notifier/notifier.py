from app.notifier.telegram_notifier import send_telegram_message
from app.notifier.formatter import format_grouped_messages
import pprint

def notify_signal(signals: list):
    messages = format_grouped_messages(signals)
    for message in messages:
        send_telegram_message(message)
