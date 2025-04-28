# validation.py
import requests
from bs4 import BeautifulSoup

def validar_links_de_dados(pagina_url):
    """Busca links e botões plausíveis para download de dados."""
    links_dados = []
    palavras_chave = ['download', 'dataset', 'csv', 'excel', 'dados', 'arquivo', 'exportar']

    try:
        resposta = requests.get(pagina_url, timeout=15)
        if resposta.status_code != 200:
            return []

        soup = BeautifulSoup(resposta.content, 'html.parser')

        # 🔵 Procurar <a href> normais
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            texto_link = (a_tag.get_text() or '').lower()

            if any(palavra in href.lower() for palavra in palavras_chave) or any(palavra in texto_link for palavra in palavras_chave):
                if any(href.lower().endswith(ext) for ext in ('.csv', '.xlsx', '.json', '.zip')):
                    if href.startswith('/'):
                        href = pagina_url.rstrip('/') + href
                    links_dados.append(href)

        # 🔵 Procurar botões que podem estar escondendo links
        for button in soup.find_all('button'):
            texto = (button.get_text() or '').lower()
            if any(palavra in texto for palavra in palavras_chave):
                # Não sabemos se botão aciona download diretamente, então apenas registra possibilidade
                links_dados.append(pagina_url)

    except Exception as e:
        print(f"Erro validando {pagina_url}: {e}")

    return list(set(links_dados))  # Remover duplicados

def extrair_tabelas_html(pagina_url):
    """Tenta extrair tabelas HTML como datasets."""
    try:
        dfs = pd.read_html(pagina_url)
        # Filtra tabelas minimamente grandes
        tabelas_validas = [df for df in dfs if df.shape[0] > 10 and df.shape[1] > 3]
        return tabelas_validas
    except Exception as e:
        print(f"Erro extraindo tabelas de {pagina_url}: {e}")
        return []
