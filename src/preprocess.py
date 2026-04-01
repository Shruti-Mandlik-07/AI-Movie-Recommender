import pandas as pd
import ast

# load data
movies = pd.read_csv('data/movies.csv')
credits = pd.read_csv('data/credits.csv')

# merge datasets
movies = movies.merge(credits, on='title')

# select useful columns
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

# drop nulls
movies.dropna(inplace=True)

# convert string to list
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

# take top 3 cast
def convert_cast(obj):
    L = []
    for i in ast.literal_eval(obj)[:3]:
        L.append(i['name'])
    return L

movies['cast'] = movies['cast'].apply(convert_cast)

# fetch director
def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

movies['crew'] = movies['crew'].apply(fetch_director)

# split overview into words
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# remove spaces
def collapse(L):
    return [i.replace(" ", "") for i in L]

movies['genres'] = movies['genres'].apply(collapse)
movies['keywords'] = movies['keywords'].apply(collapse)
movies['cast'] = movies['cast'].apply(collapse)
movies['crew'] = movies['crew'].apply(collapse)

# create tags
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# final dataframe
new_df = movies[['movie_id','title','tags']]

# convert list → string
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

print(new_df.head())