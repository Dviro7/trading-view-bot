from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "7692770954:AAED9zJC-GHgp2F-W-75dXGrGlTyKX2yyQU")
CHAT_ID = os.getenv("CHAT_ID", "524990252")

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    return requests.post(url, data=data)

@app.route("/", methods=["GET"])
def home():
    return "DVIRTRADER Webhook is live."

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    action = data.get("action", "no-action").upper()
    position_size = data.get("position_size", 0)
    oscillator = data.get("oscillator", 0.0)

    msg = f"🚨 DVIRTRADER SIGNAL 🚨\nAction: {action}\nStochastic: {oscillator}\nSize: {position_size}x"
    send_telegram_message(msg)
    return jsonify({"status": "ok", "message": "Signal received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)