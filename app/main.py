import streamlit as st
from auth import login, check_admin_password
from database import get_db_connection
from utils import configure_gemini, get_gemini_models
from ui import setup_interface

# Configuração inicial
st.set_page_config(
    layout="wide",
    page_title="Agente Generativo",
    page_icon="🤖"
)

def main():
    # Autenticação
    if not st.session_state.get("logged_in", False):
        login()
        return

    # Configurações iniciais
    configure_gemini()
    get_db_connection()
    
    # Setup da interface principal
    setup_interface()

if __name__ == "__main__":
    main()
