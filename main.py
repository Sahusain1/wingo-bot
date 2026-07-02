import os
import datetime
import pytz
import telebot
import time
import random
from flask import Flask
from threading import Thread

# 1. Flask Web Server Setup
app = Flask('')

@app.route('/')
def home():
    return "NY WINGO SYSTEM ENGINE IS LIVE!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. Telegram Bot Setup
BOT_TOKEN = "8891931437:AAGW6oQJeyfh4GzbBAnZG8BhyEs-Mzty5Eo"
bot = telebot.TeleBot(BOT_TOKEN)

# 📢 INTEGRATED LINKS (Aapki details fix kar di hain)
CHANNEL_ID = "@WINGO_1_MINUTES_24"       
BOT_LINK = "https://t.me/Pridictionrobot"   
CHANNEL_LINK = "https://t.me/WINGO_1_MINUTES_24" 

active_chats = {}

def get_current_period():
    gmt = pytz.timezone('UTC')
    now = datetime.datetime.now(gmt)
    intervals = (now.hour * 60) + now.minute + 1
    ist = pytz.timezone('Asia/Kolkata')
    date_str = datetime.datetime.now(ist).strftime("%Y%m%d")
    return f"{date_str}10001{str(intervals).zfill(4)}"

def check_force_join(user_id):
    """Check karega ki user ne mandatory channel join kiya hai ya nahi"""
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        # Agar bot channel me admin nahi hai, toh safe side ke liye true rakhega
        return True

def wingo_1minute_broadcast_loop():
    last_processed_period = ""
    while True:
        try:
            period = get_current_period()
            for chat_id, data in list(active_chats.items()):
                if data["active"] and data["last_posted_period"] != period:
                    
                    # Prediction Calculation
                    last_four = int(period[-4:])
                    pred_seed = ((last_four * 13) + 7) % 2
                    next_prediction = "BIG" if pred_seed == 0 else "SMALL"
                    
                    if next_prediction == "BIG":
                        next_nums = random.sample([5, 6, 7, 8, 9], 2)
                    else:
                        next_nums = random.sample([0, 1, 2, 3, 4], 2)
                        
                    safe_nums_str = f"{next_nums[0]} or {next_nums[1]}"
                    
                    # ✨ AAPKA BATAUYA HUA CARD FORMAT ✨
                    prediction_msg = (
                        "🔔 *WINGO 1-MIN PREDICTION* 🔔\n\n"
                        f"🎯 *Period:* `{period}`\n"
                        f"🎲 *Result:* `{next_prediction}`\n"
                        f"🔢 *2 Safe Numbers:* `{safe_nums_str}`\n\n"
                        "⚠️ *Bold Trade:* Khud ke risk par khelehein!\n\n"
                        f"🤖 [🤖 Bot Link]({BOT_LINK}) | 📢 [📢 Join Channel]({CHANNEL_LINK})"
                    )
                    
                    bot.send_message(chat_id, prediction_msg, parse_mode="Markdown", disable_web_page_preview=True)
                    active_chats[chat_id]["last_posted_period"] = period
                    
            last_processed_period = period
        except Exception as e:
            pass
        time.sleep(2)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if chat_id not in active_chats:
        active_chats[chat_id] = {"active": False, "last_posted_period": ""}
    
    welcome_text = (
        "👋 *Welcome to Wingo Prediction Bot!*\n\n"
        f"🚨 *Prediction chalu karne ke liye aapko hamara official channel join karna zaroori hai:*\n👉 [JOIN CHANNEL NOW]({CHANNEL_LINK})\n\n"
        "Join karne ke baad prediction chalu karne ke liye `/start_prediction` bhejein!"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown", disable_web_page_preview=True)

@bot.message_handler(commands=['start_prediction'])
def start_pred(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Membership Verification
    if not check_force_join(user_id):
        bot.reply_to(message, f"❌ *Pehle hamara official channel join kijiye tabhi predictions unlock hongi:*\n👉 [CLICK HERE TO JOIN]({CHANNEL_LINK})", parse_mode="Markdown", disable_web_page_preview=True)
        return

    if chat_id not in active_chats:
        active_chats[chat_id] = {"active": True, "last_posted_period": ""}
    active_chats[chat_id]["active"] = True
    bot.reply_to(message, "🚀 *Wingo 1-Minute Engine Active!* Har 60 seconds me automated signals is chat me aane shuru ho jayenge.", parse_mode="Markdown")

if __name__ == "__main__":
    Thread(target=run_web_server, daemon=True).start()
    Thread(target=wingo_1minute_broadcast_loop, daemon=True).start()
    bot.infinity_polling()
    
