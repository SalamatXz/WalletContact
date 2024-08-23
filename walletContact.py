import requests
import time
import json

# توکن بات تلگرام
TELEGRAM_TOKEN = "Token Bot Telegram "

# seed phrase اولیه
seed_phrase = "12 Words for trust wallet"
target_address = "Target Addres"

def send_telegram_message(chat_id, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    requests.post(url, data=payload)

def get_balance(wallet_address):
    url = f"https://api.trongrid.io/v1/accounts/{wallet_address}"
    response = requests.get(url)
    if response.status_code == 200:
        balance = response.json().get('data', [{}])[0].get('balance', 0)
        return balance / 1_000_000  # تبدیل به TRX
    return 0

def main():
    global target_address
    offset = 0

    while True:
        updates = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={offset}").json()

        for update in updates['result']:
            offset = update['update_id'] + 1  # به روز رسانی offset

            chat_id = update['message']['chat']['id']
            text = update['message'].get('text', '')

            if text == "/start":
                send_telegram_message(chat_id, "سلام! از دستورات زیر استفاده کنید:\n"
                                                "/wallet_balance - نمایش موجودی\n"
                                                "/change_wallet <آدرس جدید> - تغییر آدرس ولت")
            elif text.startswith("/wallet_balance"):
                wallet_address = seed_phrase_to_address(seed_phrase)  # تابعی برای تبدیل seed phrase به آدرس
                balance = get_balance(wallet_address)
                send_telegram_message(chat_id, f"موجودی ولت: {balance} TRX")
            elif text.startswith("/change_wallet"):
                args = text.split()
                if len(args) == 2:
                    target_address = args[1]
                    send_telegram_message(chat_id, f"آدرس ولت جدید تنظیم شد: {target_address}")
                else:
                    send_telegram_message(chat_id, "لطفاً آدرس جدید را وارد کنید.")

        time.sleep(1)  # جلوگیری از بار زیاد بر روی سرور

def seed_phrase_to_address(seed_phrase):
    # اینجا باید کدی برای تبدیل seed phrase به آدرس ترون بنویسید
    # این کار ممکن است نیاز به استفاده از کتابخانه‌های خاص داشته باشد
    pass

if __name__ == '__main__':
    main()