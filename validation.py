# validation.py
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

PALAVRAS_CHAVE = ['download', 'dataset', 'csv', 'excel', 'dados', 'arquivo', 'exportar', 'planilha', 'data']

EXTENSOES_DADOS = {'.csv', '.xlsx', '.json', '.zip', '.parquet', '.h5', '.hdf5', '.nc'}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/122 Safari/537.36"
}


@retry(
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
    stop=stop_after_attempt(2),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    reraise=False,
)
def _get_pagina(url: str) -> httpx.Response | None:
    return httpx.get(url, headers=HEADERS, follow_redirects=True, timeout=8)


def validar_links_de_dados(pagina_url: str) -> list[tuple[str, str, str]]:
    """
    Busca links para download de dados em uma página.
    Retorna lista de (url_arquivo, titulo_pagina, descricao_pagina).
    O título e a descrição servem como contexto para o scoring de relevância.
    """
    resultados: list[tuple[str, str, str]] = []
    try:
        resposta = _get_pagina(pagina_url)
        if resposta is None or resposta.status_code != 200:
            return []

        soup = BeautifulSoup(resposta.content, 'html.parser')
        base = pagina_url.rstrip('/')

        # Extrai título e meta description da página como contexto
        titulo_pagina = (soup.title.string or "").strip() if soup.title else ""
        meta_desc = ""
        for tag in soup.find_all("meta"):
            if tag.get("name", "").lower() in ("description", "keywords"):
                meta_desc += " " + (tag.get("content") or "")
        contexto = f"{titulo_pagina} {meta_desc}".strip()[:300]

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            texto = (a_tag.get_text() or '').lower()
            href_lower = href.lower().split('?')[0]

            if any(href_lower.endswith(ext) for ext in EXTENSOES_DADOS):
                full = (base + href) if href.startswith('/') else href
                resultados.append((full, titulo_pagina, contexto))
                continue

            if any(p in href_lower for p in PALAVRAS_CHAVE) or any(p in texto for p in PALAVRAS_CHAVE):
                if any(href_lower.endswith(ext) for ext in EXTENSOES_DADOS):
                    full = (base + href) if href.startswith('/') else href
                    resultados.append((full, titulo_pagina, contexto))

    except Exception as e:
        print(f"[validation] Erro em {pagina_url}: {e}")

    # deduplica por URL
    seen: set[str] = set()
    dedup = []
    for url, titulo, desc in resultados:
        if url not in seen:
            seen.add(url)
            dedup.append((url, titulo, desc))
    return dedup


def validar_links_em_paralelo(
    urls: list[str], max_workers: int = 10
) -> list[tuple[str, str, str]]:
    """
    Valida múltiplas páginas em paralelo.
    Retorna lista de (url_arquivo, titulo_pagina, descricao_pagina).
    """
    all_results: list[tuple[str, str, str]] = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(validar_links_de_dados, url): url for url in urls}
        for future in as_completed(futures):
            try:
                all_results.extend(future.result())
            except Exception:
                pass
    # deduplica por URL mantendo primeiro contexto encontrado
    seen: set[str] = set()
    dedup = []
    for item in all_results:
        if item[0] not in seen:
            seen.add(item[0])
            dedup.append(item)
    return dedup


def extrair_tabelas_html(pagina_url: str) -> list[pd.DataFrame]:
    """Tenta extrair tabelas HTML da página via pandas."""
    try:
        dfs = pd.read_html(pagina_url)
        return [df for df in dfs if df.shape[0] > 10 and df.shape[1] > 3]
    except Exception as e:
        print(f"[validation] Sem tabelas em {pagina_url}: {e}")
        return []
