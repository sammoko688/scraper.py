from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Home route to confirm the service is live
@app.route("/")
def home():
    return "✅ Crazy Time Tracker is running!"

# Example scraping route
@app.route("/data")
def get_data():
    url = "https://casinoscores.com/crazy-time/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Modify this to match real data on CasinoScores
        results = []
        game_elements = soup.select(".game-result-item")  # You must update this selector
        for el in game_elements[:10]:
            results.append(el.text.strip())

        return jsonify({"status": "success", "results": results})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
