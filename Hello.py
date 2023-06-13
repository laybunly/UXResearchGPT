import streamlit as st

st.title('Welcome to the UX Research GPT App!')

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
    st.header('Create Interview Questions')
    st.write(apps['Create Interview Questions'])

with col2:
    st.header('Create a Persona')
    st.write(apps['Create a Persona'])

with col3:
    st.header('Create a Journey Map')
    st.write(apps['Create a Journey Map'])
