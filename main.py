from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load movie data
movies_data = pd.read_csv('movies.csv')

# Your existing code for the recommendation system
movies_data['vote_average'] = movies_data['vote_average'].map(str)
selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director', 'vote_average']
for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')
combined_features = movies_data['genres'] + ' ' + movies_data['keywords'] + ' ' + movies_data['tagline'] + ' ' + \
                 movies_data['cast'] + ' ' + movies_data['director'] + ' ' + movies_data['vote_average']
vectorized = TfidfVectorizer()
feature_vectors = vectorized.fit_transform(combined_features)
similarity = cosine_similarity(feature_vectors)
list_of_all_titles = movies_data['title'].tolist()

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []

    if request.method == 'POST':
        movie_name = request.form['movie_name']
        find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

        if find_close_match:
            close_match = find_close_match[0]
            index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
            similarity_score = list(enumerate(similarity[index_of_the_movie]))
            sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

            for movie in sorted_similar_movies[:10]:
                recommendations.append(movies_data[movies_data.index == movie[0]]['title'].values[0])

    return render_template('index.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
