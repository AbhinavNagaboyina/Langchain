import os
import langchain
from langchain.callbacks import FileCallbackHandler
from loguru import logger
from constants import openai_key
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.callbacks import get_openai_callback
import streamlit as st
from langchain.memory import ConversationBufferWindowMemory

# OpenAI API secret key
os.environ["OPENAI_API_KEY"]= openai_key

def code_generator(code_text, language, sample_input):

    #LLM model
    llm= ChatOpenAI(temperature = 0)

    #chat prompt template
    chat_prompt1 = PromptTemplate(
        input_variables=["code_text", "language","sample_input"],
        template = "You are a helpful assistant that generates {code_text} code in {language} for this given {sample_input}."
        )  

    #log file creation
    logfile = "output.log"
    logger.add(logfile, colorize=True, enqueue=True)
    handler = FileCallbackHandler(logfile)
    
    chain1 = LLMChain(llm=llm, prompt=chat_prompt1, callbacks=[handler], verbose=True, output_key= "code")

    with get_openai_callback() as cb:
        response1 = chain1({"code_text": code_text, "language": language, "sample_input": sample_input})
        
        logger.info(response1)

        total_tokens = cb.total_tokens
        assert total_tokens > 0
        st.sidebar.write(f"Total Tokens: {cb.total_tokens}")
        st.sidebar.write(f"Prompt Tokens: {cb.prompt_tokens}")
        st.sidebar.write(f"Completion Tokens: {cb.completion_tokens}")
        st.sidebar.write(f"Total Cost (USD): ${cb.total_cost}")

        return response1

                
                
                