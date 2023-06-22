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
role = st.text_input('Enter the persona`s role', placeholder='e.g. Manager')
industry = st.text_input('Enter the industry the persona is working in (optional)', placeholder='e.g. Automotive')
socio = st.text_input('Describe the learner`s background and previous experience with the product to be trained (optional)', placeholder='e.g., Digital native, has 4 years of experience with Sales Cloud, uses Account and Opportunity Management on a daily basis')
additional = st.text_input('Additional information regarding your script (optional)', placeholder='e.g., formal language, very short sentences')

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
    input_variables=['role', 'industry', 'additional', 'keywords', 'socio'], 
    template='Act as a professional HCC Consultant/ Enablement architect / trainer who needs to write a extensive script text for a training video / short tutorial for Salesforce products, directly addressing the end users with the role of {role} in the following industry: {industry}. Keep in mind the learner`s background {socio} and additional information on the language, tone, length etc. {additional}. Include explanations for the following topics: {keywords}. Please start with a general introduction about what is happening and end with an outro text. Remember this script needs to be extensive.'
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
    if role: 
        persona = persona_chain.run(role=role, industry=industry, additional=additional, keywords=keywords, socio=socio)
        st.write(persona) 
        with st.expander('Persona History'): 
            st.info(memory.buffer)
