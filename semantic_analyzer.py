# semantic_analyzer.py

def analisar_semantica_das_colunas(colunas):
    """Gera uma análise semântica baseada nos nomes das colunas."""
    categorias = {
        'geografia': ['estado', 'cidade', 'municipio', 'localidade', 'uf', 'bairro'],
        'tempo': ['ano', 'mes', 'data', 'hora', 'periodo'],
        'demografia': ['populacao', 'habitantes', 'densidade'],
        'qualidade_agua': ['ph', 'turbidez', 'temperatura', 'oxigenio', 'cloro'],
        'financeiro': ['receita', 'despesa', 'valor', 'custo', 'preco'],
        'saude': ['hospital', 'doenca', 'sintoma', 'casos', 'mortalidade'],
        'educacao': ['escola', 'aluno', 'ensino', 'nota', 'frequencia']
    }

    tags_detectadas = set()

    for coluna in colunas:
        coluna_lower = coluna.lower()
        for categoria, palavras in categorias.items():
            if any(palavra in coluna_lower for palavra in palavras):
                tags_detectadas.add(categoria)

    return list(tags_detectadas)

def gerar_resumo_semantico(colunas):
    """Cria uma descrição textual baseada na análise semântica."""
    tags = analisar_semantica_das_colunas(colunas)
    if not tags:
        return "Tipo de dados indefinido"
    else:
        return f"Dataset relacionado a: {', '.join(tags)}"
