import streamlit as st
from streamlit_emoji import Emoji
from pages import InterviewQuestions, PersonaCreator, JourneyBuilder

PAGES = {
    "Create Interview Questions": InterviewQuestions,
    "Create a Persona": PersonaCreator,
    "Create a Journey Map": JourneyBuilder
}

st.title('Welcome to the UX Research GPT App!')

col1, col2, col3 = st.beta_columns(3)

with col1:
    st.header("Create Interview Questions")
    st.write("Maximize your user interview sessions by providing relevant information and receiving tailored interview questions.")
    st.write("Description of the app goes here.")

with col2:
    st.header("Create a Persona")
    st.write("Enter information and receive a detailed description of the persona.")
    st.write("Description of the app goes here.")

with col3:
    st.header("Create a Journey Map")
    st.write("Based on a created persona, you can generate a journey map.")
    st.write("Description of the app goes here.")
