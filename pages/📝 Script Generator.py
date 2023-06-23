import os 
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

# App framework
st.title('📝  Script Generator')

with st.sidebar:
    st.markdown("""
    This script generator is a tool that helps you create training video scripts. All you need to do is input the key points or topics that you want to include in your training video. These can be entered in a simple bullet point format. Once you've input the topics, the tool takes over.<br><br>
    It uses the power of artificial intelligence to transform these bullet points into a full script that can be used for your training video. It writes out everything that the narrator would need to say to cover all the points you've entered.<br><br>
    So, you can think of this as an AI assistant that helps you write scripts for your training videos. It's designed to make the script writing process quicker and easier, allowing you to focus on the other aspects of creating your training content.
    """, unsafe_allow_html=True)

# Create the input fields with placeholders 
persona_description = st.text_area('What is the content of your video?', placeholder="Step 1: Global Opportunity page Layout, Step 1.1: Account Information: = is linked to the Legal Entity account including 1.1) Territory", height=200)

# Prompt templates
persona_template = PromptTemplate(
    input_variables=['persona_description'], 
    template='You are a video script text generator. I need you to create a detailed and lengthy text script for video that will be read for a training video. It is about Salesforce software. I will give you just the bullet points of the topics and I need you to create a text that will be read by someone, while the video runs, in the video the topics are shown. These are the bullet points: {persona_description}. Always start with an introduction and end with an outro.'
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
        with st.expander('Script History'): 
            st.info(memory.buffer)
