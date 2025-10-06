import streamlit as st
from auth.authentication import check_admin_password
from agents.crud import listar_agentes, desativar_agente, criar_agente, atualizar_agente, listar_agentes_mae
from agents.inheritance import obter_agente_com_heranca
from ui.chat_interface import render_chat_interface
from ui.video_interface import render_video_interface
from ui.management_interface import render_management_interface
from ui.validation_interface import render_validation_interface
from ui.generation_interface import render_generation_interface
from ui.summary_interface import render_summary_interface

def setup_interface():
    """Configura a interface principal com todas as abas"""
    
    # Sidebar com informações do usuário
    st.sidebar.title(f"🤖 Bem-vindo, {st.session_state.user}!")
    
    # Botão de logout na sidebar
    if st.sidebar.button("🚪 Sair", key="logout_btn"):
        for key in ["logged_in", "user", "admin_password_correct", "admin_user"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    st.title("🤖 Agente Generativo Personalizável")

    # Inicializar estado da sessão
    if "agente_selecionado" not in st.session_state:
        st.session_state.agente_selecionado = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "segmentos_selecionados" not in st.session_state:
        st.session_state.segmentos_selecionados = ["system_prompt", "base_conhecimento", "comments", "planejamento"]

    # Menu de abas
    tab_chat, tab_gerenciamento, tab_aprovacao, tab_video, tab_geracao, tab_resumo = st.tabs([
        "💬 Chat", 
        "⚙️ Gerenciar Agentes", 
        "✅ Validação", 
        "🎬 Validação de Vídeo",
        "✨ Geração de Conteúdo",
        "📝 Resumo de Textos"
    ])

    with tab_gerenciamento:
        render_management_interface()

    with tab_chat:
        render_chat_interface()

    with tab_video:
        render_video_interface()

    with tab_aprovacao:
        render_validation_interface()

    with tab_geracao:
        render_generation_interface()

    with tab_resumo:
        render_summary_interface()

    # Estilização
    st.markdown("""
    <style>
        .stChatMessage {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        [data-testid="stChatMessageContent"] {
            font-size: 1rem;
        }
        .stChatInput {
            bottom: 20px;
            position: fixed;
            width: calc(100% - 5rem);
        }
        div[data-testid="stTabs"] {
            margin-top: -30px;
        }
        div[data-testid="stVerticalBlock"] > div:has(>.stTextArea) {
            border-left: 3px solid #4CAF50;
            padding-left: 1rem;
        }
        .segment-indicator {
            background-color: #f0f2f6;
            padding: 0.5rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            border-left: 4px solid #4CAF50;
        }
        .video-analysis-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        .inheritance-badge {
            background-color: #e3f2fd;
            color: #1976d2;
            padding: 0.2rem 0.5rem;
            border-radius: 12px;
            font-size: 0.8rem;
            margin-left: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)
