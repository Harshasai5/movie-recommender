import streamlit as st
import pandas as pd
import difflib
import pickle
import gdown
import os

# Load the movie data
df = pickle.load(open('movies.pkl', 'rb'))

# Download similarity.pkl from Google Drive if not present
file_id = '1jogmLx8GNPMst0pTYQT5o8972XGBss99'
url = f'https://drive.google.com/uc?id={file_id}&export=download'
output = 'similarity.pkl'

if not os.path.exists(output):
    gdown.download(url, output, quiet=False)

# Load the similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.title("🎥 Movie Recommender System")
st.markdown("Enter your favorite movie and get 20 similar recommendations.")

# User input
movie_name = st.text_input("Enter your favorite movie:")

if st.button("Recommend"):
    if movie_name.strip() == "":
        st.warning("Please enter a movie name.")
    else:
        list_of_all_titles = df['title'].tolist()
        find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

        if not find_close_match:
            st.error("No close match found. Please try a different name.")
        else:
            close_match = find_close_match[0]
            index_of_the_movie = df[df.title == close_match]['index'].values[0]
            similarity_score = list(enumerate(similarity[index_of_the_movie]))
            sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

            st.subheader(f"Top 20 Movies Similar to: **{close_match}**")
            for i, movie in enumerate(sorted_similar_movies[1:21], start=1):
                index = movie[0]
                title_from_index = df[df.index == index]['title'].values[0]
                st.markdown(f"**{i}. {title_from_index}**")
