import streamlit as st
import os
import google.generativeai as genai
import datetime
from bson import ObjectId
from database import get_db_connection

def configure_gemini():
    """Configura a API do Gemini"""
    if "gemini_configured" not in st.session_state:
        gemini_api_key = os.getenv("GEM_API_KEY")
        if not gemini_api_key:
            st.error("GEMINI_API_KEY não encontrada nas variáveis de ambiente")
            st.stop()

        genai.configure(api_key=gemini_api_key)
        st.session_state.gemini_configured = True

def get_gemini_models():
    """Retorna os modelos Gemini configurados"""
    if "gemini_models" not in st.session_state:
        modelo_vision = genai.GenerativeModel("gemini-2.5-flash", generation_config={"temperature": 0.1})
        modelo_texto = genai.GenerativeModel("gemini-2.5-flash")
        st.session_state.gemini_models = (modelo_vision, modelo_texto)
    
    return st.session_state.gemini_models

def construir_contexto(agente, segmentos_selecionados, historico_mensagens=None):
    """Constrói o contexto com base nos segmentos selecionados"""
    contexto = ""
    
    if "system_prompt" in segmentos_selecionados and agente.get('system_prompt'):
        contexto += f"### INSTRUÇÕES DO SISTEMA ###\n{agente['system_prompt']}\n\n"
    
    if "base_conhecimento" in segmentos_selecionados and agente.get('base_conhecimento'):
        contexto += f"### BASE DE CONHECIMENTO ###\n{agente['base_conhecimento']}\n\n"
    
    if "comments" in segmentos_selecionados and agente.get('comments'):
        contexto += f"### COMENTÁRIOS DO CLIENTE ###\n{agente['comments']}\n\n"
    
    if "planejamento" in segmentos_selecionados and agente.get('planejamento'):
        contexto += f"### PLANEJAMENTO ###\n{agente['planejamento']}\n\n"
    
    # Adicionar histórico se fornecido
    if historico_mensagens:
        contexto += "### HISTÓRICO DA CONVERSA ###\n"
        for msg in historico_mensagens:
            contexto += f"{msg['role']}: {msg['content']}\n"
        contexto += "\n"
    
    contexto += "### RESPOSTA ATUAL ###\nassistant:"
    
    return contexto
