import os
import datetime
import pytz
import telebot
import time
import random
import threading
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Thread safety ke liye locks aur global dictionary
state_lock = threading.Lock()
engine_state = {
    "GLOBAL_MODE": "AUTOMATIC",  # Default State: AUTOMATIC ya MANUAL
    "external_chats": {},
    "manual_result_store": {}
}

# 1. Flask Web Server Setup
app = Flask('')

@app.route('/')
def home():
    with state_lock:
        current_mode = engine_state["GLOBAL_MODE"]
    return f"HYBRID CONTROL ENGINE IS RUNNING! MODE: {current_mode}"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. Telegram Bot Setup
BOT_TOKEN = "8891931437:AAGW6oQJeyfh4GzbBAnZG8BhyEs-Mzty5Eo"
bot = telebot.TeleBot(BOT_TOKEN)

# 📢 TARGET LINKS
MY_MAIN_CHANNEL = "@WINGO_1_MINUTES_24"       
BOT_LINK = "https://t.me/Pridictionrobot"   
CHANNEL_LINK = "https://t.me/WINGO_1_MINUTES_24" 
ADMIN_ID = 5334460773

def get_current_period():
    gmt = pytz.timezone('UTC')
    now = datetime.datetime.now(gmt)
    intervals = (now.hour * 60) + now.minute + 1
    ist = pytz.timezone('Asia/Kolkata')
    date_str = datetime.datetime.now(ist).strftime("%Y%m%d")
    return f"{date_str}10001{str(intervals).zfill(4)}"

def check_force_join(user_id):
    try:
        member = bot.get_chat_member(MY_MAIN_CHANNEL, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except:
        return True

# 🎛️ MODE PANEL KEYBOARD FOR ADMIN
def get_admin_panel_keyboard():
    with state_lock:
        current_mode = engine_state["GLOBAL_MODE"]
        
    markup = InlineKeyboardMarkup()
    status_text = "🤖 AUTO ACTIVE" if current_mode == "AUTOMATIC" else "✍️ MANUAL ACTIVE"
    
    btn_auto = InlineKeyboardButton("🤖 Set AUTOMATIC Mode", callback_data="set_auto")
    btn_manual = InlineKeyboardButton("✍️ Set MANUAL Mode", callback_data="set_manual")
    btn_status = InlineKeyboardButton(f"Current Status: {status_text}", callback_data="status_info")
    
    markup.row(btn_auto, btn_manual)
    markup.row(btn_status)
    return markup

# ⏱️ 40-SECOND PRECISION BROADCAST LOOP
def precision_prediction_loop():
    last_processed_period = ""
    
    while True:
        try:
            ist = pytz.timezone('Asia/Kolkata')
            now_seconds = datetime.datetime.now(ist).second
            
            # EXACT 20th SECOND PAR POST HOGA (40 Sec Pehle)
            if 20 <= now_seconds <= 24:
                period = get_current_period()
                
                if last_processed_period != period:
                    last_four = int(period[-4:])
                    pichla_period = str(int(period) - 1)
                    
                    base_math = ((last_four * 9) + 4) % 10
                    predicted_base_size = "BIG" if base_math >= 5 else "SMALL"
                    
                    # Safe thread reads
                    with state_lock:
                        current_mode = engine_state["GLOBAL_MODE"]
                        manual_number = engine_state["manual_result_store"].get(pichla_period, None)
                    
                    # MODE ROUTING LOGIC WITH FALLBACK
                    if current_mode == "MANUAL" and manual_number is not None:
                        num = int(manual_number)
                        # Violet Override Triggers
                        if num == 0 or num == 5:
                            next_prediction = "BIG" if num == 0 else "SMALL"
                        else:
                            last_size = "BIG" if num >= 5 else "SMALL"
                            next_prediction = "SMALL" if last_size == "BIG" else "BIG"
                    else:
                        # AUTOMATIC MODE FALLBACK (Run if Auto is set OR if Manual has no input number)
                        group_block = (last_four // 3) % 2
                        time_weight = (last_four + now_seconds) % 4
                        if group_block == 1 and time_weight > 1:
                            next_prediction = "SMALL" if predicted_base_size == "BIG" else "BIG"
                        else:
                            next_prediction = predicted_base_size
                    
                    if next_prediction == "BIG":
                        available_nums = [5, 6, 7, 8, 9]
                        num1 = base_math if base_math in available_nums else 8
                        num2 = random.choice([n for n in available_nums if n != num1])
                    else:
                        available_nums = [0, 1, 2, 3, 4]
                        num1 = base_math if base_math in available_nums else 1
                        num2 = random.choice([n for n in available_nums if n != num1])
                        
                    safe_nums_str = f"{num1} or {num2}"
                    
                    prediction_msg = (
                        "🔔 *WINGO 1-MIN PREDICTION* 🔔\n\n"
                        f"🎯 *Period:* `{period}`\n"
                        f"🎲 *Result:* `{next_prediction}`\n"
                        f"🔢 *2 Safe Numbers:* `{safe_nums_str}`\n\n"
                        "⚠️ *Bold Trade:* 3-Level safety plan strictly follow karein!\n\n"
                        f"🤖 [🤖 Bot Link]({BOT_LINK}) | 📢 [📢 Join Channel]({CHANNEL_LINK})"
                    )
                    
                    try:
                        bot.send_message(MY_MAIN_CHANNEL, prediction_msg, parse_mode="Markdown", disable_web_page_preview=True)
                    except Exception as e:
                        print(f"Broadcast error: {e}")
                    
                    with state_lock:
                        chats_to_send = list(engine_state["external_chats"].items())
                        
                    for ext_chat_id, data in chats_to_send:
                        if data.get("active"):
                            try:
                                bot.send_message(ext_chat_id, prediction_msg, parse_mode="Markdown", disable_web_page_preview=True)
                            except:
                                with state_lock:
                                    engine_state["external_chats"].pop(ext_chat_id, None)
                                
                    last_processed_period = period
                    
                    with state_lock:
                        if len(engine_state["manual_result_store"]) > 15:
                            engine_state["manual_result_store"].clear()
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Loop core issue: {e}")
            time.sleep(2)

# 🛑 TELEGRAM CALL INTERACTION BLOCK
@bot.callback_query_handler(func=lambda call: True)
def handle_control_callbacks(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "❌ Aap admin nahi ho!", show_alert=True)
        return
        
    if call.data == "set_auto":
        with state_lock:
            engine_state["GLOBAL_MODE"] = "AUTOMATIC"
        bot.answer_callback_query(call.id, "🤖 Automatic Mode Set Ho Gaya!", show_alert=False)
    elif call.data == "set_manual":
        with state_lock:
            engine_state["GLOBAL_MODE"] = "MANUAL"
        bot.answer_callback_query(call.id, "✍️ Manual Mode Set Ho Gaya!", show_alert=False)
    elif call.data == "status_info":
        with state_lock:
            current_mode = engine_state["GLOBAL_MODE"]
        bot.answer_callback_query(call.id, f"Current active structure: {current_mode}", show_alert=True)
        return
        
    try:
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=get_admin_panel_keyboard())
    except:
        pass

@bot.message_handler(commands=['panel'])
def send_admin_control_panel(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        bot.reply_to(message, "⚙️ *BDG GAME HYBRID CONTROL PANEL*\n\nNiche diye gaye button se direct Automatic ya Manual behavior control karein:", parse_mode="Markdown", reply_markup=get_admin_panel_keyboard())
    except Exception as e:
        print(f"Panel send error: {e}")

@bot.message_handler(commands=['update'])
def handle_manual_update(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "⚠️ Format: `/update <number>` (e.g. `/update 5`)", parse_mode="Markdown")
            return
            
        input_number = int(args[1])
        if not (0 <= input_number <= 9):
            bot.reply_to(message, "❌ Invalid single digit target number.")
            return
            
        current_period = get_current_period()
        target_period = str(int(current_period) - 1)
        
        with state_lock:
            engine_state["manual_result_store"][target_period] = input_number
            
        bot.reply_to(message, f"✅ Target Locked!\nPeriod `{target_period}` actual number is `{input_number}`.", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Session processing error: {e}")

@bot.message_handler(commands=['start_prediction'])
def handle_external_start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.chat.type == "private":
        return
    if not check_force_join(user_id):
        bot.reply_to(message, f"❌ Join: {CHANNEL_LINK}")
        return
    with state_lock:
        engine_state["external_chats"][chat_id] = {"active": True}
    bot.reply_to(message, "🚀 *Wingo Precision Engine Attached!*")

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, f"👋 Active me in groups via `/start_prediction`!\n📢 Official Node: {CHANNEL_LINK}")

if __name__ == "__main__":
    Thread(target=run_web_server, daemon=True).start()
    Thread(target=precision_prediction_loop, daemon=True).start()
    bot.infinity_polling()
    
