import os 
from apikey import apikey

import streamlit as st
from streamlit_tags import st_tags
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

os.environ['OPENAI_API_KEY'] = apikey

# App framework
st.title('User Journey Map Creator')
default_value = " "
persona_description = st.text_area('Who is your Persona?', placeholder="Tom is a project manager at a tech company in Silicon Valley, striving for efficiency and timely delivery within budget constraints. His main pain points are unexpected last-minute changes and scope creep, which cause delays and budget overruns.", height=200)
# Optional attributes
with st.expander('Detailed Persona Description (optional)'):
    pain_points = st.text_input('Pain Points', placeholder=default_value)
    goals = st.text_input('Goals', placeholder=default_value)
    character_traits = st.text_input('Character Traits', placeholder=default_value)
    daily_tasks = st.text_input('Daily Tasks', placeholder=default_value)
    quotes = st.text_input('Quotes', placeholder=default_value)

additional_info = st.text_input('Additional Information', placeholder="e.g. 43 years old, single, from Germany, based in Japan")

stages = st_tags(
    label='# Which stages should be considered?',
    text='Press enter to add more',
    value=['Awareness', 'Consideration', 'Purchase', 'Delivery', 'Usage & Service', 'Retention & Loyalty'],
    suggestions=['Awareness', 'Consideration', 'Purchase', 'Delivery', 'Usage & Service', 'Retention & Loyalty'],
    maxtags = 6,
    key='1',
)


# Prompt templates
journey_template = PromptTemplate(
    input_variables = ['persona_description', 'additional_info', 'stages', 'pain_points', 'goals', 'character_traits', 'daily_tasks', 'quotes'], 
    template='Using the Persona description: {persona_description}, additional information: {additional_info}, and considering the following stages: {stages}. If provided, include Pain Points: {pain_points}, Goals: {goals}, Character Traits: {character_traits}, Daily Tasks: {daily_tasks}, and Quotes: {quotes}. Generate a User Journey Map.'
)

# Memory 
memory = ConversationBufferMemory(input_key='persona_description', memory_key='chat_history')

# Llms
llm = OpenAI(temperature=0.9) 
journey_chain = LLMChain(llm=llm, prompt=journey_template, verbose=True, output_key='journey', memory=memory)

# Show stuff on the screen if there's a prompt
if st.button('Generate User Journey Map'):
    if persona_description and additional_info: 
        journey = journey_chain.run(persona_description=persona_description, additional_info=additional_info, stages=stages, pain_points=pain_points, goals=goals, character_traits=character_traits, daily_tasks=daily_tasks, quotes=quotes)
        st.write(journey) 
        with st.expander('Journey History'): 
            st.info(memory.buffer)
