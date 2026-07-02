import os
import datetime
import pytz
import telebot
import time
import random
import threading
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

# Global Control variables with Thread Safety
state_lock = threading.Lock()
engine_state = {
    "GLOBAL_MODE": "AUTOMATIC",  
    "external_chats": {},
    "manual_result_store": {},
    "consecutive_misses": 0,       
    "last_prediction_made": "BIG"
}

# 1. Flask Web Server Setup
app = Flask('')

@app.route('/')
def home():
    with state_lock:
        current_mode = engine_state["GLOBAL_MODE"]
    return f"ANTI-STREAK ENGINE IS LIVE! MODE: {current_mode}"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. Telegram Bot Setup
BOT_TOKEN = "8891931437:AAGW6oQJeyfh4GzbBAnZG8BhyEs-Mzty5Eo"
bot = telebot.TeleBot(BOT_TOKEN)

# 📢 STRICT SYSTEM CONFIGURATION (LOCKING CHANNELS & OWNER ID)       
ADMIN_ID = 7795350715
BOT_LINK = "https://t.me/Pridictionrobot"   
CHANNEL_LINK = "https://t.me/WINGO_1_MINUTES_24" 

def get_current_period():
    gmt = pytz.timezone('UTC')
    now = datetime.datetime.now(gmt)
    intervals = (now.hour * 60) + now.minute + 1
    ist = pytz.timezone('Asia/Kolkata')
    date_str = datetime.datetime.now(ist).strftime("%Y%m%d")
    return f"{date_str}10001{str(intervals).zfill(4)}"

# 🎛️ CONTROL INTERFACE PANEL
def get_admin_panel_keyboard():
    with state_lock:
        current_mode = engine_state["GLOBAL_MODE"]
        misses = engine_state["consecutive_misses"]
        
    markup = InlineKeyboardMarkup()
    status_text = "AUTO" if current_mode == "AUTOMATIC" else "MANUAL"
    layer_text = f"Safety Tier: {misses}"
    
    btn_auto = InlineKeyboardButton("🤖 Set AUTOMATIC Mode", callback_data="set_auto")
    btn_manual = InlineKeyboardButton("✍️ Set MANUAL Mode", callback_data="set_manual")
    btn_status = InlineKeyboardButton(f"Mode: {status_text} | {layer_text}", callback_data="status_info")
    
    markup.row(btn_auto, btn_manual)
    markup.row(btn_status)
    return markup

# ⏱️ 40-SECOND PRECISION LOOP
def precision_prediction_loop():
    last_processed_period = ""
    
    while True:
        try:
            ist = pytz.timezone('Asia/Kolkata')
            now_seconds = datetime.datetime.now(ist).second
            
            if 20 <= now_seconds <= 24:
                period = get_current_period()
                
                if last_processed_period != period:
                    last_four = int(period[-4:])
                    pichla_period = str(int(period) - 1)
                    
                    base_math = ((last_four * 9) + 4) % 10
                    predicted_base_size = "BIG" if base_math >= 5 else "SMALL"
                    
                    with state_lock:
                        current_mode = engine_state["GLOBAL_MODE"]
                        manual_number = engine_state["manual_result_store"].get(pichla_period, None)
                        miss_streak = engine_state["consecutive_misses"]
                        last_pred = engine_state["last_prediction_made"]
                    
                    if current_mode == "MANUAL" and manual_number is not None:
                        num = int(manual_number)
                        actual_last_size = "BIG" if num >= 5 else "SMALL"
                        
                        if actual_last_size == last_pred:
                            with state_lock:
                                engine_state["consecutive_misses"] = 0
                            miss_streak = 0
                        else:
                            with state_lock:
                                engine_state["consecutive_misses"] += 1
                            miss_streak += 1
                        
                        if miss_streak >= 3:
                            next_prediction = actual_last_size
                        elif num == 0 or num == 5:
                            next_prediction = "BIG" if num == 0 else "SMALL"
                        else:
                            next_prediction = "SMALL" if actual_last_size == "BIG" else "BIG"
                    else:
                        group_block = (last_four // 3) % 2
                        time_weight = (last_four + now_seconds) % 4
                        if group_block == 1 and time_weight > 1:
                            next_prediction = "SMALL" if predicted_base_size == "BIG" else "BIG"
                        else:
                            next_prediction = predicted_base_size
                    
                    with state_lock:
                        engine_state["last_prediction_made"] = next_prediction
                    
                    if next_prediction == "BIG":
                        available_nums = [5, 6, 7, 8, 9]
                        num1 = base_math if base_math in available_nums else 7
                        num2 = random.choice([n for n in available_nums if n != num1])
                    else:
                        available_nums = [0, 1, 2, 3, 4]
                        num1 = base_math if base_math in available_nums else 3
                        num2 = random.choice([n for n in available_nums if n != num1])
                        
                    safe_nums_str = f"{num1} or {num2}"
                    
                    prediction_msg = (
                        f"🔔 WINGO 1-MIN PREDICTION 🔔\n\n"
                        f"🎯 Period: {period}\n"
                        f"🎲 Result: {next_prediction}\n"
                        f"🔢 2 Safe Numbers: {safe_nums_str}\n\n"
                        f"⚠️ Risk Alert: Unstable trend mitigation active!"
                    )
                    
                    try:
                        bot.send_message(MY_MAIN_CHANNEL, prediction_msg)
                    except Exception as e:
                        print(f"Broadcast error on channel: {e}")
                    
                    with state_lock:
                        chats_to_send = list(engine_state["external_chats"].items())
                        
                    for ext_chat_id, data in chats_to_send:
                        if data.get("active"):
                            try:
                                bot.send_message(ext_chat_id, prediction_msg)
                            except:
                                with state_lock:
                                    engine_state["external_chats"].pop(ext_chat_id, None)
                                
                    last_processed_period = period
                    
                    with state_lock:
                        if len(engine_state["manual_result_store"]) > 15:
                            engine_state["manual_result_store"].clear()
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Loop operational variance: {e}")
            time.sleep(2)

# 🛑 Admin Panel Callback Direct Interface
@bot.callback_query_handler(func=lambda call: True)
def handle_control_callbacks(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Access Denied.")
        return
        
    if call.data == "set_auto":
        with state_lock:
            engine_state["GLOBAL_MODE"] = "AUTOMATIC"
            engine_state["consecutive_misses"] = 0
        bot.answer_callback_query(call.id, "Automatic mode configured.")
    elif call.data == "set_manual":
        with state_lock:
            engine_state["GLOBAL_MODE"] = "MANUAL"
            engine_state["consecutive_misses"] = 0
        bot.answer_callback_query(call.id, "Manual override configured.")
    elif call.data == "status_info":
        with state_lock:
            current_mode = engine_state["GLOBAL_MODE"]
            misses = engine_state["consecutive_misses"]
        bot.answer_callback_query(call.id, f"Mode: {current_mode} | Tier: {misses}")
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
        bot.send_message(message.chat.id, "⚙️ CONTROL PANEL\n\nConfigure active baseline logic parameters:", reply_markup=get_admin_panel_keyboard())
    except Exception as e:
        print(f"Admin control interface delivery error: {e}")

@bot.message_handler(commands=['update'])
def handle_manual_update(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "Usage format: /update <number>")
            return
            
        input_number = int(args[1])
        if not (0 <= input_number <= 9):
            return
            
        current_period = get_current_period()
        target_period = str(int(current_period) - 1)
        
        with state_lock:
            engine_state["manual_result_store"][target_period] = input_number
            
        bot.reply_to(message, f"Verified: Period {target_period} registered as {input_number}.")
    except Exception as e:
        print(f"Sequence memory update failure: {e}")

@bot.message_handler(commands=['start'])
def start_cmd(message):
    if message.from_user.id != ADMIN_ID:
        return
    bot.reply_to(message, "Welcome Owner! Secure baseline engine is operational. Tap the bottom left Menu button or type /panel.")

if __name__ == "__main__":
    try:
        bot.set_my_commands([
            BotCommand("panel", "🎛️ Open Control Panel (Auto/Manual)"),
            BotCommand("update", "✍️ Submit Live Number Result"),
            BotCommand("start", "🔄 Refresh Bot Context Operations")
        ])
    except Exception as cmd_err:
        print(f"Interface setting error: {cmd_err}")

    Thread(target=run_web_server, daemon=True).start()
    Thread(target=precision_prediction_loop, daemon=True).start()
    bot.infinity_polling(skip_pending=True)
