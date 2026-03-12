from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Settings
TARGET_URL = "https://picamart.vercel.app/"

# Ye variables memory mein rahenge (Reset hote rahenge, par visits count karenge)
stats = {
    "today_visits": 0,
    "total_visits": 0,
    "last_visit": "Never",
    "start_date": datetime.now().strftime("%Y-%m-%d")
}

@app.route('/api/keep-alive')
def keep_alive():
    global stats
    try:
        # Website visit logic
        resp = requests.get(TARGET_URL, timeout=15)
        
        # Stats Update
        stats["total_visits"] += 1
        stats["today_visits"] += 1
        stats["last_visit"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return jsonify({
            "status": "success",
            "message": "PicaMart Visited Successfully",
            "web_response": resp.status_code,
            "stats": {
                "today": stats["today_visits"],
                "total": stats["total_visits"],
                "last_visit_at": stats["last_visit"]
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def dashboard():
    # API kholte hi ye dashboard dikhega
    return f"""
    <html>
        <body style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h1>🚀 PicaMart Bot Dashboard</h1>
            <p>Target: <b>{TARGET_URL}</b></p>
            <div style="font-size: 24px; margin: 20px; border: 1px solid #ccc; display: inline-block; padding: 20px; border-radius: 10px;">
                <p>Today's Visits: <span style="color: green;">{stats['today_visits']}</span></p>
                <p>Total Visits (Session): <span style="color: blue;">{stats['total_visits']}</span></p>
            </div>
            <p>Last Ping: {stats['last_visit']}</p>
            <hr>
            <p>Cron Job is active via Vercel.</p>
        </body>
    </html>
    """
