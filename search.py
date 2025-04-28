# search.py
import requests
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup

def buscar_paginas(query, max_results=20):
    fontes_preferidas = ['data.gov', 'dados.gov', 'kaggle.com', '.gov', '.edu']
    links_priorizados = []
    outros_links = []

    with DDGS() as ddgs:
        resultados = ddgs.text(f"{query} filetype:csv OR filetype:xlsx OR filetype:json OR filetype:zip", max_results=max_results)

    for resultado in resultados:
        url = resultado.get('href', '')
        if any(fonte in url for fonte in fontes_preferidas):
            links_priorizados.append(url)
        else:
            outros_links.append(url)

    return links_priorizados + outros_links