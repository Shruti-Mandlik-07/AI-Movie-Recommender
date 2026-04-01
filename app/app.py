from flask import Flask, render_template, request
import pickle
import requests

app = Flask(__name__)

# load model (FIXED PATH)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
movies_path = os.path.join(BASE_DIR, 'model', 'movies.pkl')

movies = pickle.load(open(movies_path, 'rb'))
similarity = pickle.load(open('../model/similarity.pkl', 'rb'))

# recommendation function
def fetch_poster(movie_id):
    try:
        # Using the standard educational API key for TMDB
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url).json()
        poster_path = data['poster_path']
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception as e:
        return None
    return None

def recommend(movie):
    movie = movie.lower()

    if movie not in movies['title'].str.lower().values:
        return []

    movie_index = movies[movies['title'].str.lower() == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        try:
            movie_id = movies.iloc[i[0]].movie_id
        except Exception:
            movie_id = ''
            
        poster = fetch_poster(movie_id) if movie_id else None
        recommended_movies.append({'title': title, 'id': movie_id, 'poster': poster})

    return recommended_movies

@app.route('/', methods=['GET', 'POST'])
def index():
    # Provide the full list of titles for the search autocomplete feature
    try:
        all_movies = movies['title'].values.tolist()
    except Exception:
        all_movies = []

    if request.method == 'POST':
        movie = request.form.get('movie', '').strip()

        results = recommend(movie)

        if len(results) == 0:
            return render_template('index.html', error=f"Movie '{movie}' not found! Please try selecting from the autocomplete list.", all_movies=all_movies)

        return render_template('index.html', results=results, searched_movie=movie, all_movies=all_movies)

    return render_template('index.html', all_movies=all_movies)


if __name__ == '__main__':
    app.run(debug=True)