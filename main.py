import telebot
import datetime
import pytz
import time
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8891931437:AAGW6oQJeyfh4GzbBAnZG8BhyEs-Mzty5Eo"
ADMIN_ID = 7795350715
BOT_LINK = "https://t.me/Pridictionrobot"
CHANNEL_LINK = "https://t.me/WINGO_1_MINUTES_24"

bot = telebot.TeleBot(BOT_TOKEN)
active_groups = {-1003851797245} 

@bot.message_handler(commands=['start_prediction'])
def add_group(message):
    if message.from_user.id == ADMIN_ID:
        active_groups.add(message.chat.id)
        bot.reply_to(message, "✅ Prediction Engine Active!")

def prediction_engine():
    last_processed = ""
    while True:
        try:
            # GMT/UTC Timezone (Kyuki aapne confirm kiya ki 841 match ho raha hai)
            now = datetime.datetime.now(pytz.utc)
            if now.second == 20:
                intervals = (now.hour * 60) + now.minute + 1
                period = f"{now.strftime('%Y%m%d')}10001{str(intervals).zfill(4)}"
                
                if last_processed != period:
                    last_four = int(period[-4:])
                    val = (last_four * 17.35) + 21.45
                    res = "BIG" if (int(val) % 10) >= 5 else "SMALL"
                    
                    # Safe Numbers
                    if res == "BIG":
                        n1, n2 = 5 + (last_four % 5), 5 + ((last_four + 3) % 5)
                    else:
                        n1, n2 = last_four % 5, (last_four + 3) % 5
                    
                    markup = InlineKeyboardMarkup()
                    markup.row(InlineKeyboardButton("🤖 Bot Link", url=BOT_LINK),
                               InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
                    
                    msg = (f"🔔 WINGO 1-MIN PREDICTION 🔔\n\n"
                           f"🎯 Period: {period}\n"
                           f"🎲 Result: {res}\n"
                           f"🔢 2 Safe Numbers: {n1} or {n2}\n\n"
                           f"⚠️ Risk Alert: Unstable trend mitigation active! Follow levels securely.")
                    
                    for chat_id in active_groups:
                        try: bot.send_message(chat_id, msg, reply_markup=markup)
                        except: pass
                    last_processed = period
            time.sleep(1)
        except: time.sleep(5)

app = Flask(__name__)
@app.route('/')
def home(): return "Bot Online"

if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    Thread(target=prediction_engine, daemon=True).start()
    bot.infinity_polling()
    
