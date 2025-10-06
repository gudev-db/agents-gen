import streamlit as st
import os
import google.generativeai as genai

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
