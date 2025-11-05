import os
import streamlit as st 
from crewai import Agent, Task, Crew, Process, LLM

# AGENTES PARA ESTUDO.
st.header("Agentes para Estudo")
st.write("Informe o tema e gere material para estudar:")

tema = st.text_input("Tema de estudo: ",placeholder="Ex.: Algoritimos")
objetivo = st.text_input("Objetivo: ", placeholder="Ex.:Entender conceitos")

executar = st.button("Gerar Material")
api_key = 'CHAVE_API'

if executar: 
    llm = LLM(
        model="groq/llama-3.3 -70b-versatitle",
        api_key=api_key,
        temperature=0.3
        # Temperature: define nivel de criatividade.
        # menor ou igual a 0.3 mais deterministico
        # entre 0.4 e 0.7 equilibrado para explicaçao
        # maior que 0.7 mais criativo porem menos previsivel
    )