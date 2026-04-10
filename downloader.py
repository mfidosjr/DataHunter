# downloader.py
import os
import zipfile
import re

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


def limpar_nome_arquivo(url):
    """Limpa e extrai um nome de arquivo seguro da URL."""
    nome = url.split("/")[-1].split("?")[0]
    nome = re.sub(r'[^a-zA-Z0-9_\-.]', '_', nome)
    return nome or "arquivo_baixado"


@retry(
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=False,
)
def _get_com_retry(url: str, timeout: int) -> httpx.Response:
    return httpx.get(url, follow_redirects=True, timeout=timeout)


def baixar_arquivo(url, destino_pasta='datasets', timeout=20):
    """
    Baixa um arquivo de dados com retry automático (até 3 tentativas, backoff exponencial).
    Se for ZIP, descompacta automaticamente.
    """
    os.makedirs(destino_pasta, exist_ok=True)
    nome_arquivo = limpar_nome_arquivo(url)
    caminho_arquivo = os.path.join(destino_pasta, nome_arquivo)

    try:
        resposta = _get_com_retry(url, timeout)
        if resposta is None:
            return None
        if resposta.status_code != 200:
            return None
        if 'text/html' in resposta.headers.get('content-type', ''):
            return None

        with open(caminho_arquivo, 'wb') as f:
            f.write(resposta.content)

    except Exception as e:
        print(f"[downloader] Falha ao baixar {url}: {e}")
        return None

    # Valida extensão suportada
    EXTENSOES_SUPORTADAS = {'.csv', '.xlsx', '.json', '.zip', '.parquet', '.h5', '.hdf5', '.nc'}
    ext = os.path.splitext(caminho_arquivo)[1].lower()
    if ext not in EXTENSOES_SUPORTADAS:
        os.remove(caminho_arquivo)
        return None

    # Descompacta ZIP automaticamente
    if caminho_arquivo.endswith('.zip'):
        try:
            with zipfile.ZipFile(caminho_arquivo, 'r') as zip_ref:
                zip_ref.extractall(destino_pasta)
            os.remove(caminho_arquivo)
        except Exception as e:
            print(f"[downloader] Erro descompactando {nome_arquivo}: {e}")

    return caminho_arquivo
