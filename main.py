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
    return "NY MULTI-CHANNEL NETWORK ENGINE IS LIVE!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. Telegram Bot Setup
BOT_TOKEN = "8891931437:AAGW6oQJeyfh4GzbBAnZG8BhyEs-Mzty5Eo"
bot = telebot.TeleBot(BOT_TOKEN)

# 📢 TARGET LINKS (Aapki details fixed hain)
MY_MAIN_CHANNEL = "@WINGO_1_MINUTES_24"       
BOT_LINK = "https://t.me/Pridictionrobot"   
CHANNEL_LINK = "https://t.me/WINGO_1_MINUTES_24" 

# Doosre groups aur channels ki list save karne ke liye
external_chats = {}

def get_current_period():
    gmt = pytz.timezone('UTC')
    now = datetime.datetime.now(gmt)
    intervals = (now.hour * 60) + now.minute + 1
    ist = pytz.timezone('Asia/Kolkata')
    date_str = datetime.datetime.now(ist).strftime("%Y%m%d")
    return f"{date_str}10001{str(intervals).zfill(4)}"

def check_force_join(user_id):
    """Check karega ki command chalane wala banda aapke channel me hai ya nahi"""
    try:
        member = bot.get_chat_member(MY_MAIN_CHANNEL, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except:
        return True

def wingo_1minute_broadcast_loop():
    last_processed_period = ""
    while True:
        try:
            period = get_current_period()
            
            if last_processed_period != period:
                # Prediction Calculation Logic
                last_four = int(period[-4:])
                pred_seed = ((last_four * 13) + 7) % 2
                next_prediction = "BIG" if pred_seed == 0 else "SMALL"
                
                if next_prediction == "BIG":
                    next_nums = random.sample([5, 6, 7, 8, 9], 2)
                else:
                    next_nums = random.sample([0, 1, 2, 3, 4], 2)
                    
                safe_nums_str = f"{next_nums[0]} or {next_nums[1]}"
                
                # ✨ PREDICTION CARD FORMAT ✨
                prediction_msg = (
                    "🔔 *WINGO 1-MIN PREDICTION* 🔔\n\n"
                    f"🎯 *Period:* `{period}`\n"
                    f"🎲 *Result:* `{next_prediction}`\n"
                    f"🔢 *2 Safe Numbers:* `{safe_nums_str}`\n\n"
                    "⚠️ *Bold Trade:* Khud ke risk par khelehein!\n\n"
                    f"🤖 [🤖 Bot Link]({BOT_LINK}) | 📢 [📢 Join Channel]({CHANNEL_LINK})"
                )
                
                # 1. Aapke khud ke channel par bina ruke direct send hoga
                try:
                    bot.send_message(MY_MAIN_CHANNEL, prediction_msg, parse_mode="Markdown", disable_web_page_preview=True)
                except Exception as e:
                    print(f"Main Channel Error: {e}")
                
                # 2. Jitne bhi doosre approved groups/channels hain, sabme ek sath broadcast hoga
                for ext_chat_id, data in list(external_chats.items()):
                    if data.get("active"):
                        try:
                            bot.send_message(ext_chat_id, prediction_msg, parse_mode="Markdown", disable_web_page_preview=True)
                        except:
                            # Agar bot ko kisi ne group se nikal diya, toh automatic database se hat jayega
                            external_chats.pop(ext_chat_id, None)
                
                last_processed_period = period
                
        except Exception as e:
            print(f"Loop Error: {str(e)}")
            
        time.sleep(2)

# Jab koi doosre group ya channel me bot ko add karke start karega
@bot.message_handler(commands=['start_prediction'])
def handle_external_start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    chat_type = message.chat.type
    
    # Agar koi personal me chalaye toh normal msg dikhao
    if chat_type == "private":
        bot.reply_to(message, f"🤖 *Yeh bot ab direct channels aur groups me chalta hai!*\n\nPredictions dekhne ke liye hamara official channel join karein:\n👉 [JOIN NOW]({CHANNEL_LINK})", parse_mode="Markdown")
        return

    # FORCE JOIN CHECK: Command chalane wala aapka channel joined hona chahiye
    if not check_force_join(user_id):
        bot.reply_to(message, f"❌ *Aap is bot ko is group me active nahi kar sakte!*\n\nPehle bot ke Owner ka official channel join kijiye:\n👉 [CLICK HERE TO JOIN]({CHANNEL_LINK})\n\nJoin karne ke baad fir se `/start_prediction` bhejein.", parse_mode="Markdown", disable_web_page_preview=True)
        return

    # Agar verification pass ho gayi, toh group ko list me daal do
    external_chats[chat_id] = {"active": True}
    bot.reply_to(message, "🚀 *Wingo 1-Minute Engine Active!* Ab is group/channel me bhi har minute automatic signals aana shuru ho jayenge.", parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, f"👋 Hello! Mujhe prediction chalu karne ke liye apne group ya channel me add kijiye aur wahan `/start_prediction` type kijiye!\n\n📢 Main Channel: {CHANNEL_LINK}", parse_mode="Markdown")

if __name__ == "__main__":
    Thread(target=run_web_server, daemon=True).start()
    Thread(target=wingo_1minute_broadcast_loop, daemon=True).start()
    bot.infinity_polling()
    
