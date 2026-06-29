from telegram import Bot
import asyncio
from datetime import datetime
import random
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# --- APNI DETAILS ---
TOKEN = '8891931437:AAGW6oQJeyfh4GzbBAnZG8BhyEs-Mzty5Eo'  
CHANNEL_ID = '@WINGO_1_MINUTES_24' 

# ⚠️ APNA LIVE PERIOD NUMBER YAHAN UPDATE KAREIN (Jo abhi chalne wala ho)
live_period = 20260629100010623  

# Render free web service ke liye dummy port open rakhna zaroori hai
def run_dummy_server():
    class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is Running")
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

async def send_predictions():
    global live_period
    bot = Bot(token=TOKEN)
    print("Only Prediction Wingo Bot Free Server par chalu ho raha hai...")
    
    while True:
        size_choice = random.choice(["BIG", "SMALL"])
        
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
            live_period += 1
        except Exception as e:
            print(f"Prediction error: {e}")

        now = datetime.now()
        seconds_left = 60 - now.second
        await asyncio.sleep(seconds_left)

if __name__ == "__main__":
    # Dummy server ko background thread me chalana
    threading.Thread(target=run_dummy_server, daemon=True).start()
    asyncio.run(send_predictions())
