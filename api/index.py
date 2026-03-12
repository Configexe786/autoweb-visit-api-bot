from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

TARGET_URL = "https://picamart.vercel.app/"

# Memory data (Session-based)
stats = {
    "today_visits": 0,
    "total_visits": 0,
    "last_visit": "Never"
}

# Ye route trigger hoga jab aap /api/keep-alive khologe
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
            "stats": stats
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Ye dashboard dikhayega jab aap sirf main URL khologe
@app.route('/')
def dashboard():
    return f"""
    <html>
        <body style="font-family: sans-serif; text-align: center; padding: 50px; background: #f4f4f4;">
            <div style="background: white; display: inline-block; padding: 30px; border-radius: 15px; shadow: 0px 4px 10px rgba(0,0,0,0.1);">
                <h1>🚀 PicaMart Bot Dashboard</h1>
                <p>Website: <a href="{TARGET_URL}">{TARGET_URL}</a></p>
                <hr>
                <h2 style="color: #2ecc71;">Today's Visits: {stats['today_visits']}</h2>
                <h2 style="color: #3498db;">Total (Session): {stats['total_visits']}</h2>
                <p><b>Last Ping:</b> {stats['last_visit']}</p>
                <br>
                <a href="/api/keep-alive" style="text-decoration: none; background: #333; color: white; padding: 10px 20px; border-radius: 5px;">Test Manual Visit</a>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run()
