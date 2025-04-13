from app.notifier.telegram_notifier import send_telegram_message

if __name__ == "__main__":
    test_message = "✅ <b>텔레그램 알림 테스트</b>\n이 메시지가 도착하면 성공입니다."
    success = send_telegram_message(test_message)

    if success:
        print("📨 메시지 전송 성공")
    else:
        print("❌ 메시지 전송 실패")