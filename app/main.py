import streamlit as st
from auth.authentication import login, check_admin_password
from database.mongodb import get_db_connection
from ui.tabs_manager import setup_interface
from utils.config import configure_gemini

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
