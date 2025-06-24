from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/data")
def get_data():
    url = "https://casinoscores.com/api/live/CrazyTime"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json().get("data", [])
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=False, port=10000)
