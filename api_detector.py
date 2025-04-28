# api_detector.py
import requests
import pandas as pd

def detectar_apis_na_pagina(pagina_url):
    """Tenta detectar possíveis APIs JSON relacionadas à página."""
    apis_detectadas = []

    # Heurística simples: tentar variantes conhecidas
    possiveis_endpoints = [
        pagina_url.replace('html', 'json'),
        pagina_url.replace('/view/', '/api/'),
        pagina_url.replace('/pages/', '/data/'),
        pagina_url + '/data.json',
        pagina_url + '.json'
    ]

    for endpoint in possiveis_endpoints:
        try:
            resposta = requests.get(endpoint, timeout=10)
            if resposta.status_code == 200 and 'application/json' in resposta.headers.get('Content-Type', ''):
                apis_detectadas.append(endpoint)
        except Exception:
            continue

    return apis_detectadas

def baixar_dados_da_api(api_url, destino_pasta='datasets', nome_base='dados_api'):
    """Baixa dados JSON de um endpoint e salva como CSV."""
    try:
        os.makedirs(destino_pasta, exist_ok=True)
        resposta = requests.get(api_url, timeout=10)
        if resposta.status_code != 200:
            return None

        dados = resposta.json()

        # Tentativa: tratar como lista ou dict
        if isinstance(dados, list):
            df = pd.DataFrame(dados)
        elif isinstance(dados, dict):
            # Tenta encontrar a primeira lista no dicionário
            for k, v in dados.items():
                if isinstance(v, list):
                    df = pd.DataFrame(v)
                    break
            else:
                return None
        else:
            return None

        # Salvar CSV
        caminho = os.path.join(destino_pasta, f"{nome_base}.csv")
        df.to_csv(caminho, index=False)
        return caminho

    except Exception as e:
        print(f"Erro ao baixar dados da API {api_url}: {e}")
        return None
