from app.notifier.telegram_notifier import send_telegram_message
from app.notifier.formatter import format_grouped_messages
from app.logger.signal_logger import is_duplicate_signal, log_signal, get_continuation_signal

def notify_signal(signals: list):
    messages = []

    for sig in signals:
        if is_duplicate_signal(sig):
            continuation = get_continuation_signal(sig)
            if continuation:
                messages.append(continuation)
            continue
        log_signal(sig)
        messages.append(sig)

    grouped_messages = format_grouped_messages(messages)
    for message in grouped_messages:
        send_telegram_message(message)
