import streamlit as st
from processing.context_builder import construir_contexto
from utils.config import get_gemini_models
from google.genai import types

def processar_video_upload(video_file, segmentos_selecionados, agente, tipo_analise="completa"):
    """Processa vídeo upload e retorna análise"""
    try:
        modelo_vision, _ = get_gemini_models()
        video_bytes = video_file.read()
        
        contexto = construir_contexto(agente, segmentos_selecionados)
        
        if tipo_analise == "completa":
            prompt = f"""
            {contexto}
            
            Analise este vídeo considerando as diretrizes fornecidas e forneça um relatório detalhado:
            
            ## 🎬 ANÁLISE DO VÍDEO
            
            ### 📊 Resumo Executivo
            [Forneça uma visão geral da conformidade do vídeo com as diretrizes]
            
            ### ✅ Pontos de Conformidade
            - [Liste os aspectos que estão em conformidade]
            
            ### ⚠️ Pontos de Atenção
            - [Liste os aspectos que precisam de ajustes]
            
            ### 🎯 Análise de Conteúdo
            - **Mensagem**: [Avalie se a mensagem está alinhada]
            - **Tom e Linguagem**: [Avalie o tom utilizado]
            - **Valores da Marca**: [Verifique alinhamento com valores]
            
            ### 🎨 Análise Visual
            - **Identidade Visual**: [Cores, logos, tipografia]
            - **Qualidade Técnica**: [Iluminação, enquadramento, áudio]
            - **Consistência**: [Manutenção da identidade ao longo do vídeo]
            
            ### 🔊 Análise de Áudio
            - [Qualidade, trilha sonora, voz]
            
            ### 📋 Recomendações Específicas
            [Liste recomendações práticas para melhorias]
            
            ### 🏆 Avaliação Final
            [Aprovado/Reprovado/Com ajustes] - [Justificativa]
            """
        elif tipo_analise == "rapida":
            prompt = f"""
            {contexto}
            
            Faça uma análise rápida deste vídeo focando nos aspectos mais críticos:
            
            ### 🔍 Análise Rápida
            - **Conformidade Geral**: [Avaliação geral]
            - **Principais Pontos Positivos**: [2-3 pontos]
            - **Principais Problemas**: [2-3 pontos críticos]
            - **Recomendação Imediata**: [Aprovar/Reprovar/Ajustar]
            """
        else:  # análise técnica
            prompt = f"""
            {contexto}
            
            Faça uma análise técnica detalhada do vídeo:
            
            ### 🛠️ Análise Técnica
            - **Qualidade de Vídeo**: [Resolução, estabilidade, compressão]
            - **Qualidade de Áudio**: [Clareza, ruído, mixagem]
            - **Edição e Transições**: [Fluidez, ritmo, cortes]
            - **Aspectos Técnicos Conformes**: 
            - **Problemas Técnicos Identificados**:
            - **Recomendações Técnicas**:
            """
        
        response = modelo_vision.generate_content(
            contents=[
                types.Part(
                    inline_data=types.Blob(
                        data=video_bytes,
                        mime_type=video_file.type
                    )
                ),
                types.Part(text=prompt)
            ]
        )
        
        return response.text
        
    except Exception as e:
        return f"Erro ao processar vídeo: {str(e)}"

def processar_url_youtube(youtube_url, segmentos_selecionados, agente, tipo_analise="completa"):
    """Processa URL do YouTube e retorna análise"""
    try:
        modelo_vision, _ = get_gemini_models()
        contexto = construir_contexto(agente, segmentos_selecionados)
        
        if tipo_analise == "completa":
            prompt = f"""
            {contexto}
            
            Analise este vídeo do YouTube considerando as diretrizes fornecidas:
            
            ## 🎬 ANÁLISE DO VÍDEO - YOUTUBE
            
            ### 📊 Resumo Executivo
            [Avaliação geral de conformidade]
            
            ### 🎯 Conteúdo e Mensagem
            - Alinhamento com diretrizes: 
            - Clareza da mensagem:
            - Tom e abordagem:
            
            ### 🎨 Aspectos Visuais
            - Identidade visual:
            - Qualidade de produção:
            - Consistência da marca:
            
            ### 🔊 Aspectos de Áudio
            - Qualidade do áudio:
            - Trilha sonora:
            - Narração/diálogo:
            
            ### 📈 Estrutura e Engajamento
            - Ritmo do vídeo:
            - Manutenção do interesse:
            - Chamadas para ação:
            
            ### ✅ Pontos Fortes
            - [Liste os pontos positivos]
            
            ### ⚠️ Pontos de Melhoria
            - [Liste sugestões de melhoria]
            
            ### 🏆 Recomendação Final
            [Status e justificativa]
            """
        
        response = modelo_vision.generate_content(
            contents=[
                types.Part(
                    file_data=types.FileData(file_uri=youtube_url)
                ),
                types.Part(text=prompt)
            ]
        )
        
        return response.text
        
    except Exception as e:
        return f"Erro ao processar URL do YouTube: {str(e)}"
