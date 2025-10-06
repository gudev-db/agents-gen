import streamlit as st
from utils.config import get_gemini_models

def render_generation_interface():
    """Renderiza a interface de geração de conteúdo"""
    st.header("✨ Geração de Conteúdo")
    
    if not st.session_state.agente_selecionado:
        st.info("Selecione um agente primeiro na aba de Chat")
    else:
        agente = st.session_state.agente_selecionado
        st.subheader(f"Geração com: {agente['nome']}")
        
        campanha_brief = st.text_area("Briefing criativo:", help="Descreva objetivos, tom de voz e especificações", height=150, key="campanha_brief")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Diretrizes Visuais")
            if st.button("Gerar Especificações Visuais", key="gen_visual"):
                with st.spinner('Criando guia de estilo...'):
                    prompt = f"""
                    {agente['system_prompt']}
                    
                            Brand Guidelines:
                            ###BEGIN Brand Guidelines###
                            {agente.get('base_conhecimento', '')}
                            ###END Brand Guidelines###

                            Comentários de observação de conteúdo do cliente:
                            ###BEGIN COMMENTS FROM CLIENT###
                            {agente.get('comments', '')}
                            ###END COMMENTS FROM CLIENT###
                    
                            Planejamento:
                            ###BEGIN PLANEJAMENTO###
                            {agente.get('planejamento', '')}
                            ###END PLANEJAMENTO###
                    
                    Com base no briefing: {campanha_brief}
                    
                    Crie um manual técnico para designers incluindo:
                    1. 🎨 Paleta de cores (códigos HEX/RGB)
                    2. 🖼️ Diretrizes de fotografia/ilustração
                    3. ✏️ Tipografia hierárquica
                    4. 📐 Grid e proporções recomendadas
                    5. ⚠️ Restrições de uso
                    6. 🖌️ Descrição da imagem principal sugerida
                    7. 📱 Adaptações para diferentes formatos
                    """
                    _, modelo_texto = get_gemini_models()
                    resposta = modelo_texto.generate_content(prompt)
                    st.markdown(resposta.text)

        with col2:
            st.subheader("Copywriting")
            if st.button("Gerar Textos", key="gen_copy"):
                with st.spinner('Desenvolvendo conteúdo textual...'):
                    prompt = f"""
                    {agente['system_prompt']}
                    
                            Brand Guidelines:
                            ###BEGIN Brand Guidelines###
                            {agente.get('base_conhecimento', '')}
                            ###END Brand Guidelines###

                            Comentários de observação de conteúdo do cliente:
                            ###BEGIN COMMENTS FROM CLIENT###
                            {agente.get('comments', '')}
                            ###END COMMENTS FROM CLIENT###
                    
                            Planejamento:
                            ###BEGIN PLANEJAMENTO###
                            {agente.get('planejamento', '')}
                            ###END PLANEJAMENTO###
                    
                    Com base no briefing: {campanha_brief}
                    
                    Crie textos para campanha incluindo:
                    - 📝 Legenda principal (com emojis e quebras de linha)
                    - 🏷️ 10 hashtags relevantes
                    - 🔗 Sugestão de link (se aplicável)
                    - 📢 CTA adequado ao objetivo
                    - 🎯 3 opções de headline
                    - 📄 Corpo de texto (200 caracteres)
                    """
                    _, modelo_texto = get_gemini_models()
                    resposta = modelo_texto.generate_content(prompt)
                    st.markdown(resposta.text)
