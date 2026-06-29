from telegram import Bot
import asyncio
from datetime import datetime, timedelta
import random

# --- APNI DETAILS ---
TOKEN = '8891931437:AAGW6oQJeyfh4GzbBAnZG8BhyEs-Mzty5Eo'  
CHANNEL_ID = '@WINGO_1_MINUTES_24' 

# ⚠️ LIVE PERIOD NUMBER YAHAN UPDATE KAREIN (Jo abhi chalne wala ho)
live_period = 20260629100010610  

async def send_predictions():
    global live_period
    bot = Bot(token=TOKEN)
    print("Only Prediction Wingo Bot chalu ho raha hai...")
    
    while True:
        # --- Nayi Prediction Banana ---
        size_choice = random.choice(["BIG", "SMALL"])
        
        # Size ke mutabik sahi matching single number chunna
        if size_choice == "BIG":
            number_choice = random.choice([5, 6, 7, 8, 9])
        else:
            number_choice = random.choice([0, 1, 2, 3, 4])

        prediction_msg = (
            f"🔔 **WINGO 1-MIN PREDICTION** 🔔\n\n"
            f"🎯 **Period:** `{live_period}`\n"
            f"🎲 **Result:** {size_choice}\n"
            f"🔢 **Single Number:** {number_choice}\n\n"
            f"⚠️ *Khud ke risk par khelehein!*"
        )

        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=prediction_msg, parse_mode='Markdown')
            print(f"Prediction sent for period: {live_period}")
            
            # Agle minute ke liye period number badhana (+1)
            live_period += 1
        except Exception as e:
            print(f"Prediction error: {e}")

        # Exact agle minute ke :00 second tak wait karna (Game ke time se match karne ke liye)
        now = datetime.now()
        seconds_left = 60 - now.second
        await asyncio.sleep(seconds_left)

if __name__ == "__main__":
    asyncio.run(send_predictions())
  
