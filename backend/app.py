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

# MYSQL CONNECTION
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="AJAY KUMAR@2006",
    database="cybershield"
)

cursor = db.cursor()

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

    return jsonify(result)

# URL HISTORY ROUTE
@app.route('/history')
def history():

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

    return jsonify(result)

# SPAM MESSAGE SCAN ROUTE
@app.route('/scan-message', methods=['POST'])
def scan_message():

    data = request.json

    message = data.get('message')

    result = analyze_message(message)

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

    return jsonify(result)

# RUN SERVER
if __name__ == '__main__':
    app.run(debug=True)