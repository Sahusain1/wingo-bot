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

# --- CONFIGURATION ---
MY_MAIN_CHANNEL = -1002675209005 # Aapka main channel ID
BOT_TOKEN = "8891931437:AAGW6oQJeyfh4GzbBAnZG8BhyEs-Mzty5Eo"
ADMIN_ID = 7795350715
CHANNEL_LINK = "https://t.me/WINGO_1_MINUTES_24"
BOT_LINK = "https://t.me/Pridictionrobot"

# Memory for dynamic groups
STORAGE_FILE = "bot_memory.json"
def load_memory():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as f:
            try: return json.load(f)
            except: return {"external_chats": {str(MY_MAIN_CHANNEL): {"active": True}}}
    return {"external_chats": {str(MY_MAIN_CHANNEL): {"active": True}}}

def save_memory(data):
    with open(STORAGE_FILE, "w") as f: json.dump(data, f)

engine_state = {"external_chats": load_memory().get("external_chats", {})}

bot = telebot.TeleBot(BOT_TOKEN)

# --- ENGINE ---
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
                    
                    # Buttons
                    markup = InlineKeyboardMarkup()
                    markup.row(InlineKeyboardButton("🤖 Bot Link", url=BOT_LINK),
                               InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
                    
                    msg = (f"🔔 WINGO 1-MIN PREDICTION 🔔\n\n🎯 Period: {period}\n🎲 Result: {next_prediction}\n\n⚠️ Bold Trade: Khud ke risk par khelehein!")
                    
                    # Broadcast to ALL registered chats
                    chats = list(engine_state["external_chats"].keys())
                    for chat_id in chats:
                        try: bot.send_message(int(chat_id), msg, reply_markup=markup)
                        except: pass
                    last_processed_period = period
            time.sleep(1)
        except: time.sleep(5)

# --- COMMANDS ---
@bot.message_handler(commands=['start_prediction'])
def add_chat(message):
    if message.from_user.id != ADMIN_ID: return
    engine_state["external_chats"][str(message.chat.id)] = {"active": True}
    save_memory({"external_chats": engine_state["external_chats"]})
    bot.reply_to(message, "✅ Channel/Group linked for 24/7 predictions!")

# [Add /panel and other handlers here...]
Thread(target=precision_prediction_loop, daemon=True).start()
bot.infinity_polling()
