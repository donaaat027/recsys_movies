import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import load_npz
import joblib
from PIL import Image
import requests
from io import BytesIO

def load_resources():
    df = pd.read_csv('movie_data.csv')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
    tfidf_matrix = load_npz('tfidf_matrix.npz')
    return df, vectorizer, tfidf_matrix

def get_recommendations(df, vectorizer, tfidf_matrix, user_input, top_n=10):
    user_input = user_input.strip().lower()
    try:
        idx = df[df['clean_title'].str.lower() == user_input].index[0]
        sim_scores = cosine_similarity(tfidf_matrix[idx], tfidf_matrix)
    except:
        input_vector = vectorizer.transform([user_input])
        sim_scores = cosine_similarity(input_vector, tfidf_matrix)
    
    sim_scores = sim_scores.flatten()
    top_indices = np.argsort(sim_scores)[::-1][:top_n]
    return df.iloc[top_indices]

def get_poster(url):
    try:
        response = requests.get(f"https://image.tmdb.org/t/p/w500{url}", timeout=10)
        return Image.open(BytesIO(response.content))
    except Exception as e:
        return Image.new('RGB', (200, 300), color='grey')