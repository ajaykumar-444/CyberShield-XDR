from qr_detector import analyze_qr
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from detector import analyze_url
import mysql.connector
from datetime import datetime
from spam_detector import analyze_message

app = Flask(__name__)
CORS(app)

# CREATE UPLOADS FOLDER IF NOT EXISTS
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# MYSQL CONNECTION WITH CLOUD ERROR HANDLING
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="AJAY KUMAR@2006",
        database="cybershield"
    )
    cursor = db.cursor()
    print("Database connection established successfully!")
except mysql.connector.Error as err:
    print(f"Database connection failed: {err}")
    print("Running application without database services for cloud hosting.")
    db = None
    cursor = None

# HOME ROUTE
@app.route('/')
def home():
    return jsonify({
        "message": "CyberShield XDR Running"
    })

# URL SCAN ROUTE
@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    url = data.get('url')

    result = analyze_url(url)

    # Only attempt database insert if connection exists
    if db and cursor:
        try:
            query = """
            INSERT INTO scanned_urls
            (url, score, classification, scan_time)
            VALUES (%s, %s, %s, %s)
            """
            values = (
                url,
                result['score'],
                result['classification'],
                datetime.now()
            )
            cursor.execute(query, values)
            db.commit()
        except mysql.connector.Error as err:
            print(f"Database insert failed: {err}")

    return jsonify(result)

# URL HISTORY ROUTE
@app.route('/history')
def history():
    # If no database is available, return an empty list or error message
    if not db or not cursor:
        return jsonify({"message": "History unavailable (Database disconnected)"}), 503

    try:
        cursor.execute(
            "SELECT * FROM scanned_urls ORDER BY id DESC"
        )
        rows = cursor.fetchall()
        output = []
        for row in rows:
            output.append({
                "id": row[0],
                "url": row[1],
                "score": row[2],
                "classification": row[3],
                "time": row[4]
            })
        return jsonify(output)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# QR SCAN ROUTE
@app.route('/scan-qr', methods=['POST'])
def scan_qr():
    file = request.files['file']

    path = os.path.join(
        'uploads',
        file.filename
    )
    file.save(path)

    result = analyze_qr(path)

    # Only attempt database insert if connection exists
    if db and cursor:
        try:
            query = """
            INSERT INTO qr_scans
            (qr_data, result, scan_time)
            VALUES (%s, %s, %s)
            """
            values = (
                result.get('qr_data'),
                result.get('classification'),
                datetime.now()
            )
            cursor.execute(query, values)
            db.commit()
        except mysql.connector.Error as err:
            print(f"Database insert failed: {err}")

    return jsonify(result)

# SPAM MESSAGE SCAN ROUTE
@app.route('/scan-message', methods=['POST'])
def scan_message():
    data = request.json
    message = data.get('message')

    result = analyze_message(message)

    # Only attempt database insert if connection exists
    if db and cursor:
        try:
            query = """
            INSERT INTO spam_messages
            (message, result, scan_time)
            VALUES (%s, %s, %s)
            """
            values = (
                message,
                result['classification'],
                datetime.now()
            )
            cursor.execute(query, values)
            db.commit()
        except mysql.connector.Error as err:
            print(f"Database insert failed: {err}")

    return jsonify(result)

# RUN SERVER
if __name__ == '__main__':
    # Render assigns a port dynamically via environment variables
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)