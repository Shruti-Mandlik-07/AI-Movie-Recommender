import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv('data/movies.csv')

# handle missing values
movies['overview'] = movies['overview'].fillna('')

# create tags
movies['tags'] = movies['overview']

# vectorization
cv = CountVectorizer(max_features=1000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

# similarity
similarity = cosine_similarity(vectors)

# save
pickle.dump(movies, open('model/movies.pkl', 'wb'))
pickle.dump(similarity, open('model/similarity.pkl', 'wb'))
