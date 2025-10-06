import io
from PIL import Image
from utils.config import get_gemini_models

def processar_imagem(uploaded_image, agente):
    """Processa análise de imagem"""
    try:
        modelo_vision, _ = get_gemini_models()
        image = Image.open(uploaded_image)
        img_bytes = io.BytesIO()
        image.save(img_bytes, format=image.format)
        
        prompt_analise = f"""
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
        
        Analise esta imagem e forneça um parecer detalhado com:
        - ✅ Pontos positivos
        - ❌ Pontos que precisam de ajuste
        - 🛠 Recomendações específicas
        - Avaliação final (aprovado/reprovado/com observações)
        """
        
        resposta = modelo_vision.generate_content([
            prompt_analise,
            {"mime_type": "image/jpeg", "data": img_bytes.getvalue()}
        ])
        return resposta.text
    except Exception as e:
        return f"Falha na análise: {str(e)}"

def processar_texto_validacao(texto_input, agente):
    """Processa validação de texto"""
    try:
        _, modelo_texto = get_gemini_models()
        
        prompt_analise = f"""
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
    
        Analise este texto e forneça um parecer detalhado:
        
        Texto a ser analisado:
        {texto_input}
        
        Formato da resposta:
        ### Análise Geral
        [resumo da análise]
        
        ### Pontos Fortes
        - [lista de pontos positivos]
        
        ### Pontos a Melhorar
        - [lista de sugestões]
        
        ### Recomendações
        - [ações recomendadas]
        
        ### Versão Ajustada (se necessário)
        [texto revisado]
        """
        
        resposta = modelo_texto.generate_content(prompt_analise)
        return resposta.text
    except Exception as e:
        return f"Erro ao processar texto: {str(e)}"
