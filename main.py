from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

balance = 10000.0
leverage = 20
position = None
entry_price = 0.0

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

@app.route('/alert', methods=['POST'])
def webhook():
    global balance, position, entry_price
    data = request.json or {}
    alert_msg = data.get("message", "")
    parts = alert_msg.split(":")
    tag = parts[0].strip().upper()
    price = float(parts[1].strip()) if len(parts) > 1 else 0.0

    send_telegram(f"📡 Alert: {tag} @ {price}")

    if tag == "LONG" and not position:
        position = "long"
        entry_price = price
        send_telegram(f"🟢 נכנס ללונג ב-{price}")
    elif tag == "SHORT" and not position:
        position = "short"
        entry_price = price
        send_telegram(f"🔴 נכנס לשורט ב-{price}")
    elif tag == "CLOSE_HALF" and position:
        profit = ((price - entry_price) * leverage) if position == "long" else ((entry_price - price) * leverage)
        balance += profit / 2
        send_telegram(f"✂️ סגר חצי {position.upper()} | רווח: {profit/2:.2f} | יתרה: {balance:.2f}")
    elif tag == "CLOSE_ALL" and position:
        profit = ((price - entry_price) * leverage) if position == "long" else ((entry_price - price) * leverage)
        balance += profit
        send_telegram(f"✅ סגר הכל {position.upper()} | רווח: {profit:.2f} | יתרה: {balance:.2f}")
        position = None

    return "ok"

@app.route('/')
def home():
    return "בוט מסחר פעיל ✅"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
