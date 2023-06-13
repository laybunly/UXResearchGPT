import streamlit as st
from pages import PersonaCreator, JourneyBuilder

PAGES = {
    "Start": PersonaCreator,
    "Page 2: Journey Map": JourneyBuilder
}

st.title('Welcome to the Persona Creator and Journey Map Application!')
st.write('''
    With this application, you can:
    - Create a Persona: Enter information and receive a detailed description of the persona.
    - Create a Journey Map: Based on a created persona, you can generate a journey map.
''')


