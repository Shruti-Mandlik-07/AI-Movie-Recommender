import os
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

movies_path = os.path.join(BASE_DIR, 'model', 'movies.pkl')
similarity_path = os.path.join(BASE_DIR, 'model', 'similarity.pkl')

with open(movies_path, 'rb') as f:
    movies = pickle.load(f)

with open(similarity_path, 'rb') as f:
    similarity = pickle.load(f)