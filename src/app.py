import json
from pathlib import Path

import pandas as pd
import requests
import streamlit as st


# ============ CONFIGURAÇÃO ============

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


# ============ CARREGAR DADOS ============

def carregar_json(nome_arquivo: str) -> dict:
    with open(DATA_DIR / nome_arquivo, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


perfil = carregar_json("perfil_usuario.json")
base_conhecimento = carregar_json("base_conhecimento_treino.json")
exercicios = pd.read_csv(DATA_DIR / "exercicios.csv")
historico = pd.read_csv(DATA_DIR / "historico_atendimento.csv")


# ============ MONTAR CONTEXTO ============

contexto = f"""
PERFIL DO USUÁRIO:
{json.dumps(perfil, indent=2, ensure_ascii=False)}

BASE DE CONHECIMENTO SOBRE TREINOS:
{json.dumps(base_conhecimento, indent=2, ensure_ascii=False)}

EXERCÍCIOS DISPONÍVEIS:
{exercicios.to_string(index=False)}

HISTÓRICO DE ATENDIMENTO:
{historico.to_string(index=False)}
"""


# ============ SYSTEM PROMPT ============

SYSTEM_PROMPT = """
Você é o FitGuia IA, um assistente virtual de orientação inicial de treinos.

OBJETIVO:
Ajudar a pessoa usuária a organizar treinos simples, seguros e coerentes para casa ou academia, usando a base de conhecimento fornecida.

REGRAS:
- Use apenas as informações presentes no contexto.
- Não invente exercícios, cargas, diagnósticos ou promessas de resultado.
- Não substitua médico, fisioterapeuta ou profissional de Educação Física.
- Não crie dietas.
- Não incentive treino extremo ou treino com dor intensa.
- Se o usuário relatar dor forte, lesão recente, tontura, dor no peito ou falta de ar anormal, não monte treino.
- Quando faltarem informações importantes, faça perguntas objetivas.
- Explique de forma simples e direta.
- Responda em no máximo 4 parágrafos.
- Sempre entregue um próximo passo prático.
- Se a pergunta fugir do tema de treinos, explique seu papel e redirecione.
"""


# ============ CHAMAR OLLAMA ============

def perguntar(mensagem: str) -> str:
    prompt = f"""
{SYSTEM_PROMPT}

CONTEXTO:
{contexto}

PERGUNTA DO USUÁRIO:
{mensagem}
"""

    try:
        resposta = requests.post(
            OLLAMA_URL,
            json={
                "model": MODELO,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        resposta.raise_for_status()
        dados = resposta.json()
        return dados.get("response", "Não consegui gerar uma resposta no momento.")
    except requests.exceptions.ConnectionError:
        return (
            "Não consegui conectar ao Ollama em http://localhost:11434. "
            "Verifique se o Ollama está instalado e se o comando `ollama serve` está em execução."
        )
    except requests.exceptions.Timeout:
        return "A resposta demorou demais. Tente novamente com uma pergunta mais curta."
    except requests.exceptions.RequestException as erro:
        return f"Ocorreu um erro ao chamar o Ollama: {erro}"
    except KeyError:
        return "A resposta do Ollama veio em um formato inesperado."


# ============ INTERFACE STREAMLIT ============

st.set_page_config(
    page_title="FitGuia IA",
    page_icon="🏋️",
    layout="centered"
)

st.title("FitGuia IA")
st.caption("Assistente virtual local para treinos em casa e na academia")

with st.sidebar:
    st.header("Sobre o agente")
    st.write(
        "O FitGuia IA usa uma LLM local via Ollama e uma base de conhecimento "
        "em JSON/CSV para responder dúvidas sobre treinos."
    )
    st.write("**Modelo:** gpt-oss")
    st.write("**Interface:** Streamlit")
    st.write("**Execução:** localhost")
    st.divider()
    st.write("Exemplos de perguntas:")
    st.markdown("- Quero treinar em casa, sou iniciante e tenho 20 minutos.")
    st.markdown("- Treino na academia e quero ganhar força.")
    st.markdown("- Estou com dor forte no joelho. Posso treinar perna?")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {
            "role": "assistant",
            "content": (
                "Olá. Sou o FitGuia IA. Posso ajudar com orientações gerais sobre "
                "treinos em casa ou na academia. Conte seu objetivo, nível e onde pretende treinar."
            )
        }
    ]

for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["role"]):
        st.write(mensagem["content"])

if pergunta_usuario := st.chat_input("Digite sua dúvida sobre treinos..."):
    st.session_state.mensagens.append({"role": "user", "content": pergunta_usuario})

    with st.chat_message("user"):
        st.write(pergunta_usuario)

    with st.chat_message("assistant"):
        with st.spinner("Analisando sua pergunta..."):
            resposta = perguntar(pergunta_usuario)
            st.write(resposta)

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
