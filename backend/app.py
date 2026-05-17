from pymongo import MongoClient
from datetime import datetime
from qr_detector import analyze_qr
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from detector import analyze_url
import mysql.connector
from spam_detector import analyze_message

app = Flask(__name__)

# ENABLE CORS
CORS(app)

# =========================
# MONGODB CONNECTION
# =========================

client = MongoClient(
    "mongodb+srv://ajaynaidumathi99_db_user:VfvH1K5CvtSaNdYf@cluster0.yc9c2vm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

mongodb = client["cybershield"]

scans_collection = mongodb["scans"]

print("MongoDB Connected Successfully!")

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

    # URL TABLE

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scanned_urls (
        id INT AUTO_INCREMENT PRIMARY KEY,
        url TEXT NOT NULL,
        score INT NOT NULL,
        classification VARCHAR(50) NOT NULL,
        scan_time DATETIME NOT NULL
    )
    """)

    # QR TABLE

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS qr_scans (
        id INT AUTO_INCREMENT PRIMARY KEY,
        qr_data TEXT NOT NULL,
        result VARCHAR(50) NOT NULL,
        scan_time DATETIME NOT NULL
    )
    """)

    # SPAM TABLE

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spam_messages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        message TEXT NOT NULL,
        result VARCHAR(50) NOT NULL,
        scan_time DATETIME NOT NULL
    )
    """)

    db.commit()

    print("All Tables Ready!")

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

    # SAVE IN MYSQL

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

            print(f"MySQL Insert Failed: {err}")

    # SAVE IN MONGODB

    try:

        scans_collection.insert_one({
            "type": "URL Scan",
            "url": url,
            "score": result['score'],
            "classification": result['classification'],
            "reasons": result['reasons'],
            "time": datetime.now()
        })

    except Exception as e:

        print(f"MongoDB Insert Failed: {e}")

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

    # SAVE IN MYSQL

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

            print(f"MySQL Insert Failed: {err}")

    # SAVE IN MONGODB

    try:

        scans_collection.insert_one({
            "type": "QR Scan",
            "qr_data": result.get('qr_data'),
            "classification": result.get('classification'),
            "score": result.get('score'),
            "reasons": result.get('reasons'),
            "time": datetime.now()
        })

    except Exception as e:

        print(f"MongoDB Insert Failed: {e}")

    return jsonify(result)

# =========================
# SPAM MESSAGE ROUTE
# =========================

@app.route('/scan-message', methods=['POST'])
def scan_message():

    data = request.json

    message = data.get('message')

    result = analyze_message(message)

    # SAVE IN MYSQL

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

            print(f"MySQL Insert Failed: {err}")

    # SAVE IN MONGODB

    try:

        scans_collection.insert_one({
            "type": "Spam Message",
            "message": message,
            "classification": result['classification'],
            "score": result['score'],
            "reasons": result['reasons'],
            "time": datetime.now()
        })

    except Exception as e:

        print(f"MongoDB Insert Failed: {e}")

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