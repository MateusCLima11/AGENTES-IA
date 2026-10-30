import os
import streamlit as st 
from crewai import Agent, Task, Crew, Process, LLM

# Configuração da página
st.header("🦾🤖 Agentes para Estudo")
st.write("Informe o tema e gere material para estudar:")

tema = st.text_input("Tema de estudo:", placeholder="Ex.: Algoritmos")
objetivo = st.text_input("Objetivo:", placeholder="Ex.: Entender conceitos básicos")

executar = st.button("Gerar Material")
api_key = "SUA_CHAVE_API_AQUI"  # Insira sua chave da Groq aqui

if executar:
    if not tema or not objetivo:
        st.warning("Por favor, preencha o tema e o objetivo antes de prosseguir.")
    else:
        with st.spinner("Gerando material de estudo..."):
            # Configuração do LLM
            llm = LLM(
                model="groq/llama-3.3-70b-versatile",
                api_key=api_key,
                temperature=0.3
            )

            # Agentes
            agente_resumo = Agent(
                role="Redator de resumo didático",
                goal="Escrever RESUMO claro e didático sobre {tema} alinhado com o objetivo: {objetivo}. A linguagem deve ser didática, direta e com contexto prático e sem jargões.",
                backstory="Você transforma temas técnicos/acadêmicos em explicações curtas e precisas.",
                llm=llm,
                verbose=False 
            )

            agente_exemplos = Agent(
                role="Criador de exemplos contextualizados",
                goal="Gerar 5 EXEMPLOS CURTOS sobre {tema}, cada um com contexto realista. Cada exemplo com um título (em negrito), cenário, dados (se houver), aplicação e resultado.",
                backstory="Você mostra o conceito em ação com exemplos breves e concretos.",
                llm=llm,
                verbose=False
            )

            agente_exercicios = Agent(
                role="Criador de exercícios práticos",
                goal="Criar 4 EXERCÍCIOS SIMPLES sobre {tema}. Variar formato (múltipla escolha, V/F, completar, resolução curta). Enunciados claros. NÃO incluir respostas.",
                backstory="Você cria atividades rápidas que fixam os conceitos essenciais.",
                llm=llm,
                verbose=False
            )

            agente_gabarito = Agent(
                role="Revisor e Gabaritador",
                goal="Produzir o GABARITO oficial para os exercícios sobre {tema}, com respostas corretas e justificativa breve (1-3 frases) por item.",
                backstory="Você confere consistência e explica rapidamente o porquê da resposta.",
                llm=llm,
                verbose=False
            )

            # Tarefas (Tasks)
            task_resumo = Task(
                description="Escreva um resumo didático sobre {tema} focado em {objetivo}.",
                expected_output="Um resumo didático e estruturado em Markdown.",
                agent=agente_resumo
            )

            task_exemplos = Task(
                description="Crie 5 exemplos práticos e realistas aplicados ao tema {tema}.",
                expected_output="5 exemplos práticos formatados em Markdown.",
                agent=agente_exemplos
            )

            task_exercicios = Task(
                description="Crie 4 exercícios práticos sobre {tema} sem o gabarito.",
                expected_output="4 exercícios em formatos variados em Markdown.",
                agent=agente_exercicios
            )

            task_gabarito = Task(
                description="Crie o gabarito com explicações breves para as questões criadas sobre {tema}.",
                expected_output="Gabarito detalhado e justificativa em Markdown.",
                agent=agente_gabarito
            )

            # Equipe e Execução (Crew)
            equipe = Crew(
                agents=[agente_resumo, agente_exemplos, agente_exercicios, agente_gabarito],
                tasks=[task_resumo, task_exemplos, task_exercicios, task_gabarito],
                process=Process.sequential
            )

            resultado = equipe.kickoff(inputs={"tema": tema, "objetivo": objetivo})

            # Exibição do Resultado
            st.markdown("---")
            st.markdown("### 📚 Material de Estudo Gerado")
            st.markdown(resultado)
