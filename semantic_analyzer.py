# semantic_analyzer.py

import re

# 🔵 Dicionário de categorias e palavras-chave
CATEGORIAS_SEMANTICAS = {
    'geografia': ['estado', 'cidade', 'municipio', 'localidade', 'uf', 'bairro'],
    'tempo': ['ano', 'mes', 'data', 'hora', 'periodo'],
    'demografia': ['populacao', 'habitantes', 'densidade'],
    'qualidade_agua': ['ph', 'turbidez', 'temperatura', 'oxigenio', 'cloro'],
    'financeiro': ['receita', 'despesa', 'valor', 'custo', 'preco'],
    'saude': ['hospital', 'doenca', 'sintoma', 'casos', 'mortalidade'],
    'educacao': ['escola', 'aluno', 'ensino', 'nota', 'frequencia']
}

def tokenizar_coluna(nome_coluna):
    """Divide nomes de colunas compostas em tokens limpos."""
    nome_coluna = nome_coluna.lower()
    tokens = re.split(r'[^a-zA-Z0-9]', nome_coluna)
    return [t for t in tokens if t]

def analisar_semantica_das_colunas(colunas):
    """Gera uma análise semântica baseada nos nomes das colunas."""
    tags_detectadas = set()

    for coluna in colunas:
        tokens = tokenizar_coluna(coluna)
        for token in tokens:
            for categoria, palavras in CATEGORIAS_SEMANTICAS.items():
                if token in palavras:
                    tags_detectadas.add(categoria)

    return list(tags_detectadas)

def gerar_resumo_semantico(colunas):
    """Cria uma descrição textual baseada na análise semântica."""
    tags = analisar_semantica_das_colunas(colunas)
    if not tags:
        return "Tipo de dados indefinido"
    else:
        # Futuramente: ordenação por prioridade de categoria
        return f"Dataset relacionado a: {', '.join(tags)}"
