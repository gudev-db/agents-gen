import streamlit as st
import datetime
from processing.video_processor import processar_video_upload, processar_url_youtube

def render_video_interface():
    """Renderiza a interface de validação de vídeos"""
    st.header("🎬 Validação de Vídeos")
    
    if not st.session_state.agente_selecionado:
        st.info("Selecione um agente primeiro na aba de Chat")
    else:
        agente = st.session_state.agente_selecionado
        st.subheader(f"Validação com: {agente['nome']}")
        
        # Controles de segmentos para validação de vídeo
        st.sidebar.subheader("🔧 Configurações de Validação de Vídeo")
        st.sidebar.write("Selecione bases para validação:")
        
        segmentos_video = st.sidebar.multiselect(
            "Bases para validação de vídeo:",
            options=["system_prompt", "base_conhecimento", "comments", "planejamento"],
            default=st.session_state.segmentos_selecionados,
            key="video_segmentos"
        )
        
        # Seleção do tipo de entrada
        entrada_tipo = st.radio(
            "Escolha o tipo de entrada:",
            ["Upload de Arquivo", "URL do YouTube"],
            horizontal=True,
            key="video_input_type"
        )
        
        # Configurações de análise
        col_config1, col_config2 = st.columns(2)
        
        with col_config1:
            tipo_analise = st.selectbox(
                "Tipo de Análise:",
                ["completa", "rapida", "tecnica"],
                format_func=lambda x: {
                    "completa": "📊 Análise Completa",
                    "rapida": "⚡ Análise Rápida", 
                    "tecnica": "🛠️ Análise Técnica"
                }[x],
                key="tipo_analise"
            )
        
        with col_config2:
            if tipo_analise == "completa":
                st.info("Análise detalhada de todos os aspectos")
            elif tipo_analise == "rapida":
                st.info("Foco nos pontos mais críticos")
            else:
                st.info("Análise técnica e de qualidade")
        
        if entrada_tipo == "Upload de Arquivo":
            st.subheader("📤 Upload de Vídeo")
            
            uploaded_video = st.file_uploader(
                "Carregue o vídeo para análise",
                type=["mp4", "mpeg", "mov", "avi", "flv", "mpg", "webm", "wmv", "3gpp"],
                help="Formatos suportados: MP4, MPEG, MOV, AVI, FLV, MPG, WEBM, WMV, 3GPP",
                key="video_uploader"
            )
            
            if uploaded_video:
                # Exibir informações do vídeo
                st.info(f"📹 Arquivo: {uploaded_video.name}")
                st.info(f"📏 Tamanho: {uploaded_video.size / (1024*1024):.2f} MB")
                
                # Exibir preview do vídeo
                st.video(uploaded_video)
                
                # Botão de análise
                if st.button("🎬 Iniciar Análise do Vídeo", type="primary", key="analise_upload"):
                    with st.spinner('Analisando vídeo... Isso pode levar alguns minutos'):
                        resultado = processar_video_upload(
                            uploaded_video, 
                            segmentos_video, 
                            agente, 
                            tipo_analise
                        )
                        
                        st.subheader("📋 Resultado da Análise")
                        st.markdown(resultado)
                        
                        # Opção para download do relatório
                        st.download_button(
                            "💾 Baixar Relatório",
                            data=resultado,
                            file_name=f"relatorio_video_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            key="download_upload"
                        )
        
        else:  # URL do YouTube
            st.subheader("🔗 URL do YouTube")
            
            youtube_url = st.text_input(
                "Cole a URL do vídeo do YouTube:",
                placeholder="https://www.youtube.com/watch?v=...",
                help="A URL deve ser pública (não privada ou não listada)",
                key="youtube_url"
            )
            
            if youtube_url:
                # Validar URL do YouTube
                if "youtube.com" in youtube_url or "youtu.be" in youtube_url:
                    st.success("✅ URL do YouTube válida detectada")
                    
                    # Botão de análise
                    if st.button("🎬 Iniciar Análise do Vídeo", type="primary", key="analise_youtube"):
                        with st.spinner('Analisando vídeo do YouTube... Isso pode levar alguns minutos'):
                            resultado = processar_url_youtube(
                                youtube_url, 
                                segmentos_video, 
                                agente, 
                                tipo_analise
                            )
                            
                            st.subheader("📋 Resultado da Análise")
                            st.markdown(resultado)
                            
                            # Opção para download do relatório
                            st.download_button(
                                "💾 Baixar Relatório",
                                data=resultado,
                                file_name=f"relatorio_youtube_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                mime="text/plain",
                                key="download_youtube"
                            )
                else:
                    st.error("❌ Por favor, insira uma URL válida do YouTube")
        
        # Seção de informações
        with st.expander("ℹ️ Informações sobre Análise de Vídeos"):
            st.markdown("""
            ### 📹 Capacidades de Análise
            
            O agente pode analisar vídeos considerando:
            
            **🎯 Conteúdo e Mensagem:**
            - Alinhamento com diretrizes da marca
            - Clareza da mensagem principal
            - Tom e linguagem apropriados
            - Valores e posicionamento
            
            **🎨 Aspectos Visuais:**
            - Identidade visual (cores, logos, tipografia)
            - Qualidade de produção
            - Consistência da marca
            - Enquadramento e composição
            
            **🔊 Aspectos de Áudio:**
            - Qualidade do áudio
            - Trilha sonora adequada
            - Narração/diálogo claro
            - Mixagem e balanceamento
            
            **📊 Estrutura e Engajamento:**
            - Ritmo e duração apropriados
            - Manutenção do interesse
            - Chamadas para ação eficazes
            - Progressão lógica
            
            ### ⚠️ Limitações Técnicas
            
            - **Duração**: Recomendado até 2 horas para análise completa
            - **Formato**: Formatos comuns de vídeo suportados
            - **Qualidade**: Análise em 1 frame por segundo padrão
            - **YouTube**: Apenas vídeos públicos
            """)
