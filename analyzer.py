# analyzer.py
import pandas as pd

def analisar_dataset(filepath):
    try:
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
        score = (linhas * 0.3) + (colunas * 0.5) - (percentual_nulos * 0.2)

        resumo = {
            'arquivo': filepath.split('/')[-1],
            'linhas': linhas,
            'colunas': colunas,
            '%_nulos': percentual_nulos,
            'pontuacao': score,
            'caminho': filepath
        }
        return resumo
    except:
        return None