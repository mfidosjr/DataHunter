# semantic_analyzer.py

import os
import re

# --- Fallback: keyword-based analysis ---

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
    nome_coluna = nome_coluna.lower()
    tokens = re.split(r'[^a-zA-Z0-9]', nome_coluna)
    return [t for t in tokens if t]

def analisar_semantica_das_colunas(colunas):
    tags_detectadas = set()
    for coluna in colunas:
        tokens = tokenizar_coluna(coluna)
        for token in tokens:
            for categoria, palavras in CATEGORIAS_SEMANTICAS.items():
                if token in palavras:
                    tags_detectadas.add(categoria)
    return list(tags_detectadas)

def _resumo_por_keywords(colunas):
    tags = analisar_semantica_das_colunas(colunas)
    if not tags:
        return "Tipo de dados indefinido"
    return f"Dataset relacionado a: {', '.join(tags)}"


# --- Claude-powered analysis ---

def _resumo_por_groq(colunas):
    """Uses Groq to generate a rich semantic description of the dataset columns."""
    try:
        from groq import Groq
        client = Groq(api_key=os.environ["GROQ_API_KEY"])

        colunas_str = ", ".join(str(c) for c in colunas[:50])  # cap at 50 columns

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=150,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Analise os seguintes nomes de colunas de um dataset e escreva UMA frase curta "
                        f"(máximo 20 palavras) descrevendo o que este dataset provavelmente contém. "
                        f"Responda apenas a frase, sem introdução.\n\nColunas: {colunas_str}"
                    ),
                }
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return _resumo_por_keywords(colunas)


# --- Public API ---

def gerar_resumo_semantico(colunas):
    """
    Generates a semantic description of what the dataset is about.
    Uses Groq API if GROQ_API_KEY is set, otherwise falls back to keyword matching.
    """
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if api_key:
        return _resumo_por_groq(colunas)
    return _resumo_por_keywords(colunas)
