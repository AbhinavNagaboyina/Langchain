import os
import langchain
from langchain.callbacks import FileCallbackHandler
from loguru import logger
from constants import openai_key
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback
from pydantic import BaseModel
import guardrails as gd
from langchain.cache import InMemoryCache
from langchain.chains import SimpleSequentialChain


# OpenAI API secret key
os.environ["OPENAI_API_KEY"]= openai_key

st.title("Code Generator UI")

# Text input for code
code_input = st.text_area("Enter your prompt here:")

# Dropdown for selecting the programming language
programming_languages = ["Python","Java","C++"]
selected_language = st.selectbox("Select a programming language:", programming_languages)

sample_ip = st.text_area("Please enter the sample inputs")


langchain.llm_cache = InMemoryCache()


#chat prompt template

chat_prompt = PromptTemplate(
    input_variables=["text", "lang"],
    template = "You are a helpful assistant that generates {text} code in {lang}."
    )

#log file creation
logfile = "output.log"
logger.add(logfile, colorize=True, enqueue=True)
handler = FileCallbackHandler(logfile)

#LLM model

llm= ChatOpenAI(temperature = 0)
chain1 = LLMChain(llm=llm, prompt=chat_prompt, callbacks=[handler], verbose=True, output_key="code")

chat_prompt2 = PromptTemplate(
    input_variables=["input","generated_code"],
    template = "please pass the given sample input data {input} to the {generated_code}."
    )

chain2 = LLMChain(llm=llm, prompt= chat_prompt2, callbacks=[handler], verbose= True)


if st.button("Generate Code"):
    if code_input:
        with get_openai_callback() as cb:
            code= chain1({"text": code_input, "lang": selected_language})
            st.code(code,language= "python")
            logger.info(code)
            sample_op= chain2({"input": sample_ip, "generated_code": code})
            st.write(sample_op)
            total_tokens = cb.total_tokens
            assert total_tokens > 0
            st.write(f"Total Tokens: {cb.total_tokens}")
            st.write(f"Prompt Tokens: {cb.prompt_tokens}")
            st.write(f"Completion Tokens: {cb.completion_tokens}")
            st.write(f"Total Cost (USD): ${cb.total_cost}")
