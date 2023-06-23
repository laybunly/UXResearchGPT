import os 
from apikey import apikey

import streamlit as st
from streamlit_tags import st_tags
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

# App framework
st.title('👤 Script Generator')

# Include text in the sidebar
with st.sidebar:
    st.write("Explanation Script Generator")


# Create the input fields with placeholders
persona_description = st.text_area('What is the content of your video?', placeholder="Step 1: Global Opportunity page Layout, Step 1.1: Account Information: = is linked to the Legal Entity account including 1.1) Territory", height=200)
#role = st.text_input('Enter the persona`s role', placeholder='e.g. Manager')
#industry = st.text_input('Enter the industry the persona is working in (optional)', placeholder='e.g. Automotive')
#socio = st.text_input('Describe the learner`s background and previous experience with the product to be trained (optional)', placeholder='e.g., Digital native, has 4 years of experience with Sales Cloud, uses Account and Opportunity Management on a daily basis')
#additional = st.text_input('Additional information regarding your script (optional)', placeholder='e.g., formal language, very short sentences')

keywords = st_tags(
    label='# What needs to be included in the script?',
    text='Press enter to add more',
    value=['Intoduction', 'Outro', 'Learning Goals', 'Important Highlights'],
    suggestions=['Intoduction', 'Outro', 'Learning Goals', 'Important Highlights'],
    maxtags=10,
    key='1',
)

# Prompt templates
persona_template = PromptTemplate(
    input_variables=['persona_description'], 
    template='You are a video script text generator. I need you to create a text script for video that will be read for a training video. It is about Salesforce software. I will give you just the bullet points of the topics and I need you to create a text that will be read by someone, while the video runs, in the video the topics are shown. These are the bullet points: {persona_description}. Always start with an introduction and end with an outro.'
)

journey_template = PromptTemplate(
    input_variables=['persona'], 
    template='write me a Journey Map, based on the Persona: {persona}.'
)

# Memory 
memory = ConversationBufferMemory(input_key='role', memory_key='chat_history')

# Llms
llm = OpenAI(temperature=0.9) 
persona_chain = LLMChain(llm=llm, prompt=persona_template, verbose=True, output_key='persona', memory=memory)
journey_chain = LLMChain(llm=llm, prompt=journey_template, verbose=True, output_key='journey', memory=memory)

# Show stuff on the screen if there's a prompt
if st.button('Generate Script'):
    if persona_description: 
        persona = persona_chain.run(persona_description=persona_description)
        st.write(persona) 
        with st.expander('Persona History'): 
            st.info(memory.buffer)
