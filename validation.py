# validation.py
import requests
import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def validar_links_de_dados(pagina_url):
    """Busca links, botões e possíveis downloads dentro da página."""
    links_dados = []
    palavras_chave = ['download', 'dataset', 'csv', 'excel', 'dados', 'arquivo', 'exportar', 'planilha']

    try:
        resposta = requests.get(pagina_url, timeout=15)
        if resposta.status_code != 200:
            return []

        soup = BeautifulSoup(resposta.content, 'html.parser')

        # 🔵 Buscar links
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            texto = (a_tag.get_text() or '').lower()

            if any(palavra in href.lower() for palavra in palavras_chave) or any(palavra in texto for palavra in palavras_chave):
                if any(href.lower().endswith(ext) for ext in ['.csv', '.xlsx', '.json', '.zip']):
                    if href.startswith('/'):
                        href = pagina_url.rstrip('/') + href
                    links_dados.append(href)

        # 🔵 Buscar botões de download
        for button in soup.find_all('button'):
            texto = (button.get_text() or '').lower()
            if any(palavra in texto for palavra in palavras_chave):
                links_dados.append(pagina_url)  # Pode ser necessário renderizar com Selenium depois

    except Exception as e:
        print(f"Erro validando {pagina_url}: {e}")

    return list(set(links_dados))  # Remove duplicados

def extrair_tabelas_html(pagina_url):
    """Tenta extrair tabelas HTML visíveis; se falhar, usa Selenium para capturar."""
    try:
        # Primeiro tenta pandas
        dfs = pd.read_html(pagina_url)
        tabelas_validas = [df for df in dfs if df.shape[0] > 10 and df.shape[1] > 3]
        if tabelas_validas:
            return tabelas_validas
    except Exception as e:
        print(f"Pandas não conseguiu extrair: {e}")

    # Se pandas falhar, usar Selenium
    try:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get(pagina_url)

        tabelas_html = driver.find_elements(By.TAG_NAME, 'table')
        tabelas_extraidas = []

        for tabela in tabelas_html:
            html_tabela = tabela.get_attribute('outerHTML')
            try:
                dfs = pd.read_html(html_tabela)
                for df in dfs:
                    if df.shape[0] > 10 and df.shape[1] > 3:
                        tabelas_extraidas.append(df)
            except:
                continue

        driver.quit()
        return tabelas_extraidas

    except Exception as e:
        print(f"Selenium também não conseguiu extrair: {e}")
        return []
