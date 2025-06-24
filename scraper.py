from flask import Flask, jsonify
import requests
import json
import re

app = Flask(__name__)  # ✅ This is what was missing

@app.route("/")
def home():
    return "Crazy Time Tracker is running!"

@app.route("/data")
def get_data():
    url = "https://tracksino.com/crazytime"
    r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    text = r.text

    m = re.search(r"window\._INITIAL_STATE_\s*=\s*({.*?});", text)
    if not m:
        return jsonify({"status": "error", "message": "No INITIAL_STATE found"}), 500

    state = json.loads(m.group(1))
    history = state["games"]["history"] if "games" in state and "history" in state["games"] else []

    spins = []
    for item in history[:200]:
        spins.append({
            "time": item.get("timestamp", ""),
            "bonus": item.get("bonus", ""),
            "result": item.get("result", "")
        })
    return jsonify({"status":"success","spins":spins})

# Only needed for local testing
# if __name__ == "__main__":
#     app.run(debug=True)
