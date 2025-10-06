import streamlit as st
from agents.crud import listar_agentes, salvar_conversa
from agents.inheritance import obter_agente_com_heranca
from processing.context_builder import construir_contexto
from utils.config import get_gemini_models

def render_chat_interface():
    """Renderiza a interface do chat"""
    st.header("💬 Chat com Agente")
    
    # Seleção de agente se não houver um selecionado
    if not st.session_state.agente_selecionado:
        agentes = listar_agentes()
        if agentes:
            # Agrupar agentes por categoria
            agentes_por_categoria = {}
            for agente in agentes:
                categoria = agente.get('categoria', 'Social')
                if categoria not in agentes_por_categoria:
                    agentes_por_categoria[categoria] = []
                agentes_por_categoria[categoria].append(agente)
            
            # Seleção com agrupamento
            agente_options = {}
            for categoria, agentes_cat in agentes_por_categoria.items():
                for agente in agentes_cat:
                    agente_completo = obter_agente_com_heranca(agente['_id'])
                    display_name = f"{agente['nome']} ({categoria})"
                    if agente.get('agente_mae_id'):
                        display_name += " 🔗"
                    agente_options[display_name] = agente_completo
            
            agente_selecionado_display = st.selectbox("Selecione um agente para conversar:", 
                                                     list(agente_options.keys()))
            
            if st.button("Iniciar Conversa", key="iniciar_chat"):
                st.session_state.agente_selecionado = agente_options[agente_selecionado_display]
                st.session_state.messages = []
                st.rerun()
        else:
            st.info("Nenhum agente disponível. Crie um agente primeiro na aba de Gerenciamento.")
    else:
        agente = st.session_state.agente_selecionado
        st.subheader(f"Conversando com: {agente['nome']}")
        
        # Mostrar informações de herança se aplicável
        if 'agente_mae_id' in agente and agente['agente_mae_id']:
            from agents.crud import obter_agente
            agente_original = obter_agente(agente['_id'])
            if agente_original and agente_original.get('herdar_elementos'):
                st.info(f"🔗 Este agente herda {len(agente_original['herdar_elementos'])} elementos do agente mãe")
        
        # Controles de segmentos na sidebar do chat
        st.sidebar.subheader("🔧 Configurações do Agente")
        st.sidebar.write("Selecione quais bases de conhecimento usar:")
        
        segmentos_disponiveis = {
            "Prompt do Sistema": "system_prompt",
            "Brand Guidelines": "base_conhecimento", 
            "Comentários do Cliente": "comments",
            "Planejamento": "planejamento"
        }
        
        segmentos_selecionados = []
        for nome, chave in segmentos_disponiveis.items():
            if st.sidebar.checkbox(nome, value=chave in st.session_state.segmentos_selecionados, key=f"seg_{chave}"):
                segmentos_selecionados.append(chave)
        
        st.session_state.segmentos_selecionados = segmentos_selecionados
        
        # Exibir status dos segmentos
        if segmentos_selecionados:
            st.sidebar.success(f"✅ Usando {len(segmentos_selecionados)} segmento(s)")
        else:
            st.sidebar.warning("⚠️ Nenhum segmento selecionado")
        
        # Botão para trocar de agente
        if st.button("Trocar de Agente", key="trocar_agente"):
            st.session_state.agente_selecionado = None
            st.session_state.messages = []
            st.rerun()
        
        # Exibir histórico de mensagens
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Input do usuário
        if prompt := st.chat_input("Digite sua mensagem..."):
            # Adicionar mensagem do usuário ao histórico
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Construir contexto com segmentos selecionados
            contexto = construir_contexto(
                agente, 
                st.session_state.segmentos_selecionados, 
                st.session_state.messages
            )
            
            # Gerar resposta
            with st.chat_message("assistant"):
                with st.spinner('Pensando...'):
                    try:
                        _, modelo_texto = get_gemini_models()
                        resposta = modelo_texto.generate_content(contexto)
                        st.markdown(resposta.text)
                        
                        # Adicionar ao histórico
                        st.session_state.messages.append({"role": "assistant", "content": resposta.text})
                        
                        # Salvar conversa com segmentos utilizados
                        salvar_conversa(
                            agente['_id'], 
                            st.session_state.messages,
                            st.session_state.segmentos_selecionados
                        )
                        
                    except Exception as e:
                        st.error(f"Erro ao gerar resposta: {str(e)}")
