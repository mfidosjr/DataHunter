# downloader.py
import os
import requests
import zipfile
import time

def baixar_arquivo(url, destino_pasta='datasets', max_tentativas=2):
    """Tenta baixar um arquivo de dados. Se for ZIP, descompacta automaticamente."""
    os.makedirs(destino_pasta, exist_ok=True)
    nome_arquivo = url.split("/")[-1].split("?")[0]
    caminho_arquivo = os.path.join(destino_pasta, nome_arquivo)

    tentativas = 0
    sucesso = False

    while tentativas < max_tentativas and not sucesso:
        try:
            resposta = requests.get(url, stream=True, timeout=15)
            if resposta.status_code == 200 and 'text/html' not in resposta.headers.get('Content-Type', ''):
                with open(caminho_arquivo, 'wb') as f:
                    for chunk in resposta.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                sucesso = True
            else:
                tentativas += 1
                time.sleep(2)
        except Exception as e:
            tentativas += 1
            time.sleep(2)

    if not sucesso:
        return None

    # Se for ZIP, descompacta
    if caminho_arquivo.endswith('.zip'):
        try:
            with zipfile.ZipFile(caminho_arquivo, 'r') as zip_ref:
                zip_ref.extractall(destino_pasta)
            os.remove(caminho_arquivo)  # Remove o zip após extração
        except Exception as e:
            print(f"Erro descompactando {nome_arquivo}: {e}")

    return caminho_arquivo
