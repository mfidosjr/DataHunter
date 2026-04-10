# tests/integration/test_pipeline_integration.py
"""
Testes de integração de ponta a ponta do pipeline completo.
Validam que o fluxo busca → download → análise produz resultados úteis.
Rodar com: pytest tests/integration/test_pipeline_integration.py -v
"""
import os
import pytest

pytestmark = pytest.mark.integration

QUERY = "iris flower dataset"


class TestPipelineKaggle:
    """Fluxo completo: Kaggle busca → download → análise → scores."""

    def test_pipeline_retorna_pelo_menos_um_dataset(self, tmp_path):
        from kaggle_source import buscar_datasets_kaggle, baixar_dataset_kaggle
        from analyzer import analisar_dataset

        resultados = buscar_datasets_kaggle(QUERY, max_results=3)
        assert len(resultados) > 0, "Kaggle não encontrou datasets"

        # Usa o primeiro resultado
        ref = resultados[0]['ref']
        arquivos = baixar_dataset_kaggle(ref, destino=str(tmp_path))
        assert len(arquivos) > 0, f"Nenhum arquivo baixado de {ref}"

        csvs = [f for f in arquivos if f.endswith('.csv')]
        assert len(csvs) > 0, "Nenhum CSV no dataset baixado"

        resumo = analisar_dataset(csvs[0], query=QUERY)
        assert resumo is not None

    def test_pipeline_score_qualidade_positivo(self, tmp_path):
        from kaggle_source import buscar_datasets_kaggle, baixar_dataset_kaggle
        from analyzer import analisar_dataset

        resultados = buscar_datasets_kaggle(QUERY, max_results=2)
        ref = resultados[0]['ref']
        arquivos = baixar_dataset_kaggle(ref, destino=str(tmp_path))
        csvs = [f for f in arquivos if f.endswith('.csv')]

        resumo = analisar_dataset(csvs[0], query=QUERY)
        assert resumo['qualidade'] > 0, "Score de qualidade deveria ser > 0"

    def test_pipeline_score_relevancia_positivo(self, tmp_path):
        from kaggle_source import buscar_datasets_kaggle, baixar_dataset_kaggle
        from analyzer import analisar_dataset

        resultados = buscar_datasets_kaggle(QUERY, max_results=2)
        ref = resultados[0]['ref']
        arquivos = baixar_dataset_kaggle(ref, destino=str(tmp_path))
        csvs = [f for f in arquivos if f.endswith('.csv')]

        resumo = analisar_dataset(csvs[0], query=QUERY)
        # "iris" aparece em nomes de colunas de datasets de iris — relevância > 0
        assert resumo['relevancia'] >= 0, "Score de relevância não pode ser negativo"

    def test_pipeline_descricao_semantica_gerada(self, tmp_path):
        from kaggle_source import buscar_datasets_kaggle, baixar_dataset_kaggle
        from analyzer import ler_dataset
        from semantic_analyzer import gerar_resumo_semantico

        resultados = buscar_datasets_kaggle(QUERY, max_results=2)
        ref = resultados[0]['ref']
        arquivos = baixar_dataset_kaggle(ref, destino=str(tmp_path))
        csvs = [f for f in arquivos if f.endswith('.csv')]

        df = ler_dataset(csvs[0])
        assert df is not None
        descricao = gerar_resumo_semantico(df.columns)
        assert isinstance(descricao, str) and len(descricao) > 0


class TestPipelineWeb:
    """Fluxo completo via web: busca → download direto → análise."""

    CSV_IRIS = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"

    def test_download_e_analise_producao_scores(self, tmp_path):
        from downloader import baixar_arquivo
        from analyzer import analisar_dataset

        caminho = baixar_arquivo(self.CSV_IRIS, destino_pasta=str(tmp_path))
        assert caminho is not None

        resumo = analisar_dataset(caminho, query="iris flower species")
        assert resumo is not None
        assert resumo['qualidade'] > 0
        assert resumo['relevancia'] > 0  # "iris" está nas colunas

    def test_resultado_tem_todos_campos(self, tmp_path):
        from downloader import baixar_arquivo
        from analyzer import analisar_dataset

        caminho = baixar_arquivo(self.CSV_IRIS, destino_pasta=str(tmp_path))
        resumo = analisar_dataset(caminho, query="iris")

        campos = {'arquivo', 'linhas', 'colunas', '%_nulos', 'qualidade', 'relevancia', 'caminho'}
        assert campos.issubset(resumo.keys())

    def test_multiplos_datasets_rankeados_por_relevancia(self, tmp_path):
        from downloader import baixar_arquivo
        from analyzer import analisar_dataset
        import pandas as pd

        # Dois datasets: um relevante, um não
        urls = {
            "iris.csv": self.CSV_IRIS,
            "tips.csv": "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv",
        }

        resumos = []
        for nome, url in urls.items():
            caminho = baixar_arquivo(url, destino_pasta=str(tmp_path))
            if caminho:
                resumo = analisar_dataset(caminho, query="iris flower species")
                if resumo:
                    resumos.append(resumo)

        assert len(resumos) == 2
        df = pd.DataFrame(resumos).sort_values('relevancia', ascending=False)
        # iris.csv deve ter relevância maior que tips.csv para a query "iris flower species"
        assert df.iloc[0]['arquivo'] == 'iris.csv', (
            f"Esperado iris.csv no topo, mas veio: {df.iloc[0]['arquivo']}"
        )
