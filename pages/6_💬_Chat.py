import streamlit as st
# from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper


st.title('🦜🔗 Quickstart App')

# Prompt template
title_template = PromptTemplate(
    input_variables = ['topic'],
    template = "Write me a YouTube video title about {topic}"
    # template = "Write me a motivational message about {topic}"
)

title_memory = ConversationBufferMemory(input_key="topic", memory_key="chat_history")

llm = OpenAI(temperature=0.7, max_tokens=200, openai_api_key="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", openai_organization="org-Yi64r1Foet4RS92sLWP419ru")
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key="title", memory=title_memory)

def generate_response(prompt):
  st.info(prompt, icon="ℹ️")
  res = title_chain.run(prompt)
  st.write(res)

with st.form('my_form'):
  text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
  submitted = st.form_submit_button('Submit')
  if submitted:
    generate_response(text)
#   if not openai_api_key.startswith('sk-'):
#     st.warning('Please enter your OpenAI API key!', icon='⚠')
#   if submitted and openai_api_key.startswith('sk-'):
#     generate_response(text)