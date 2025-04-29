# analyzer.py
import pandas as pd
import os

def ler_dataset(filepath):
    """Lê o dataset independente do tipo."""
    if filepath.endswith('.csv'):
        return pd.read_csv(filepath, encoding='utf-8', low_memory=False)
    elif filepath.endswith('.xlsx'):
        return pd.read_excel(filepath)
    elif filepath.endswith('.json'):
        return pd.read_json(filepath)
    else:
        return None

def analisar_dataset(filepath):
    """Analisa o dataset: linhas, colunas, nulos, tipos de dados e score de qualidade."""
    try:
        df = ler_dataset(filepath)
        if df is None:
            return None

        if df.shape[0] < 10 or df.shape[1] == 0:
            return None

        linhas = df.shape[0]
        colunas = df.shape[1]
        percentual_nulos = (df.isnull().sum().sum() / (linhas * colunas)) * 100

        # 🔵 Inferência mais detalhada de tipo de dados
        tipos = {
            "numerico": len(df.select_dtypes(include=['number']).columns),
            "categorico": len(df.select_dtypes(include=['object', 'category']).columns),
            "datas": len(df.select_dtypes(include=['datetime']).columns)
        }

        # 🔵 Score de qualidade ajustado
        score = (linhas * 0.3) + (colunas * 0.5) - (percentual_nulos * 0.2)

        resumo = {
            'arquivo': os.path.basename(filepath),
            'linhas': linhas,
            'colunas': colunas,
            '%_nulos': round(percentual_nulos, 2),
            'tipos_detectados': tipos,
            'pontuacao': round(score, 2),
            'caminho': filepath
        }
        return resumo

    except Exception as e:
        print(f"Erro ao analisar {filepath}: {e}")
        return None
