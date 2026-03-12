from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Aapki website ka link
TARGET_URL = "https://picamart.vercel.app/"

# Memory storage (Vercel reset karega par visit trigger hoga)
stats = {"today": 0, "total": 0, "last": "Never"}

@app.route('/api/keep-alive')
def keep_alive():
    try:
        r = requests.get(TARGET_URL, timeout=10)
        stats["today"] += 1
        stats["total"] += 1
        stats["last"] = datetime.now().strftime("%H:%M:%S")
        return jsonify({"status": "success", "msg": "Pinged!", "stats": stats})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)})

@app.route('/')
def index():
    return f"<h1>Bot is Online!</h1><p>Today's Pings: {stats['today']}</p><a href='/api/keep-alive'>Manual Ping</a>"

# Ye line Vercel ke liye bahut zaruri hai
def handler(request):
    return app(request)
