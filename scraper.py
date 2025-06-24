from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(_name_)

def scrape_data():
    url = "https://casinoscores.com/crazy-time/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("table tbody tr")

    data = []
    for row in rows[:50]:  # latest 50 spins
        spin = {}
        cells = row.find_all("td")
        if len(cells) > 2:
            spin["time"] = cells[0].text.strip()
            spin["result"] = cells[1].text.strip()
            spin["multiplier"] = cells[2].text.strip()
            data.append(spin)
    return data

@app.route("/crazytime", methods=["GET"])
def get_data():
    try:
        data = scrape_data()
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=10000)
