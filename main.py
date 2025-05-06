import os
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from flask import Flask
import asyncio

# متغیرهای محیطی
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHANNELS = os.getenv("SOURCE_CHANNELS").split(",")  # لیست کانال‌های منبع
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")  # کانال مقصد

# ایجاد کلاینت تلگرام با استفاده از فایل سشن
client = TelegramClient('bot.session', API_ID, API_HASH)

async def start_bot():
    try:
        # بررسی اگر بات قبلاً وارد شده باشد
        if not await client.is_user_authorized():
            await client.start(bot_token=BOT_TOKEN)
        print("Bot started successfully!")
    except FloodWaitError as e:
        print(f"Flood wait error: Waiting for {e.seconds} seconds.")
        await asyncio.sleep(e.seconds)  # صبر تا پایان محدودیت
        await start_bot()  # تلاش مجدد برای ورود
    except Exception as e:
        print(f"Error during bot startup: {e}")

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

    # اجرای کلاینت تلگرام
    with client:
        client.loop.run_until_complete(start_bot())
        client.run_until_disconnected()
