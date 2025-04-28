# search.py
import requests
from duckduckgo_search import DDGS

def buscar_paginas(query, max_results=30):
    """Realiza busca inteligente, tentando várias variantes da consulta."""
    variantes = [
        query,
        f"{query} site:.gov.br",
        f"{query} site:.gov",
        f"{query} filetype:csv OR filetype:xlsx OR filetype:json",
        f"{query} dataset",
        f"{query} download dados"
    ]

    fontes_preferidas = ['data.gov', 'dados.gov', 'gov.br', '.gov', '.edu', 'kaggle.com']
    links_priorizados = []
    outros_links = []

    with DDGS() as ddgs:
        resultados = []
        for variante in variantes:
            resultados += ddgs.text(variante, max_results=max_results)

    for resultado in resultados:
        url = resultado.get('href', '')
        if any(fonte in url for fonte in fontes_preferidas):
            links_priorizados.append(url)
        else:
            outros_links.append(url)

    # Remover duplicados mantendo prioridade
    links_final = list(dict.fromkeys(links_priorizados + outros_links))
    return links_final
