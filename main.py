import telebot
import datetime
import pytz
import time
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8891931437:AAGW6oQJeyfh4GzbBAnZG8BhyEs-Mzty5Eo"
ADMIN_ID = 7795350715  # Admin Access Locked
TARGET_ID = -1003851797245 
BOT_LINK = "https://t.me/Pridictionrobot"
CHANNEL_LINK = "https://t.me/WINGO_1_MINUTES_24"

bot = telebot.TeleBot(BOT_TOKEN)

def prediction_engine():
    last_processed = ""
    while True:
        try:
            now = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            if now.second == 20:
                period = f"{now.strftime('%Y%m%d')}10001{(now.hour * 60) + now.minute + 1}"
                
                if last_processed != period:
                    val = (int(period[-4:]) * 17.35) + 21.45
                    res = "BIG" if (int(val) % 10) >= 5 else "SMALL"
                    
                    # Buttons
                    markup = InlineKeyboardMarkup()
                    markup.row(InlineKeyboardButton("🤖 Bot Link", url=BOT_LINK),
                               InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
                    
                    msg = (f"🔔 WINGO 1-MIN PREDICTION 🔔\n\n"
                           f"🎯 Period: {period}\n"
                           f"🎲 Result: {res}\n\n"
                           f"⚠️ Bold Trade: Khud ke risk par khelehein!")
                    
                    bot.send_message(TARGET_ID, msg, reply_markup=markup)
                    last_processed = period
            time.sleep(1)
        except Exception as e:
            time.sleep(5)

# Flask Web Server
app = Flask(__name__)
@app.route('/')
def home(): return "Bot Online"

if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    prediction_engine()
    
