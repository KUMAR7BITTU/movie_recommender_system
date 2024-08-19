import streamlit as st 
import pickle
import pandas as pd
import requests

# Fetch poster function with error handling for NoneType
def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=a74f93cd8576c77fa22df739d37251b8'.format(movie_id)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:  # Ensure poster_path is not None
                return "https://image.tmdb.org/t/p/w500/" + poster_path
            else:
                return "default_image.jpg"  # Provide a default image path if poster_path is None
        else:
            return "default_image.jpg"  # Handle the case where API response is not OK
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return "default_image.jpg"  # Handle any connection or request errors

# Recommendation function with posters
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from API or return default
        recommended_movies_posters.append(fetch_poster(movie_id))
        
    return recommended_movies, recommended_movies_posters

# Load data from pickle files
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app title
st.title('Movie Recommender System')

# Movie selection dropdown
selected_movie_name = st.selectbox('Select a movie', movies['title'].values)

# Recommend button
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    
    # Display recommended movies and posters in columns
    cols = st.columns(5)  # Create 5 columns for display
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i], use_column_width=True)  # Display images with column width

