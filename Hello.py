import streamlit as st
from pages import PersonaCreator, JourneyBuilder

PAGES = {
    "Start": PersonaCreator,
    "Page 2: Journey Map": JourneyBuilder
}

st.title('Welcome to the UX Research GPT App!')
st.write('''
    With this application, you can:
    - Create Interview Questions: Maximize your user interview sessions by providing relevant information and receiving tailored interview questions.
    - Create a Persona: Enter information and receive a detailed description of the persona.
    - Create a Journey Map: Based on a created persona, you can generate a journey map.

    To get started, simply select an app from the menu on the left side.
''')


