# validation.py
import requests
from bs4 import BeautifulSoup

def validar_links_de_dados(pagina_url):
    links_dados = []
    palavras_chave = ['download', 'dataset', 'csv', 'excel', 'dados', 'arquivo']

    try:
        resposta = requests.get(pagina_url, timeout=10)
        if resposta.status_code != 200:
            return []

        soup = BeautifulSoup(resposta.content, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            texto_link = (a_tag.get_text() or '').lower()

            if any(palavra in href.lower() for palavra in palavras_chave) or any(palavra in texto_link for palavra in palavras_chave):
                if href.endswith(('.csv', '.xlsx', '.json', '.zip')):
                    if href.startswith('/'):
                        href = pagina_url.rstrip('/') + href
                    links_dados.append(href)
    except:
        pass

    return links_dados