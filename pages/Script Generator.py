import os 
from apikey import apikey

import streamlit as st
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

# Prompt templates
persona_template = PromptTemplate(
    input_variables=['persona_description'], 
    template='You are a video script text generator. I need you to create a text script for video that will be read for a training video. It is about Salesforce software. I will give you just the bullet points of the topics and I need you to create a text that will be read by someone, while the video runs, in the video the topics are shown. These are the bullet points: {persona_description}. Always start with an introduction and end with an outro.'
)

# Memory 
memory = ConversationBufferMemory(input_key='persona_description', memory_key='chat_history')

# Llms
llm = OpenAI(temperature=0.9, max_tokens=1024) 
persona_chain = LLMChain(llm=llm, prompt=persona_template, verbose=True, output_key='persona', memory=memory)

# Show stuff on the screen if there's a prompt
if st.button('Generate Script'):
    if persona_description: 
        persona = persona_chain.run(persona_description=persona_description)
        st.write(persona) 
        with st.expander('Persona History'): 
            st.info(memory.buffer)
