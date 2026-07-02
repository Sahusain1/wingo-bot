import os
import datetime
import pytz
import telebot
import time
import random
import threading
import json
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

# --- CONFIG ---
MY_MAIN_CHANNEL = -1002675209005 
BOT_TOKEN = "8891931437:AAGW6oQJeyfh4GzbBAnZG8BhyEs-Mzty5Eo"
ADMIN_ID = 7795350715
CHANNEL_LINK = "https://t.me/WINGO_1_MINUTES_24"
BOT_LINK = "https://t.me/Pridictionrobot"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- WEB SERVER (FIXED PORT BINDING) ---
@app.route('/')
def home():
    return "Bot is alive!"

def run_web_server():
    # Render ke liye port zaruri hai
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- BOT LOGIC ---
def get_current_period():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(ist)
    intervals = (now.hour * 60) + now.minute + 1
    return f"{now.strftime('%Y%m%d')}10001{str(intervals).zfill(4)}"

def precision_prediction_loop():
    last_processed_period = ""
    while True:
        try:
            now_seconds = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).second
            if 20 <= now_seconds <= 24:
                period = get_current_period()
                if last_processed_period != period:
                    last_four = int(period[-4:])
                    raw_float = (last_four * 17.35) + 21.45
                    next_prediction = "BIG" if (int(raw_float) % 10) >= 5 else "SMALL"
                    
                    markup = InlineKeyboardMarkup()
                    markup.row(InlineKeyboardButton("🤖 Bot Link", url=BOT_LINK),
                               InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
                    
                    msg = (f"🔔 WINGO 1-MIN PREDICTION 🔔\n\n🎯 Period: {period}\n🎲 Result: {next_prediction}\n\n⚠️ Bold Trade: Khud ke risk par khelehein!")
                    
                    # Send to Main Channel
                    try: bot.send_message(MY_MAIN_CHANNEL, msg, reply_markup=markup)
                    except: pass
                    last_processed_period = period
            time.sleep(1)
        except: time.sleep(5)

# --- RUN ---
if __name__ == "__main__":
    Thread(target=run_web_server, daemon=True).start()
    Thread(target=precision_prediction_loop, daemon=True).start()
    bot.infinity_polling()
    
