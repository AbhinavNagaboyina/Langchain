import streamlit as st
import langchainhelper as lch

st.title("Code Generator UI")

# Text input for code
code_input = st.text_area("Enter your prompt here:")

# Dropdown for selecting the programming language
programming_languages = ["Python","Java","C++"]
selected_language = st.selectbox("Select a programming language:", programming_languages)

if selected_language == "Python":
    language= "python"
if selected_language == "Java":
    language= "java"
if selected_language == "C++":
    language= "c++"

if st.button("Generate Code"):
    if code_input:
        response = lch.code_generator(code_input,language)
        st.text(response["code"])