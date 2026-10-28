import os
import streamlit as st 
from crewai import Agent, Task, Crew, Process, LLM

# AGENTES PARA ESTUDO.
st.header("🦾🤖Agentes para Estudo")
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



    # Agentes
    agente_resumo = Agent(
        role="Redator de resumo didático.",
        goal=(
            "Escrever RESUMO claro e didático sobre {tema} alinhado com o {objativo}."
            "A linguagem deve ser didática, direta e com contexto prático e sem jargões."
        ),
    backstory="Você transforma temas técnicos/acadêmicos em explicações curtas e precisas.",
    llm=llm, verbose=False 
    )

agente_exemplos = Agent(
        role="Criador de exemplos contextualizados.",
        goal=(
            "Gera 5 EXEMPLOS CURTOS sobre {tema}, cada um com contexto realista."
            "Cada exemplo com um título (em negrito), cenário, dados (se houver), aplicação e resultado."
    ),
    backstory="Você mostra o conceito em ação com exemplos breves e concretos.",
    llm=llm, verbose=False
)

agente_exercicios = Agent(
        role="Criador de exerícios  práticos.",
        goal=(
            "Criar 4 EXERCÍCIOS SIMPLES sobre {tema}"
            "Variar formato (múltipla escolha, V/F, completar, relosução curta)"
            "Enunciados claros. NÃO incluir respostas." 
    ),
    backstory="Você cria atividades rápidas que fixam os conceitos essenciais.",
    llm=llm, verbose=False
)

agente_gabarito = Agent(
        role="Revisor e Gabaritador.",
        goal=(
            "Ler os EXERCÍCIOS sobre {tema} e produzir o GABAARITO oficial,"
            "com respostas corretas e justificativa breve (1-3) por item.",
    ),
    backstory="Você confere consistência e explica rapidamente o porquê da resposta.",
    llm=llm, verbose=False
)
