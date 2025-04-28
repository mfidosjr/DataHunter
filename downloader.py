# analyzer.py
import pandas as pd
import os

def analisar_dataset(filepath):
    """Analisa o dataset: linhas, colunas, nulos, tipos de dados e score de qualidade."""
    try:
        # Detecta tipo de arquivo
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath, encoding='utf-8', low_memory=False)
        elif filepath.endswith('.xlsx'):
            df = pd.read_excel(filepath)
        elif filepath.endswith('.json'):
            df = pd.read_json(filepath)
        else:
            return None
        
        if df.shape[0] < 10 or df.shape[1] == 0:
            return None

        linhas = df.shape[0]
        colunas = df.shape[1]
        percentual_nulos = (df.isnull().sum().sum() / (linhas * colunas)) * 100

        # 🔵 Nova parte: Inferência de tipo de dados
        tipos = df.dtypes.value_counts().to_dict()
        tipos_formatados = {str(k): int(v) for k, v in tipos.items()}

        # 🔵 Score de qualidade: baseado em quantidade de dados e poucos nulos
        score = (linhas * 0.3) + (colunas * 0.5) - (percentual_nulos * 0.2)

        resumo = {
            'arquivo': os.path.basename(filepath),
            'linhas': linhas,
            'colunas': colunas,
            '%_nulos': round(percentual_nulos, 2),
            'tipos_detectados': tipos_formatados,
            'pontuacao': round(score, 2),
            'caminho': filepath
        }
        return resumo

    except Exception as e:
        print(f"Erro ao analisar {filepath}: {e}")
        return None
