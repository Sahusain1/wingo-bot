import telebot
import datetime
import pytz
import time
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8891931437:AAGW6oQJeyfh4GzbBAnZG8BhyEs-Mzty5Eo"
ADMIN_ID = 7795350715
TARGET_ID = -1003851797245
BOT_LINK = "https://t.me/Pridictionrobot"
CHANNEL_LINK = "https://t.me/WINGO_1_MINUTES_24"

bot = telebot.TeleBot(BOT_TOKEN)

# Prediction Logic
def prediction_engine():
    last_processed = ""
    while True:
        try:
            now = datetime.datetime.now(pytz.utc)
            if now.second == 20: # Har minute ke 20th second par
                intervals = (now.hour * 60) + now.minute + 1
                period = f"{now.strftime('%Y%m%d')}10001{str(intervals).zfill(4)}"
                
                if last_processed != period:
                    last_four = int(period[-4:])
                    val = (last_four * 17.35) + 21.45
                    res = "BIG" if (int(val) % 10) >= 5 else "SMALL"
                    
                    if res == "BIG": n1, n2 = 5 + (last_four % 5), 5 + ((last_four + 3) % 5)
                    else: n1, n2 = last_four % 5, (last_four + 3) % 5
                    
                    markup = InlineKeyboardMarkup()
                    markup.row(InlineKeyboardButton("🤖 Bot Link", url=BOT_LINK),
                               InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
                    
                    msg = (f"🔔 WINGO 1-MIN PREDICTION 🔔\n\n🎯 Period: {period}\n🎲 Result: {res}\n🔢 2 Safe Numbers: {n1} or {n2}\n\n⚠️ Risk Alert: Unstable trend mitigation active! Follow levels securely.")
                    bot.send_message(TARGET_ID, msg, reply_markup=markup)
                    last_processed = period
            time.sleep(1)
        except Exception as e:
            time.sleep(5)

# Flask Server
app = Flask(__name__)
@app.route('/')
def home(): return "Bot Online"

# Main Execution
if __name__ == "__main__":
    # Server Thread
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()
    # Prediction Thread
    Thread(target=prediction_engine, daemon=True).start()
    # Polling - Yahan blocking nahi hogi
    bot.infinity_polling(none_stop=True)
    
