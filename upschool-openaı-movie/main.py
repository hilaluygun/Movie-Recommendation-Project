
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Streamlit app
st.title("Enhanced Movie  Recommendation System")

# User input form
st.header("Movie Recommendation")

movie_genre = st.selectbox(
    "Movie Recommendation",
    ["Action", "Comedy", "Drama", "Science Fiction", "Horror ", ]
)
favourite_movies = st.text_area("Your favourite movies (comma-separated)")
age = st.number_input("Please enter your age", min_value=0, max_value=120, value=30)
country = st.text_input("Your country")







# Color selection


# Initialize messages in session state if not present
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system",
         "content": "As a movie recommendation assistant you have knowledge of global films and making movie suggestions. Provide movie recommendations based on the requester preferences. Format your response as a markdown table with 3  movie recommendations. The table should have 3 columns: 'Movie Title','Genre' and 'Summary'. Keep the descriptions short but informative."}
    ]


if st.button("Get Movie Recommendations"):
# Prepare the user message
    user_message = f"""
        Please suggest movie recommendations for a {age}-year-old  who enjoys {movie_genre} films, particularly those similar to {favourite_movies}.
        The preferred type of movie is {movie_genre}.
        Consider the cultural background and film preferences of  requester  in your recommendations.
        Present your recommendations in a markdown table format with five  columns: 'Movie Title', 'Genre', 'Why It's a Good Fit', 'Summary', and 'Where to Watch'.
        In the 'Where to Watch' column, suggest 1-2 popular streaming platforms or movie theaters in {country} where the film can be watched.
        Ensure that at least some of the movie recommendations align with the preferred genre and type when appropriate.
        Provide 3-5 movie recommendations. You have knowledge of global films and making movie recommendations.
        """




    st.session_state.messages.append({"role": "user", "content": user_message})

    try:
        # Generate recommendations using OpenAI
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
        )

        recommendations = completion.choices[0].message.content

        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": recommendations})

        # Display recommendations
        st.header(" Best Movie  Recommendations")
        st.markdown(recommendations)

        # Save recommendations to file
        with open('movie_recommendations.md', 'w') as f:
            f.write(recommendations)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Display saved recommendations
st.header("Previous Recommendations")
try:
    with open('movie_recommendations.md', 'r') as f:
        st.markdown(f.read())
except FileNotFoundError:
    st.write("No previous recommendations found.")




