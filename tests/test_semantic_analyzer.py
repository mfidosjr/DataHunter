# tests/test_semantic_analyzer.py
import pytest
from unittest.mock import patch, MagicMock

from semantic_analyzer import (
    tokenizar_coluna,
    analisar_semantica_das_colunas,
    _resumo_por_keywords,
    gerar_resumo_semantico,
)


class TestTokenizarColuna:
    def test_separa_por_underline(self):
        assert 'agua' in tokenizar_coluna('qualidade_agua')

    def test_separa_por_espaco(self):
        assert 'agua' in tokenizar_coluna('qualidade agua')

    def test_converte_para_minusculo(self):
        tokens = tokenizar_coluna('TEMPERATURA')
        assert 'temperatura' in tokens

    def test_remove_tokens_vazios(self):
        tokens = tokenizar_coluna('col__nome')
        assert '' not in tokens


class TestAnalisarSemantica:
    def test_detecta_categoria_qualidade_agua(self):
        tags = analisar_semantica_das_colunas(['ph', 'turbidez', 'temperatura'])
        assert 'qualidade_agua' in tags

    def test_detecta_categoria_financeiro(self):
        tags = analisar_semantica_das_colunas(['receita', 'despesa', 'custo'])
        assert 'financeiro' in tags

    def test_colunas_sem_match_retorna_lista_vazia(self):
        tags = analisar_semantica_das_colunas(['coluna_x', 'coluna_y'])
        assert tags == []

    def test_multiplas_categorias(self):
        tags = analisar_semantica_das_colunas(['ph', 'escola', 'receita'])
        assert len(tags) >= 3


class TestResumoPorKeywords:
    def test_retorna_string_nao_vazia(self):
        result = _resumo_por_keywords(['ph', 'turbidez'])
        assert isinstance(result, str) and len(result) > 0

    def test_sem_match_retorna_indefinido(self):
        result = _resumo_por_keywords(['coluna_xyz'])
        assert 'indefinido' in result.lower()


class TestGerarResumoSemantico:
    def test_sem_api_key_usa_keywords(self):
        with patch.dict('os.environ', {'GROQ_API_KEY': ''}):
            result = gerar_resumo_semantico(['ph', 'temperatura'])
            assert 'qualidade_agua' in result

    def test_com_api_key_chama_groq(self):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = 'Dataset sobre qualidade da água.'

        with patch.dict('os.environ', {'GROQ_API_KEY': 'fake_key'}):
            with patch('groq.Groq') as MockGroq:
                MockGroq.return_value.chat.completions.create.return_value = mock_response
                result = gerar_resumo_semantico(['ph', 'temperatura'])
                assert result == 'Dataset sobre qualidade da água.'

    def test_groq_com_falha_faz_fallback_para_keywords(self):
        with patch.dict('os.environ', {'GROQ_API_KEY': 'fake_key'}):
            with patch('groq.Groq', side_effect=Exception('API error')):
                result = gerar_resumo_semantico(['ph', 'temperatura'])
                assert isinstance(result, str) and len(result) > 0
