# analyzer.py
import pandas as pd
import os
import re


def ler_dataset(filepath):
    """Lê o dataset independente do tipo."""
    if filepath.endswith('.csv'):
        return pd.read_csv(filepath, encoding='utf-8', low_memory=False)
    elif filepath.endswith('.xlsx'):
        return pd.read_excel(filepath)
    elif filepath.endswith('.json'):
        return pd.read_json(filepath)
    elif filepath.endswith('.parquet'):
        return pd.read_parquet(filepath)
    else:
        return None


def _score_qualidade(linhas, colunas, percentual_nulos):
    """
    Score técnico de qualidade (0–100).
    Recompensa datasets grandes e com muitas colunas; penaliza nulos.
    """
    import math
    base = math.log1p(linhas) * 10 + colunas * 2
    penalidade = percentual_nulos * 0.5
    return round(max(0, min(100, base - penalidade)), 1)


def _score_relevancia(colunas_df, query):
    """
    Score de relevância semântica (0–100).
    Calcula sobreposição entre tokens da query e nomes de colunas do dataset.
    """
    if not query:
        return 0.0

    tokens_query = set(re.split(r'\W+', query.lower())) - {'', 'de', 'do', 'da', 'no', 'na', 'em', 'e', 'a', 'o'}
    tokens_colunas = set()
    for col in colunas_df:
        tokens_colunas.update(re.split(r'\W+', str(col).lower()))

    if not tokens_query:
        return 0.0

    matches = tokens_query & tokens_colunas
    score = (len(matches) / len(tokens_query)) * 100
    return round(min(100, score), 1)


def analisar_dataset(filepath, query=None):
    """
    Analisa o dataset: linhas, colunas, nulos, tipos de dados.
    Retorna dois scores separados:
      - qualidade: completude e tamanho do dataset
      - relevancia: sobreposição semântica com a query do usuário
    """
    try:
        df = ler_dataset(filepath)
        if df is None:
            return None

        if df.shape[0] < 10 or df.shape[1] == 0:
            return None

        linhas = df.shape[0]
        colunas = df.shape[1]
        percentual_nulos = (df.isnull().sum().sum() / (linhas * colunas)) * 100

        tipos = {
            "numerico": len(df.select_dtypes(include=['number']).columns),
            "categorico": len(df.select_dtypes(include=['object', 'category']).columns),
            "datas": len(df.select_dtypes(include=['datetime']).columns)
        }

        resumo = {
            'arquivo': os.path.basename(filepath),
            'linhas': linhas,
            'colunas': colunas,
            '%_nulos': round(percentual_nulos, 2),
            'tipos_detectados': tipos,
            'qualidade': _score_qualidade(linhas, colunas, percentual_nulos),
            'relevancia': _score_relevancia(df.columns, query),
            'caminho': filepath
        }
        return resumo

    except Exception as e:
        print(f"Erro ao analisar {filepath}: {e}")
        return None
