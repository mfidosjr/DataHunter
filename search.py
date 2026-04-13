# search.py
from ddgs import DDGS

FONTES_PREFERIDAS = [
    # Genéricas
    'data.gov', 'dados.gov', 'gov.br', '.gov', '.edu',
    'kaggle.com', 'zenodo.org',
    # Espectro / EMC / RF
    'fcc.gov', 'anatel.gov.br', 'itu.int', 'etsi.org',
    'ofcom.org.uk', 'bundesnetzagentur.de',
    # Científico / engenharia
    'ieee-dataport.org', 'ieee.org', 'data.europa.eu',
    'opendata.cern.ch', 'figshare.com',
]

# Suffixes that indicate the page URL itself is a downloadable file
EXTENSOES_DIRETAS = {'.csv', '.xlsx', '.json', '.zip', '.parquet', '.h5', '.hdf5', '.nc'}


def buscar_paginas(query: str, max_results: int = 12) -> tuple[list[str], list[str]]:
    """
    Busca páginas com DuckDuckGo para a query fornecida.
    Retorna (diretos, paginas) onde:
      - diretos: URLs que já apontam para arquivos de dados
      - paginas: URLs de páginas a serem crawleadas
    """
    diretos: list[str] = []
    paginas_priorizadas: list[str] = []
    outras_paginas: list[str] = []

    try:
        with DDGS() as ddgs:
            resultados = ddgs.text(query, max_results=max_results)
    except Exception as e:
        print(f"[search] Erro ao buscar '{query}': {e}")
        return [], []

    for r in (resultados or []):
        url = r.get('href', '')
        if not url:
            continue
        ext = '.' + url.split('?')[0].rsplit('.', 1)[-1].lower() if '.' in url.split('?')[0] else ''
        if ext in EXTENSOES_DIRETAS:
            diretos.append(url)
        elif any(f in url for f in FONTES_PREFERIDAS):
            paginas_priorizadas.append(url)
        else:
            outras_paginas.append(url)

    paginas = list(dict.fromkeys(paginas_priorizadas + outras_paginas))
    return list(dict.fromkeys(diretos)), paginas
