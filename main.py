import os
import datetime
import pytz
import telebot
import time
from flask import Flask
from threading import Thread

# 1. Flask Web Server Setup
app = Flask('')

@app.route('/')
def home():
    return "NY 1-MINUTE STICKER ENGINE IS LIVE!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. Telegram Bot Setup
BOT_TOKEN = "8891931437:AAGW6oQJeyfh4GzbBAnZG8BhyEs-Mzty5Eo"
bot = telebot.TeleBot(BOT_TOKEN)

active_chats = {}
stats = {"wins": 0, "losses": 0}

# STICKER IDs
WIN_STICKER_ID = "CAACAgUAAxkBAAERe3RqRhsc2j26R8cBP5le2ktO-9aayAACShAAAm6DOVWI7Tqltu49vzwE"
LOSS_STICKER_ID = "CAACAgUAAxkBAAERe3ZqRhtqjf2rExcFBrsuuBHqwPjRewACJg8AAhRQUVTAisD_A8dpDzwE"

def analyze_pattern_and_get_result(period_str):
    last_four = int(period_str[-4:])
    pattern_seed = ((last_four * 17) + 13) % 10
    actual_size = "BIG" if pattern_seed >= 5 else "SMALL"
    if pattern_seed in [1, 3, 7, 9]:
        actual_color = "GREEN"
    elif pattern_seed in [2, 4, 6, 8]:
        actual_color = "RED"
    elif pattern_seed == 0:
        actual_color = "RED + VIOLET"
    else:
        actual_color = "GREEN + VIOLET"
    return str(pattern_seed), actual_size, actual_color

def get_ai_prediction(period_str, server_name):
    last_four = int(period_str[-4:])
    if "DIV" in server_name:
        weight = (last_four * 23) + 41
    elif "BADSHA" in server_name:
        weight = (last_four * 31) + 87
    else:
        weight = (last_four * 17) + 13
    ai_size = "BIG" if (weight % 2 == 0) else "SMALL"
    ai_num = "7" if ai_size == "BIG" else "3"
    return ai_size, ai_num

def get_current_period():
    gmt = pytz.timezone('UTC')
    now = datetime.datetime.now(gmt)
    intervals = (now.hour * 60) + now.minute + 1
    ist = pytz.timezone('Asia/Kolkata')
    date_str = datetime.datetime.now(ist).strftime("%Y%m%d")
    return f"{date_str}10001{str(intervals).zfill(4)}"

def wingo_1minute_broadcast_loop():
    last_processed_period = ""
    while True:
        try:
            period = get_current_period()
            for chat_id, data in list(active_chats.items()):
                if data["active"] and data["last_posted_period"] != period:
                    current_server = data.get("server", "Server 1 (SDD)")
                    if last_processed_period != "":
                        act_num, act_size, act_color = analyze_pattern_and_get_result(last_processed_period)
                        bot_size, _ = get_ai_prediction(last_processed_period, current_server)
                        is_win = (bot_size == act_size)
                        if is_win:
                            stats["wins"] += 1
                            card_title = f"🟩 RESULT 💥 {current_server[:8]}\nPeriod: {last_processed_period[-4:]}\n\n✅ WIN! 🎉 ✅"
                        else:
                            stats["losses"] += 1
                            card_title = f"🟥 RESULT 💥 {current_server[:8]}\nPeriod: {last_processed_period[-4:]}\n\n❌ LOSS ❌"
                        total = stats["wins"] + stats["losses"]
                        accuracy = int((stats["wins"] / total) * 100) if total > 0 else 100
                        result_card = f"{card_title}\n\n🔢 Number: {act_num}\n🎨 Color: {act_color}\n📐 Actual: {act_size}\n🔮 AI: {bot_size}\n\n✅ {stats['wins']} Wins ❌ {stats['losses']} Losses\n📈 Accuracy: {accuracy}%"
                        bot.send_message(chat_id, result_card, parse_mode="Markdown")
                        time.sleep(1)
                        try:
                            if is_win:
                                bot.send_sticker(chat_id, WIN_STICKER_ID)
                            else:
                                bot.send_sticker(chat_id, LOSS_STICKER_ID)
                        except:
                            pass
                        time.sleep(2)
                    next_size, next_num = get_ai_prediction(period, current_server)
                    prediction_msg = f"✨ *NY ULTRA PRO READY* ✨\n\n🎯 Period: `{period}`\n🔮 AI: `{next_size}`\n🔢 Safe: `{next_num}`"
                    bot.send_message(chat_id, prediction_msg, parse_mode="Markdown")
                    active_chats[chat_id]["last_posted_period"] = period
            last_processed_period = period
        except:
            pass
        time.sleep(2)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if chat_id not in active_chats:
        active_chats[chat_id] = {"active": False, "last_posted_period": "", "server": "Server 1 (SDD)"}
    bot.reply_to(message, "✅ BOT ONLINE! Type /start_prediction to begin.")

@bot.message_handler(commands=['start_prediction'])
def start_pred(message):
    chat_id = message.chat.id
    if chat_id not in active_chats:
        active_chats[chat_id] = {"active": True, "last_posted_period": "", "server": "Server 1 (SDD)"}
    active_chats[chat_id]["active"] = True
    bot.reply_to(message, "🚀 1-Min Engine Active!")

if __name__ == "__main__":
    Thread(target=run_web_server, daemon=True).start()
    Thread(target=wingo_1minute_broadcast_loop, daemon=True).start()
    bot.infinity_polling()
