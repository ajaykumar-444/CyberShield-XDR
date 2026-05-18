from qr_detector import analyze_qr
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from detector import analyze_url
import mysql.connector
from spam_detector import analyze_message
from datetime import datetime

app = Flask(__name__)

# ENABLE CORS
CORS(app)

# =========================
# CREATE UPLOADS FOLDER
# =========================

if not os.path.exists("uploads"):
    os.makedirs("uploads")

# =========================
# MYSQL CONNECTION
# =========================

try:
    db = mysql.connector.connect(
        host="bbp4bttcg8fgr6eiskeh-mysql.services.clever-cloud.com",
        user="uvfi6na2ida0ssjy",
        password="ylEWTT3MmhcZkDh8clcm",
        database="bbp4bttcg8fgr6eiskeh",
        port=3306
    )

    cursor = db.cursor()

    print("MySQL Database Connected!")

except mysql.connector.Error as err:

    print(f"MySQL Connection Failed: {err}")

    db = None
    cursor = None

# =========================
# HOME ROUTE
# =========================

@app.route('/')
def home():

    return jsonify({
        "message": "CyberShield XDR Running Successfully"
    })

# =========================
# URL SCAN ROUTE
# =========================

@app.route('/scan', methods=['POST'])
def scan():

    data = request.json

    url = data.get('url')

    result = analyze_url(url)

    return jsonify(result)

# =========================
# QR SCAN ROUTE
# =========================

@app.route('/scan-qr', methods=['POST'])
def scan_qr():

    file = request.files['file']

    path = os.path.join(
        'uploads',
        file.filename
    )

    file.save(path)

    result = analyze_qr(path)

    return jsonify(result)

# =========================
# SPAM MESSAGE ROUTE
# =========================

@app.route('/scan-message', methods=['POST'])
def scan_message():

    data = request.json

    message = data.get('message')

    result = analyze_message(message)

    return jsonify(result)

# =========================
# RUN SERVER
# =========================

if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host='0.0.0.0',
        port=port
    )