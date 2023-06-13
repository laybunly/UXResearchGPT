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
st.title('Persona Creator')

# Create the input fields with placeholders
role = st.text_input('Enter the persona`s role', placeholder='e.g. Manager')
industry = st.text_input('Enter the industry the persona is working in', placeholder='e.g. Automotive')
socio = st.text_input('Describe the socio-cultural aspects of your persona', placeholder='e.g. 43 years old, single, from Germany, based in Japan')
additional = st.text_input('Additional information (optional)', placeholder='Additional information')

keywords = st_tags(
    label='# What should be included in the persona description?',
    text='Press enter to add more',
    value=['Quotes', 'Character Traits', 'Pain Points', 'Goals', 'Daily Tasks'],
    suggestions=['Quotes', 'Character Traits', 'Pain Points', 'Goals', 'Daily Tasks'],
    maxtags=10,
    key='1',
)

# Prompt templates
persona_template = PromptTemplate(
    input_variables=['role', 'industry', 'additional', 'keywords', 'socio'], 
    template='Act as a professional UX Designer. Create a Persona with a name for User-Centered Development about a persona working in the following industry: {industry}, with the role of {role}. Also include the following {additional} and {socio} Include paragraphs for the following attributes: {keywords}. Start each paragraph with a header named after the mentioned attributes and a : and then start in a new line. Use the name when describing the persona and also name it at the beginning of the text.'
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
if st.button('Generate Persona'):
    if role and industry and additional: 
        persona = persona_chain.run(role=role, industry=industry, additional=additional, keywords=keywords, socio=socio)
        st.write(persona) 
        with st.expander('Persona History'): 
            st.info(memory.buffer)
