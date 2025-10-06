import streamlit as st
from pymongo import MongoClient

def get_db_connection():
    """Estabelece conexão com MongoDB e retorna as coleções"""
    if "db_initialized" not in st.session_state:
        try:
            client = MongoClient("mongodb+srv://gustavoromao3345:RqWFPNOJQfInAW1N@cluster0.5iilj.mongodb.net/auto_doc?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE&tlsAllowInvalidCertificates=true")
            db = client['agentes_personalizados']
            st.session_state.collection_agentes = db['agentes']
            st.session_state.collection_conversas = db['conversas']
            st.session_state.db_initialized = True
        except Exception as e:
            st.error(f"Erro ao conectar com MongoDB: {str(e)}")
            st.stop()
    
    return st.session_state.collection_agentes, st.session_state.collection_conversas
