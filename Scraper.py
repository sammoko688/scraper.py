import time
import json
import threading
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(_name_)
data = {"spins": []}

def scrape_loop():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    while True:
        driver.get("https://casinoscores.com/crazy-time/")
        rows = driver.find_elements("css selector", ".game-history .item")
        spins = [{"result": row.text.strip()} for row in rows[:200]]
        data["spins"] = spins
        time.sleep(60)

@app.route("/latest.json")
def latest():
    return jsonify(data)

if _name_ == "_main_":
    threading.Thread(target=scrape_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
