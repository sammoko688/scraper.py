import time
import json
import threading
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

app = Flask(_name_)
data = {"spins": []}

def scrape_loop():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    
    while True:
        try:
            driver.get("https://casinoscores.com/crazy-time/")
            time.sleep(5)  # Wait for full load

            rows = driver.find_elements(By.CSS_SELECTOR, ".game-history .item")
            spins = []

            for row in rows[:200]:
                result = row.text.strip()
                if result:
                    spins.append({"result": result})

            data["spins"] = spins
        except Exception as e:
            print("Scraping failed:", str(e))

        time.sleep(60)

@app.route("/latest.json")
def latest():
    return jsonify(data)

if _name_ == "_main_":
    threading.Thread(target=scrape_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)
