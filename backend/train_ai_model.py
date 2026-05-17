import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# PROFESSIONAL TRAINING DATA
data = {

    'message': [

        # SPAM
        'Win cash prize now',
        'Click this link urgently',
        'Your bank account is blocked',
        'Congratulations you won lottery',
        'Claim your free reward',
        'Urgent verify your account now',
        'You received free cashback',
        'Your OTP is 456789',
        'Limited time loan offer',
        'Update your bank password',

        # SAFE
        'Hello how are you',
        'Let us meet tomorrow',
        'Project submission completed',
        'Lunch at 1 PM',
        'Good morning friend',
        'Meeting scheduled today',
        'Assignment completed',
        'Call me later',
        'Happy birthday',
        'See you tomorrow'
    ],

    'label': [

        'spam',
        'spam',
        'spam',
        'spam',
        'spam',
        'spam',
        'spam',
        'spam',
        'spam',
        'spam',

        'safe',
        'safe',
        'safe',
        'safe',
        'safe',
        'safe',
        'safe',
        'safe',
        'safe',
        'safe'
    ]
}

# CREATE DATAFRAME
df = pd.DataFrame(data)

# PROFESSIONAL NLP + AI PIPELINE
model = Pipeline([

    ('tfidf', TfidfVectorizer()),

    ('classifier', LogisticRegression())
])

# TRAIN MODEL
model.fit(df['message'], df['label'])

# SAVE MODEL
with open('ai_spam_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("PRO AI MODEL TRAINED SUCCESSFULLY")