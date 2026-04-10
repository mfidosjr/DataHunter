# validation.py
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

PALAVRAS_CHAVE = ['download', 'dataset', 'csv', 'excel', 'dados', 'arquivo', 'exportar', 'planilha']

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36"
}


@retry(
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=8),
    reraise=False,
)
def _get_pagina(url: str) -> httpx.Response | None:
    return httpx.get(url, headers=HEADERS, follow_redirects=True, timeout=15)


def validar_links_de_dados(pagina_url):
    """Busca links e botões plausíveis para download de dados, com retry automático."""
    links_dados = []

    try:
        resposta = _get_pagina(pagina_url)
        if resposta is None or resposta.status_code != 200:
            return []

        soup = BeautifulSoup(resposta.content, 'html.parser')

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            texto = (a_tag.get_text() or '').lower()

            if any(p in href.lower() for p in PALAVRAS_CHAVE) or any(p in texto for p in PALAVRAS_CHAVE):
                if any(href.lower().endswith(ext) for ext in ['.csv', '.xlsx', '.json', '.zip']):
                    if href.startswith('/'):
                        href = pagina_url.rstrip('/') + href
                    links_dados.append(href)

        for button in soup.find_all('button'):
            texto = (button.get_text() or '').lower()
            if any(p in texto for p in PALAVRAS_CHAVE):
                links_dados.append(pagina_url)

    except Exception as e:
        print(f"[validation] Erro em {pagina_url}: {e}")

    return list(set(links_dados))


def extrair_tabelas_html(pagina_url):
    """Tenta extrair tabelas HTML. Fallback para Selenium se necessário."""
    try:
        dfs = pd.read_html(pagina_url)
        tabelas_validas = [df for df in dfs if df.shape[0] > 10 and df.shape[1] > 3]
        if tabelas_validas:
            return tabelas_validas
    except Exception as e:
        print(f"[validation] Pandas não extraiu tabelas de {pagina_url}: {e}")

    # Selenium como fallback
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent={HEADERS['User-Agent']}")

    driver = None
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.set_page_load_timeout(20)
        driver.get(pagina_url)

        tabelas_extraidas = []
        for tabela in driver.find_elements(By.TAG_NAME, 'table'):
            html_tabela = tabela.get_attribute('outerHTML')
            try:
                dfs = pd.read_html(html_tabela)
                for df in dfs:
                    if df.shape[0] > 10 and df.shape[1] > 3:
                        tabelas_extraidas.append(df)
            except Exception:
                continue

        return tabelas_extraidas

    except Exception as e:
        print(f"[validation] Selenium falhou em {pagina_url}: {e}")
        return []

    finally:
        if driver:
            driver.quit()
