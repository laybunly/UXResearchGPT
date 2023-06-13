import streamlit as st

st.title('Welcome to the UX Research GPT!')

# Define the apps and their descriptions
apps = {
    'Create Interview Questions': 'Maximize your user interview sessions by providing relevant information and receiving tailored interview questions.',
    'Create a Persona': 'Enter information and receive a detailed description of the persona.',
    'Create a Journey Map': 'Based on a created persona, you can generate a journey map.',
    'Create a User Flow': 'Visualize and design user flows for your applications.'
}

# Create two columns
col1, col2 = st.columns(2)

# Render each app in a separate column
with col1:
    st.title('🗣️')
    st.subheader('Create Interview Questions')
    st.write(apps['Create Interview Questions'])

    st.title('🛣️')
    st.subheader('Create a Journey Map')
    st.write(apps['Create a Journey Map'])

with col2:
    st.title('👤')
    st.subheader('Create a Persona')
    st.write(apps['Create a Persona'])

    st.title('🌊')
    st.subheader('Create a User Flow')
    st.write(apps['Create a User Flow'])

st.write('To get started, simply select an app from the menu on the left side.')
