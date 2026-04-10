# tests/integration/test_kaggle_integration.py
"""
Testes de integração para o conector Kaggle.
Requerem KAGGLE_USERNAME e KAGGLE_KEY no ambiente.
Rodar com: pytest tests/integration/test_kaggle_integration.py -v
"""
import os
import pytest

pytestmark = pytest.mark.integration

# Dataset público pequeno e estável usado como fixture de teste
DATASET_REF = "uciml/iris"   # ~4KB, licença CC0


@pytest.fixture(scope="module")
def destino_tmp(tmp_path_factory):
    return str(tmp_path_factory.mktemp("kaggle_dl"))


class TestKagleBusca:
    def test_credenciais_presentes(self):
        assert os.environ.get("KAGGLE_USERNAME"), "KAGGLE_USERNAME não definido no .env"
        assert os.environ.get("KAGGLE_KEY"), "KAGGLE_KEY não definido no .env"

    def test_busca_retorna_lista_nao_vazia(self):
        from kaggle_source import buscar_datasets_kaggle
        resultado = buscar_datasets_kaggle("iris classification", max_results=5)
        assert isinstance(resultado, list)
        assert len(resultado) > 0, "Kaggle não retornou nenhum dataset"

    def test_resultado_tem_campos_obrigatorios(self):
        from kaggle_source import buscar_datasets_kaggle
        resultado = buscar_datasets_kaggle("iris", max_results=3)
        assert len(resultado) > 0
        campos = {'fonte', 'titulo', 'ref', 'url', 'downloads', 'votos', 'licenca'}
        for ds in resultado:
            assert campos.issubset(ds.keys()), f"Dataset sem campos esperados: {ds}"

    def test_url_tem_formato_correto(self):
        from kaggle_source import buscar_datasets_kaggle
        resultado = buscar_datasets_kaggle("iris", max_results=3)
        for ds in resultado:
            assert ds['url'].startswith("https://www.kaggle.com/datasets/")

    def test_downloads_e_votos_sao_numericos(self):
        from kaggle_source import buscar_datasets_kaggle
        resultado = buscar_datasets_kaggle("iris", max_results=3)
        for ds in resultado:
            assert isinstance(ds['downloads'], int)
            assert isinstance(ds['votos'], int)


class TestKaggleDownload:
    def test_download_dataset_pequeno(self, destino_tmp):
        from kaggle_source import baixar_dataset_kaggle
        arquivos = baixar_dataset_kaggle(DATASET_REF, destino=destino_tmp)
        assert len(arquivos) > 0, f"Nenhum arquivo baixado de {DATASET_REF}"

    def test_arquivo_baixado_existe_em_disco(self, destino_tmp):
        from kaggle_source import baixar_dataset_kaggle
        arquivos = baixar_dataset_kaggle(DATASET_REF, destino=destino_tmp)
        for caminho in arquivos:
            assert os.path.exists(caminho), f"Arquivo não encontrado: {caminho}"
            assert os.path.getsize(caminho) > 0, f"Arquivo vazio: {caminho}"

    def test_arquivo_baixado_e_analisavel(self, destino_tmp):
        from kaggle_source import baixar_dataset_kaggle
        from analyzer import analisar_dataset
        arquivos = baixar_dataset_kaggle(DATASET_REF, destino=destino_tmp)
        csvs = [f for f in arquivos if f.endswith('.csv')]
        assert len(csvs) > 0, "Nenhum CSV encontrado após download"
        resumo = analisar_dataset(csvs[0], query="iris classification")
        assert resumo is not None
        assert resumo['linhas'] > 0
        assert resumo['colunas'] > 0
        assert resumo['qualidade'] > 0
