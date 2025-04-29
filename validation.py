# validation.py
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 🔵 Palavras-chave globais
PALAVRAS_CHAVE = ['download', 'dataset', 'csv', 'excel', 'dados', 'arquivo', 'exportar', 'planilha']

# 🔵 Cabeçalhos padrão para requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36"
}

def validar_links_de_dados(pagina_url):
    """Busca links e botões plausíveis para download de dados."""
    links_dados = []

    try:
        resposta = requests.get(pagina_url, headers=HEADERS, timeout=15)
        if resposta.status_code != 200:
            return []

        soup = BeautifulSoup(resposta.content, 'html.parser')

        # Buscar links
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            texto = (a_tag.get_text() or '').lower()

            if any(palavra in href.lower() for palavra in PALAVRAS_CHAVE) or any(palavra in texto for palavra in PALAVRAS_CHAVE):
                if any(href.lower().endswith(ext) for ext in ['.csv', '.xlsx', '.json', '.zip']):
                    if href.startswith('/'):
                        href = pagina_url.rstrip('/') + href
                    links_dados.append(href)

        # Buscar botões de download
        for button in soup.find_all('button'):
            texto = (button.get_text() or '').lower()
            if any(palavra in texto for palavra in PALAVRAS_CHAVE):
                links_dados.append(pagina_url)

    except Exception as e:
        print(f"Erro validando {pagina_url}: {e}")

    return list(set(links_dados))

def extrair_tabelas_html(pagina_url):
    """Tenta extrair tabelas HTML padrão. Se falhar, usa Selenium."""
    try:
        dfs = pd.read_html(pagina_url)
        tabelas_validas = [df for df in dfs if df.shape[0] > 10 and df.shape[1] > 3]
        if tabelas_validas:
            return tabelas_validas
    except Exception as e:
        print(f"Pandas não conseguiu extrair: {e}")

    # Selenium como fallback
    options = Options()
    options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent={HEADERS['User-Agent']}")

    driver = None

    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.set_page_load_timeout(20)
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

        return tabelas_extraidas

    except Exception as e:
        print(f"Selenium também não conseguiu extrair: {e}")
        return []

    finally:
        if driver:
            driver.quit()
