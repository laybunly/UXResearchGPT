import streamlit as st
from pages import PersonaCreator, JourneyBuilder

st.title('Welcome to the UX Research GPT!')

# Define the apps and their descriptions
apps = {
    'Create Interview Questions': 'Maximize your user interview sessions by providing relevant information and receiving tailored interview questions.',
    'Create a Persona': 'Enter information and receive a detailed description of the persona.',
    'Create a Journey Map': 'Based on a created persona, you can generate a journey map.'
}

# Create three columns
col1, col2, col3 = st.columns(3)

# Render each app in a separate column
with col1:
    st.title('🗣️')
    st.subheader('Create Interview Questions')
    st.write(apps['Create Interview Questions'])

with col2:
    st.markdown(
        """
        <div style="text-align: center;">
            <h2>👤 Create a Persona</h2>
            <p>{}</p>
        </div>
        """.format(apps['Create a Persona']),
        unsafe_allow_html=True
    )

with col3:
    st.header('🛣️  Create a Journey Map')
    st.write("<br>", unsafe_allow_html=True)
    st.write(apps['Create a Journey Map'])
