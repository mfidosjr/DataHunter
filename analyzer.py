# analyzer.py
import pandas as pd
import os
import re


def ler_dataset(filepath):
    """Lê o dataset independente do tipo, incluindo HDF5 e NetCDF."""
    if filepath.endswith('.csv'):
        return pd.read_csv(filepath, encoding='utf-8', low_memory=False)
    elif filepath.endswith('.xlsx'):
        return pd.read_excel(filepath)
    elif filepath.endswith('.json'):
        return pd.read_json(filepath)
    elif filepath.endswith('.parquet'):
        return pd.read_parquet(filepath)
    elif filepath.endswith(('.h5', '.hdf5')):
        try:
            import h5py
            with h5py.File(filepath, 'r') as f:
                # Pega o primeiro dataset folha encontrado
                frames = []
                def _visit(name, obj):
                    if isinstance(obj, h5py.Dataset) and len(obj.shape) <= 2:
                        try:
                            frames.append(pd.DataFrame(obj[:]))
                        except Exception:
                            pass
                f.visititems(_visit)
                return frames[0] if frames else None
        except Exception as e:
            print(f"[analyzer] HDF5 leitura falhou em {filepath}: {e}")
            return None
    elif filepath.endswith('.nc'):
        try:
            import xarray as xr
            ds = xr.open_dataset(filepath)
            return ds.to_dataframe().reset_index()
        except Exception as e:
            print(f"[analyzer] NetCDF leitura falhou em {filepath}: {e}")
            return None
    else:
        return None


def _score_qualidade(linhas, colunas, percentual_nulos):
    """Score técnico de qualidade (0–100)."""
    import math
    base = math.log1p(linhas) * 10 + colunas * 2
    penalidade = percentual_nulos * 0.5
    return round(max(0, min(100, base - penalidade)), 1)


def _score_relevancia_tokens(colunas_df, query):
    """Score de relevância por sobreposição de tokens (0–100). Fallback rápido."""
    if not query:
        return 0.0
    stopwords = {'', 'de', 'do', 'da', 'no', 'na', 'em', 'e', 'a', 'o', 'the', 'of', 'in', 'for'}
    tokens_query = set(re.split(r'\W+', query.lower())) - stopwords
    tokens_colunas = set()
    for col in colunas_df:
        tokens_colunas.update(re.split(r'\W+', str(col).lower()))
    if not tokens_query:
        return 0.0
    matches = tokens_query & tokens_colunas
    return round(min(100, (len(matches) / len(tokens_query)) * 100), 1)


def _score_relevancia_ia(titulo: str, colunas, descricao: str, query: str) -> float | None:
    """
    Semantic relevance score via Groq (0–100).
    Returns None if Groq is unavailable — caller falls back to token score.
    """
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key or not query:
        return None
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        colunas_str = ", ".join(str(c) for c in list(colunas)[:30])
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=10,
            messages=[{
                "role": "user",
                "content": (
                    f"Rate the relevance of this dataset for the query: '{query}'\n"
                    f"Dataset title: {titulo}\n"
                    f"Columns: {colunas_str}\n"
                    f"Description: {descricao[:200]}\n\n"
                    "Reply with a single integer from 0 to 100. Nothing else."
                )
            }],
        )
        score = int(re.search(r'\d+', response.choices[0].message.content).group())
        return float(min(100, max(0, score)))
    except Exception:
        return None


def analisar_dataset(filepath, query=None, titulo="", descricao=""):
    """
    Analisa o dataset: linhas, colunas, nulos, tipos.
    Scores retornados:
      - qualidade:    completude e tamanho (estrutural)
      - relevancia:   sobreposição de tokens query ↔ colunas (rápido)
      - relevancia_ia: score semântico via Groq (quando disponível)
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
            "numerico":   len(df.select_dtypes(include=['number']).columns),
            "categorico": len(df.select_dtypes(include=['object', 'category']).columns),
            "datas":      len(df.select_dtypes(include=['datetime']).columns),
        }

        rel_tokens = _score_relevancia_tokens(df.columns, query)
        rel_ia = _score_relevancia_ia(titulo, df.columns, descricao, query)

        resumo = {
            'arquivo':      os.path.basename(filepath),
            'linhas':       linhas,
            'colunas':      colunas,
            '%_nulos':      round(percentual_nulos, 2),
            'tipos_detectados': tipos,
            'qualidade':    _score_qualidade(linhas, colunas, percentual_nulos),
            'relevancia':   rel_tokens,
            'relevancia_ia': rel_ia if rel_ia is not None else rel_tokens,
            'caminho':      filepath,
        }
        return resumo

    except Exception as e:
        print(f"Erro ao analisar {filepath}: {e}")
        return None
