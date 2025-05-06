import os
from telethon import TelegramClient, events
from flask import Flask

# متغیرهای محیطی
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHANNELS = os.getenv("SOURCE_CHANNELS").split(",")  # لیست کانال‌های منبع
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")  # کانال مقصد

# ایجاد کلاینت تلگرام
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

print("Bot started successfully!")

# رویداد برای دریافت و فوروارد کردن پیام‌ها
@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forward_message(event):
    try:
        print(f"New message received from {event.chat_id}: {event.message.text}")
        await client.send_message(TARGET_CHANNEL, event.message)
        print(f"Message forwarded to {TARGET_CHANNEL}")
    except Exception as e:
        print(f"Error while forwarding message: {e}")

# باز کردن پورت جعلی برای Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    # اجرای Flask برای باز کردن پورت
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    # اجرای تلگرام کلاینت تا زمانی که قطع شود
    client.run_until_disconnected()
