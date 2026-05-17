import re
import pickle

# LOAD AI MODEL
with open('ai_spam_model.pkl', 'rb') as f:
    model = pickle.load(f)

# RULE-BASED KEYWORDS
spam_keywords = [
    'otp',
    'bank',
    'verify',
    'urgent',
    'click',
    'free',
    'reward',
    'upi',
    'winner',
    'account blocked',
    'password',
    'loan',
    'credit card',
    'congratulations',
    'claim',
    'money',
    'prize',
    'offer',
    'gift',
    'lottery',
    'cash'
]

def analyze_message(message):

    # RULE-BASED ANALYSIS
    rule_score = 0
    reasons = []

    message_lower = message.lower()

    for word in spam_keywords:

        if word in message_lower:

            rule_score += 10

            reasons.append(
                f'Suspicious keyword detected: {word}'
            )

    # URL DETECTION
    if re.search(r'http[s]?://', message):

        rule_score += 20

        reasons.append('Suspicious link detected')

    # OTP DETECTION
    if re.search(r'\d{6}', message):

        rule_score += 15

        reasons.append('OTP-like pattern detected')

    # AI NLP ANALYSIS
    prediction = model.predict([message])[0]

    probability = model.predict_proba([message])[0]

    ai_score = round(max(probability) * 100, 2)

    reasons.append(
        'AI NLP analysis completed'
    )

    # HYBRID FINAL SCORE
    final_score = (rule_score + ai_score) / 2

    # FINAL CLASSIFICATION
    if final_score >= 55:

        classification = 'SPAM / FRAUD'

    elif final_score >= 30:

        classification = 'SUSPICIOUS'

    else:

        classification = 'SAFE'

    return {

        'classification': classification,

        'score': round(final_score, 2),

        'rule_score': rule_score,

        'ai_score': ai_score,

        'reasons': reasons
    }