# tests/test_analyzer.py
import os
import pytest
import pandas as pd
import tempfile

from analyzer import _score_qualidade, _score_relevancia_tokens as _score_relevancia, analisar_dataset


class TestScoreQualidade:
    def test_dataset_grande_recebe_score_alto(self):
        score = _score_qualidade(linhas=100_000, colunas=20, percentual_nulos=0)
        assert score > 50

    def test_dataset_pequeno_recebe_score_baixo(self):
        score = _score_qualidade(linhas=50, colunas=3, percentual_nulos=0)
        assert score < 50

    def test_muitos_nulos_penaliza_score(self):
        sem_nulos = _score_qualidade(1000, 10, percentual_nulos=0)
        com_nulos = _score_qualidade(1000, 10, percentual_nulos=80)
        assert sem_nulos > com_nulos

    def test_score_entre_0_e_100(self):
        for linhas, colunas, nulos in [(10, 1, 99), (10**7, 100, 0)]:
            score = _score_qualidade(linhas, colunas, nulos)
            assert 0 <= score <= 100


class TestScoreRelevancia:
    def test_colunas_identicas_a_query_retorna_100(self):
        score = _score_relevancia(['water', 'quality'], query='water quality')
        assert score == 100.0

    def test_sem_sobreposicao_retorna_0(self):
        score = _score_relevancia(['preco', 'vendas'], query='water quality')
        assert score == 0.0

    def test_sobreposicao_parcial(self):
        score = _score_relevancia(['water', 'temperatura', 'ph'], query='water quality')
        assert 0 < score < 100

    def test_query_vazia_retorna_0(self):
        assert _score_relevancia(['coluna_a'], query='') == 0.0

    def test_query_none_retorna_0(self):
        assert _score_relevancia(['coluna_a'], query=None) == 0.0


class TestAnalisarDataset:
    def _csv_tmp(self, df):
        """Cria um CSV temporário e retorna o caminho."""
        f = tempfile.NamedTemporaryFile(suffix='.csv', delete=False, mode='w')
        df.to_csv(f.name, index=False)
        f.close()
        return f.name

    def test_retorna_resumo_com_campos_esperados(self):
        df = pd.DataFrame({'a': range(20), 'b': range(20)})
        caminho = self._csv_tmp(df)
        try:
            resumo = analisar_dataset(caminho)
            assert resumo is not None
            assert {'arquivo', 'linhas', 'colunas', '%_nulos', 'qualidade', 'relevancia', 'caminho'}.issubset(resumo)
        finally:
            os.unlink(caminho)

    def test_dataset_com_menos_de_10_linhas_retorna_none(self):
        df = pd.DataFrame({'a': range(5)})
        caminho = self._csv_tmp(df)
        try:
            assert analisar_dataset(caminho) is None
        finally:
            os.unlink(caminho)

    def test_relevancia_com_query_passada(self):
        df = pd.DataFrame({'water': range(20), 'quality': range(20), 'ph': range(20)})
        caminho = self._csv_tmp(df)
        try:
            resumo = analisar_dataset(caminho, query='water quality')
            assert resumo['relevancia'] > 0
        finally:
            os.unlink(caminho)

    def test_arquivo_inexistente_retorna_none(self):
        assert analisar_dataset('/tmp/nao_existe.csv') is None
