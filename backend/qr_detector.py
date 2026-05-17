import cv2
import re

suspicious_words = [
    'login',
    'verify',
    'bank',
    'free',
    'reward',
    'upi',
    'payment'
]

def analyze_qr(image_path):

    detector = cv2.QRCodeDetector()

    data, bbox, _ = detector.detectAndDecode(
        cv2.imread(image_path)
    )

    if not data:
        return {
            'classification': 'NO QR FOUND',
            'score': 0,
            'reasons': ['No QR code detected']
        }

    score = 0
    reasons = []

    if data.startswith('http://'):
        score += 30
        reasons.append('Unsafe HTTP link')

    for word in suspicious_words:

        if word in data.lower():

            score += 15

            reasons.append(
                f'Suspicious keyword detected: {word}'
            )

    if re.search(r'bit.ly|tinyurl', data):
        score += 25
        reasons.append('Shortened URL detected')

    if score >= 50:
        classification = 'SCAM QR'

    elif score >= 25:
        classification = 'SUSPICIOUS QR'

    else:
        classification = 'SAFE QR'

    return {
        'classification': classification,
        'score': score,
        'qr_data': data,
        'reasons': reasons
    }