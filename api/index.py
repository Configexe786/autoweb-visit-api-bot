from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

TARGET_URL = "https://picamart.vercel.app/"

# Memory data (Session-based: reset hoga par testing ke liye sahi hai)
stats = {
    "today_visits": 0,
    "total_visits": 0,
    "last_visit": "Never"
}

@app.route('/api/keep-alive')
def keep_alive():
    global stats
    try:
        resp = requests.get(TARGET_URL, timeout=15)
        stats["total_visits"] += 1
        stats["today_visits"] += 1
        stats["last_visit"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return jsonify({
            "status": "success",
            "message": "PicaMart Visited!",
            "web_response": resp.status_code,
            "stats": stats
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def dashboard():
    return f"""
    <html>
        <body style="font-family: sans-serif; text-align: center; padding: 50px; background: #f0f2f5;">
            <div style="background: white; display: inline-block; padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">
                <h1 style="color: #1a73e8;">🚀 PicaMart Pinger Dashboard</h1>
                <p>Monitoring: <b>{TARGET_URL}</b></p>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                <div style="display: flex; justify-content: space-around; gap: 20px;">
                    <div>
                        <h3 style="margin-bottom: 5px;">Today</h3>
                        <span style="font-size: 2em; color: #34a853; font-weight: bold;">{stats['today_visits']}</span>
                    </div>
                    <div>
                        <h3 style="margin-bottom: 5px;">Total</h3>
                        <span style="font-size: 2em; color: #4285f4; font-weight: bold;">{stats['total_visits']}</span>
                    </div>
                </div>
                <p style="margin-top: 25px; color: #666;"><b>Last Visit:</b> {stats['last_visit']}</p>
                <br>
                <a href="/api/keep-alive" style="text-decoration: none; background: #1a73e8; color: white; padding: 12px 25px; border-radius: 8px; font-weight: bold;">Ping Now</a>
            </div>
        </body>
    </html>
    """

# Vercel ko handle karne ke liye
app = app
