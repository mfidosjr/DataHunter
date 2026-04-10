# tests/test_search.py
import pytest
from unittest.mock import patch, MagicMock

from search import buscar_paginas, FONTES_PREFERIDAS


class TestBuscarPaginas:
    def _mock_ddgs(self, urls):
        """Retorna um context manager que simula o DDGS com os resultados dados."""
        resultados = [{'href': u} for u in urls]
        mock = MagicMock()
        mock.__enter__ = MagicMock(return_value=mock)
        mock.__exit__ = MagicMock(return_value=False)
        mock.text = MagicMock(return_value=resultados)
        return mock

    def test_retorna_lista_de_urls(self):
        urls = ['https://data.gov/dataset1', 'https://exemplo.com/dados']
        with patch('search.DDGS', return_value=self._mock_ddgs(urls)):
            resultado = buscar_paginas('water quality')
            assert isinstance(resultado, list)
            assert len(resultado) > 0

    def test_fontes_preferidas_vem_primeiro(self):
        urls = ['https://exemplo.com/dados', 'https://data.gov/dataset1']
        with patch('search.DDGS', return_value=self._mock_ddgs(urls)):
            resultado = buscar_paginas('water quality')
            idx_gov = next((i for i, u in enumerate(resultado) if 'data.gov' in u), None)
            idx_outro = next((i for i, u in enumerate(resultado) if 'exemplo.com' in u), None)
            assert idx_gov is not None and idx_outro is not None
            assert idx_gov < idx_outro

    def test_remove_duplicatas(self):
        urls = ['https://data.gov/dataset1'] * 5
        with patch('search.DDGS', return_value=self._mock_ddgs(urls)):
            resultado = buscar_paginas('water quality')
            assert len(resultado) == len(set(resultado))

    def test_erro_na_busca_retorna_lista_vazia(self):
        with patch('search.DDGS', side_effect=Exception('network error')):
            resultado = buscar_paginas('water quality')
            assert resultado == []
