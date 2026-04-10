# search.py
from ddgs import DDGS

# 🔵 Variantes padrão de busca
VARIANTES_QUERY = [
    "{query}",
    "{query} site:.gov.br",
    "{query} site:.gov",
    "{query} filetype:csv OR filetype:xlsx OR filetype:json",
    "{query} dataset",
    "{query} download dados"
]

# 🔵 Fontes preferidas para priorizar
FONTES_PREFERIDAS = ['data.gov', 'dados.gov', 'gov.br', '.gov', '.edu', 'kaggle.com']

def buscar_paginas(query, max_results=30):
    """Realiza busca inteligente, tentando várias variantes da consulta."""
    links_priorizados = []
    outros_links = []

    try:
        with DDGS() as ddgs:
            resultados = []
            for template in VARIANTES_QUERY:
                consulta = template.format(query=query)
                resultados += ddgs.text(consulta, max_results=max_results)

        for resultado in resultados:
            url = resultado.get('href', '')
            if any(fonte in url for fonte in FONTES_PREFERIDAS):
                links_priorizados.append(url)
            else:
                outros_links.append(url)

    except Exception as e:
        print(f"Erro ao buscar páginas: {e}")
        return []

    # Remover duplicados mantendo prioridade
    links_final = list(dict.fromkeys(links_priorizados + outros_links))
    return links_final
