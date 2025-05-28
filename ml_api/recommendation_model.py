# ml_api/recommendation_model.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Sample dataset
data = {
    'background': ['Computer Science', 'Civil Engineering', 'Electronics'],
    'goal': ['Python Developer', 'Web Developer', 'Data Scientist'],
    'experience': ['Beginner', 'Intermediate', 'Advanced'],
    'learning_path': [
        'Python Basics (4 weeks), Intermediate Python (6 weeks), Django (8 weeks)',
        'HTML/CSS (4 weeks), JavaScript (6 weeks), React (8 weeks)',
        'Python (6 weeks), Machine Learning (10 weeks), Deep Learning (12 weeks)'
    ]
}
df = pd.DataFrame(data)

# Vectorize features
df['combined'] = df['background'] + ' ' + df['goal'] + ' ' + df['experience']
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['combined'])

def recommend_learning_path(user_background, user_goal, user_experience):
    user_input = f"{user_background} {user_goal} {user_experience}"
    user_vec = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vec, X)
    best_match_idx = np.argmax(similarities)
    return df['learning_path'].iloc[best_match_idx]