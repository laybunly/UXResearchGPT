import os
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

os.environ['OPENAI_API_KEY'] = apikey

# App framework
st.title('User Research Interview Questions Generator')

# User Profile (required field)
user_profile = st.text_input('User Profile', placeholder="e.g. College students using learning apps")

# Context of Usage (required field)
context = st.text_input('Context of Usage', placeholder="e.g. Primarily uses the app for studying biology")

# Research Objectives (optional field)
research_objectives = st.text_input('Research Objectives (optional)', placeholder="e.g. Understand main challenges faced while studying biology using the app")

# Product/Service Details (optional field)
product_details = st.text_input('Product/Service Details (optional)', placeholder="e.g. An interactive learning app with quizzes and flashcards")

# Past User Data/Insights (optional field)
past_user_data = st.text_input('Past User Data/Insights (optional)', placeholder="e.g. Users tend to spend more time on flashcards than quizzes")

# Additional information (optional field)
kpis = st.text_input('Key Performance Indicators (optional)', placeholder="")

# Prompt templates
interview_template = PromptTemplate(
    input_variables=['user_profile', 'context', 'research_objectives', 'product_details', 'past_user_data', 'kpis'],
    template='Based on the user profile: {user_profile}, context: {context}, research objectives: {research_objectives}, product details: {product_details}, past user data: {past_user_data}, and KPIs: {kpis}, generate a set of user research interview questions.'
)

# Memory
memory = ConversationBufferMemory(input_key='user_profile', memory_key='chat_history')

# Llms
llm = OpenAI(temperature=0.9)
interview_chain = LLMChain(llm=llm, prompt=interview_template, verbose=True, output_key='interview', memory=memory)

# Generate interview questions if required fields are filled
if st.button('Generate'):
    if user_profile and context:
        interview = interview_chain.run(
            user_profile=user_profile, 
            context=context, 
            research_objectives=research_objectives, 
            product_details=product_details, 
            past_user_data=past_user_data, 
            kpis=kpis
        )
        st.write(interview)
        with st.expander('Interview History'):
            st.info(memory.buffer)
    else:
        st.error("User Profile and Context of Usage are required fields.")
