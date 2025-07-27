from flask import Flask, request, jsonify

app = Flask(__name__)

# שמירת מצב הפוזיציה
trade_state = {
    "position": None,  # None / long / short
    "size": 0
}

@app.route('/')
def home():
    return "Simulated Trading Bot is Live!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data or 'stochastic' not in data:
        return jsonify({"error": "Missing 'stochastic' field"}), 400

    stochastic = float(data['stochastic'])
    response = {}

    # כניסה ללונג
    if stochastic <= -90 and trade_state["position"] is None:
        trade_state["position"] = "long"
        trade_state["size"] = 1.0
        response["action"] = "Opened LONG x20 at stochastic -90"

    # כניסה לשורט
    elif stochastic >= 90 and trade_state["position"] is None:
        trade_state["position"] = "short"
        trade_state["size"] = 1.0
        response["action"] = "Opened SHORT x20 at stochastic +90"

    # סגירת חצי פוזיציה ב־0.01
    elif abs(stochastic) <= 0.01 and trade_state["position"] and trade_state["size"] == 1.0:
        trade_state["size"] = 0.5
        response["action"] = "Closed HALF of position at stochastic 0.01"

    # סגירת לונג אם stochastic > 89
    elif trade_state["position"] == "long" and stochastic >= 89:
        response["action"] = "Closed FULL LONG position at stochastic >= 89"
        trade_state["position"] = None
        trade_state["size"] = 0

    # סגירת שורט אם stochastic < -89
    elif trade_state["position"] == "short" and stochastic <= -89:
        response["action"] = "Closed FULL SHORT position at stochastic <= -89"
        trade_state["position"] = None
        trade_state["size"] = 0

    # סגירה בשינוי כיוון
    elif (trade_state["position"] == "long" and stochastic > 0) or \
         (trade_state["position"] == "short" and stochastic < 0):
        response["action"] = f"Closed FULL {trade_state['position']} position due to direction change"
        trade_state["position"] = None
        trade_state["size"] = 0

    else:
        response["action"] = "No trade action taken"

    print(f"[{trade_state['position']}] Stochastic: {stochastic} -> {response['action']}")
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
