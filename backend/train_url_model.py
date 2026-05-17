import pandas as pd
import pickle

from sklearn.ensemble import RandomForestClassifier

# TRAINING DATA
data = {

    'url_length': [

        12, 15, 18, 90, 120,
        150, 25, 35, 80, 110
    ],

    'has_https': [

        1, 1, 1, 0, 0,
        0, 1, 1, 0, 0
    ],

    'has_at_symbol': [

        0, 0, 0, 1, 1,
        1, 0, 0, 1, 1
    ],

    'has_hyphen': [

        0, 0, 0, 1, 1,
        1, 0, 0, 1, 1
    ],

    'phishing': [

        0, 0, 0, 1, 1,
        1, 0, 0, 1, 1
    ]
}

df = pd.DataFrame(data)

X = df.drop('phishing', axis=1)

y = df['phishing']

# RANDOM FOREST AI MODEL
model = RandomForestClassifier()

model.fit(X, y)

# SAVE MODEL
with open('url_ai_model.pkl', 'wb') as f:

    pickle.dump(model, f)

print('AI URL MODEL TRAINED SUCCESSFULLY')