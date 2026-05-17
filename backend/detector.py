import pickle
from urllib.parse import urlparse

# LOAD AI MODEL
with open('url_ai_model.pkl', 'rb') as f:
    model = pickle.load(f)

def analyze_url(url):

    reasons = []

    # -----------------------------
    # RULE-BASED ANALYSIS
    # -----------------------------

    rule_score = 0

    suspicious_keywords = [
        'login',
        'verify',
        'bank',
        'secure',
        'update',
        'free',
        'bonus'
    ]

    for word in suspicious_keywords:

        if word in url.lower():

            rule_score += 10

            reasons.append(
                f'Suspicious keyword detected: {word}'
            )

    # LONG URL
    if len(url) > 75:

        rule_score += 20

        reasons.append('Very long URL detected')

    # @ SYMBOL
    if '@' in url:

        rule_score += 25

        reasons.append('@ symbol detected')

    # HYPHENATED DOMAIN
    if '-' in urlparse(url).netloc:

        rule_score += 15

        reasons.append('Hyphenated domain detected')

    # -----------------------------
    # AI FEATURE EXTRACTION
    # -----------------------------

    features = [[

        len(url),

        1 if url.startswith('https') else 0,

        1 if '@' in url else 0,

        1 if '-' in urlparse(url).netloc else 0
    ]]

    # -----------------------------
    # AI PREDICTION
    # -----------------------------

    prediction = model.predict(features)[0]

    probability = model.predict_proba(features)[0]

    ai_score = round(max(probability) * 100, 2)

    reasons.append(
        'AI phishing analysis completed'
    )

    # -----------------------------
    # DOMAIN SAFETY LOGIC
    # -----------------------------

    domain = urlparse(url).netloc.replace('www.', '')

    trusted_extensions = [
        '.com',
        '.org',
        '.edu',
        '.gov',
        '.in'
    ]

    suspicious_tlds = [
        '.xyz',
        '.tk',
        '.top',
        '.buzz',
        '.monster'
    ]

    trusted_domains = [

        'google.com',
        'amazon.in',
        'amazon.com',
        'github.com',
        'microsoft.com',
        'youtube.com',
        'facebook.com',
        'instagram.com',
        'linkedin.com'
    ]

    # SAFE DOMAIN CONDITIONS
    if (

        domain in trusted_domains

        or

        (

            any(domain.endswith(ext) for ext in trusted_extensions)

            and

            rule_score < 20

            and

            not any(domain.endswith(ext) for ext in suspicious_tlds)

        )

    ):

        final_score = 0

        reasons.append(
            'Trusted domain detected'
        )

    else:

        final_score = (rule_score + ai_score) / 2

    # -----------------------------
    # FINAL CLASSIFICATION
    # -----------------------------

    if final_score >= 55:

        classification = 'PHISHING'

    elif final_score >= 30:

        classification = 'SUSPICIOUS'

    else:

        classification = 'SAFE'

    # -----------------------------
    # RETURN RESULT
    # -----------------------------

    return {

        'classification': classification,

        'score': round(final_score, 2),

        'rule_score': rule_score,

        'ai_score': ai_score,

        'reasons': reasons
    }