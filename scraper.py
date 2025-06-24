@app.route("/data")
def get_data():
    import re
    url = "https://tracksino.com/crazytime"
    r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    text = r.text

    # Extract embedded JSON
    m = re.search(r"window\._INITIAL_STATE_\s*=\s*({.*?});", text)
    if not m:
        return jsonify({"status": "error", "message": "No INITIAL_STATE found"}), 500

    state = json.loads(m.group(1))
    history = state["games"]["history"]  # Path may vary; inspect & update

    spins = []
    for item in history[:200]:
        spins.append({
            "time": item["timestamp"],
            "bonus": item.get("bonus", "") or "",
            "result": item.get("result", "")
        })
    return jsonify({"status":"success","spins":spins})
