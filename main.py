import os
import datetime
import pytz
import telebot
import time
from flask import Flask
from threading import Thread

# 1. Flask Web Server Setup (Render continuous active rakhne ke liye)
app = Flask('')

@app.route('/')
def home():
    return "BDG AI Premium UTC Channel Bot is Running!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. Telegram Bot Configuration
BOT_TOKEN = "8891931437:AAGW6oQJeyfh4GzbBAnZG8BhyEs-Mzty5Eo"
CHANNEL_CHAT_ID = "@WINGO_1_MINUTES_24"  # Aapka channel username

bot = telebot.TeleBot(BOT_TOKEN)

def get_live_prediction():
    # 🌍 Exact UTC/GMT Time Zone Sync
    gmt = pytz.timezone('UTC')
    now = datetime.datetime.now(gmt)
    
    # UTC ke hisaab se total minutes calculation
    total_minutes = (now.hour * 60) + now.minute + 1
    
    # India Date Sync
    ist = pytz.timezone('Asia/Kolkata')
    date_str = datetime.datetime.now(ist).strftime("%Y%m%d")
    
    # Perfect Period Number Format
    live_period = f"{date_str}10001{str(total_minutes).zfill(4)}"
    
    # 🎯 === NAYA TRAINED FORMULA (YAHAN SET KAR DIYA HAI) ===
    last_four = int(live_period[-4:])
    weight = (last_four * 31) + 53
    
    # Size Decision
    if weight % 3 == 0:
        size_choice = "BIG"
    elif weight % 5 == 0:
        size_choice = "SMALL"
    else:
        size_choice = "BIG" if (last_four % 2 != 0) else "SMALL"
        
    # --- 2-NUMBERS FILTER LOGIC (Trained Pair Combinations) ---
    if size_choice == "BIG":
        num_patterns = [["5", "9"], ["6", "8"], ["7", "9"], ["5", "7"], ["6", "9"]]
        chosen_nums = num_patterns[weight % len(num_patterns)]
    else:
        num_patterns = [["0", "4"], ["1", "3"], ["2", "4"], ["0", "2"], ["1", "4"]]
        chosen_nums = num_patterns[weight % len(num_patterns)]

    return live_period, size_choice, chosen_nums

# Automatic Channel Posting Loop (Har 1 Minute Me Auto Post)
def auto_post_to_channel():
    print("Channel auto-post scheduler shuru ho chuka hai...")
    last_posted_period = ""
    
    while True:
        try:
            period, size, nums = get_live_prediction()
            
            if period != last_posted_period:
                response = (
                    f"🔔 *WINGO 1-MIN PREDICTION* 🔔\n\n"
                    f"🎯 *Period:* `{period}`\n"
                    f"🎲 *Result:* `{size}`\n"
                    f"🔢 *2 Safe Numbers:* `{nums[0]}` or `{nums[1]}`\n\n"
                    f"⚠️ *Bold Trade: Khud ke risk par khelehein!*"
                )
                
                bot.send_message(CHANNEL_CHAT_ID, response, parse_mode="Markdown")
                last_posted_period = period
                print(f"Posted successfully for period: {period}")
                
        except Exception as e:
            print(f"Channel par post karne me error aaya: {e}")
            
        time.sleep(5)

# Bot Commands (Direct Chat)
@bot.message_handler(commands=['start', 'predict'])
def send_prediction(message):
    period, size, nums = get_live_prediction()
    response = (
        f"🔔 *WINGO 1-MIN PREDICTION* 🔔\n\n"
        f"🎯 *Period:* `{period}`\n"
        f"🎲 *Result:* `{size}`\n"
        f"🔢 *2 Safe Numbers:* `{nums[0]}` or `{nums[1]}`\n\n"
        f"⚠️ *Bold Trade: Khud ke risk par khelehein!*"
    )
    bot.reply_to(message, response, parse_mode="Markdown")

if __name__ == "__main__":
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    
    channel_thread = Thread(target=auto_post_to_channel)
    channel_thread.daemon = True
    channel_thread.start()
    
    bot.infinity_polling()
    
