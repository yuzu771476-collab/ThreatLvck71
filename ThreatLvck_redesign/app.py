import os
import sqlite3
from datetime import datetime, timezone

from flask import Flask, render_template, request, jsonify
from analyzer import analyze_url

app = Flask(__name__)

DATABASE = os.path.join(os.path.dirname(__file__), "threatlvck.db")


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# --------------------------------------------------
# DATABASE INITIALIZATION
# --------------------------------------------------

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scanned_at TEXT NOT NULL,
                url TEXT NOT NULL,
                risk_score INTEGER NOT NULL,
                status TEXT NOT NULL,
                findings_count INTEGER NOT NULL
            )
        """)


init_db()


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# ANALYTICS PAGE
# --------------------------------------------------

@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


# --------------------------------------------------
# URL SCANNER
# --------------------------------------------------

@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "")

    if not isinstance(url, str) or not url.strip():
        return jsonify({"error": "Please enter a URL."}), 400

    try:
        result = analyze_url(url)

        with get_db() as db:
            db.execute(
                """INSERT INTO scans
                (scanned_at, url, risk_score, status, findings_count)
                VALUES (?, ?, ?, ?, ?)""",
                (
                    datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    result.get("url", url.strip()),
                    int(result.get("risk_score", 0)),
                    str(result.get("status", "UNKNOWN")),
                    len(result.get("findings", []))
                )
            )

        app.logger.info(
            "Scan completed: score=%s, status=%s",
            result["risk_score"],
            result["status"]
        )

        return jsonify(result)

    except Exception:
        app.logger.exception("URL scan failed")
        return jsonify({
            "error": "The scan failed. Check the VS Code terminal."
        }), 500


# --------------------------------------------------
# ANALYTICS DATA
# --------------------------------------------------

@app.route("/api/analytics")
def analytics_data():
    with get_db() as db:
        rows = db.execute(
            "SELECT id, scanned_at, url, risk_score, status, findings_count "
            "FROM scans ORDER BY id DESC LIMIT 100"
        ).fetchall()

    scans = [dict(row) for row in rows]

    scores = [item["risk_score"] for item in scans]
    total = len(scans)

    high = sum(1 for item in scans if item["risk_score"] >= 40)
    suspicious = sum(
        1 for item in scans
        if 15 <= item["risk_score"] < 40
    )
    low = sum(1 for item in scans if item["risk_score"] < 15)

    return jsonify({
        "scans": scans,
        "total_scans": total,
        "average_score": round(sum(scores) / total, 1) if total else 0,
        "highest_score": max(scores) if scores else 0,
        "high_risk": high,
        "suspicious": suspicious,
        "lower_risk": low
    })


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)