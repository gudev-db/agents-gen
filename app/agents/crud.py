import datetime
from bson import ObjectId
from database.mongodb import get_db_connection

def criar_agente(nome, system_prompt, base_conhecimento, comments, planejamento, categoria, agente_mae_id=None, herdar_elementos=None):
    """Cria um novo agente no MongoDB"""
    collection_agentes, _ = get_db_connection()
    
    agente = {
        "nome": nome,
        "system_prompt": system_prompt,
        "base_conhecimento": base_conhecimento,
        "comments": comments,
        "planejamento": planejamento,
        "categoria": categoria,
        "agente_mae_id": agente_mae_id,
        "herdar_elementos": herdar_elementos or [],
        "data_criacao": datetime.datetime.now(),
        "ativo": True
    }
    result = collection_agentes.insert_one(agente)
    return result.inserted_id

def listar_agentes():
    """Retorna todos os agentes ativos"""
    collection_agentes, _ = get_db_connection()
    return list(collection_agentes.find({"ativo": True}).sort("data_criacao", -1))

def listar_agentes_mae():
    """Retorna apenas agentes que podem ser mães (não são filhos)"""
    collection_agentes, _ = get_db_connection()
    return list(collection_agentes.find({"ativo": True, "agente_mae_id": None}).sort("data_criacao", -1))

def obter_agente(agente_id):
    """Obtém um agente específico pelo ID"""
    collection_agentes, _ = get_db_connection()
    if isinstance(agente_id, str):
        agente_id = ObjectId(agente_id)
    return collection_agentes.find_one({"_id": agente_id})

def atualizar_agente(agente_id, nome, system_prompt, base_conhecimento, comments, planejamento, categoria, agente_mae_id=None, herdar_elementos=None):
    """Atualiza um agente existente"""
    collection_agentes, _ = get_db_connection()
    if isinstance(agente_id, str):
        agente_id = ObjectId(agente_id)
    return collection_agentes.update_one(
        {"_id": agente_id},
        {
            "$set": {
                "nome": nome,
                "system_prompt": system_prompt,
                "base_conhecimento": base_conhecimento,
                "comments": comments,
                "planejamento": planejamento,
                "categoria": categoria,
                "agente_mae_id": agente_mae_id,
                "herdar_elementos": herdar_elementos or [],
                "data_atualizacao": datetime.datetime.now()
            }
        }
    )

def desativar_agente(agente_id):
    """Desativa um agente (soft delete)"""
    collection_agentes, _ = get_db_connection()
    if isinstance(agente_id, str):
        agente_id = ObjectId(agente_id)
    return collection_agentes.update_one(
        {"_id": agente_id},
        {"$set": {"ativo": False, "data_desativacao": datetime.datetime.now()}}
    )
