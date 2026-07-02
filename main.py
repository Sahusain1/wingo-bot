import os
import datetime
import pytz
import telebot
import time
import threading
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# CONFIG
BOT_TOKEN = "8891931437:AAGW6oQJeyfh4GzbBAnZG8BhyEs-Mzty5Eo"
ADMIN_ID = 7795350715
CHANNEL_LINK = "https://t.me/WINGO_1_MINUTES_24"
BOT_LINK = "https://t.me/Pridictionrobot"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active and running!"

# --- LOGIC ---
def prediction_worker():
    last_processed = ""
    # List of all target IDs (Aap yahan aur bhi add kar sakte ho)
    target_channels = [-1002675209005] 
    
    while True:
        try:
            now = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            # Period calculation
            intervals = (now.hour * 60) + now.minute + 1
            period = f"{now.strftime('%Y%m%d')}10001{str(intervals).zfill(4)}"
            
            if 20 <= now.second <= 25 and last_processed != period:
                # Math Formula
                last_four = int(period[-4:])
                val = (last_four * 17.35) + 21.45
                result = "BIG" if (int(val) % 10) >= 5 else "SMALL"
                
                # Buttons & Msg
                markup = InlineKeyboardMarkup()
                markup.row(InlineKeyboardButton("🤖 Bot Link", url=BOT_LINK),
                           InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
                msg = f"🔔 WINGO 1-MIN PREDICTION 🔔\n\n🎯 Period: {period}\n🎲 Result: {result}\n\n⚠️ Bold Trade: Khud ke risk par khelehein!"
                
                # FORCE BROADCAST
                for ch_id in target_channels:
                    try:
                        bot.send_message(ch_id, msg, reply_markup=markup)
                    except Exception as e:
                        print(f"Error in {ch_id}: {e}")
                
                last_processed = period
            time.sleep(1)
        except Exception as e:
            time.sleep(5)

# --- START ---
if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()
    prediction_worker() # Polling aur worker ko alag rakha hai
