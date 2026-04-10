# tests/test_kaggle_source.py
import sys
import pytest
from unittest.mock import MagicMock, patch

# Injeta um mock do módulo kaggle antes de qualquer import real,
# evitando o authenticate() que o pacote chama na importação.
_kaggle_mock = MagicMock()
sys.modules.setdefault('kaggle', _kaggle_mock)
sys.modules.setdefault('kaggle.api', _kaggle_mock.api)

from kaggle_source import buscar_datasets_kaggle


def _make_ds(ref='owner/slug', title='My Dataset', total_bytes=1024,
             download_count=100, vote_count=10, license_name='CC0', tags=None):
    ds = MagicMock()
    ds.ref = ref
    ds.title = title
    ds.total_bytes = total_bytes
    ds.download_count = download_count
    ds.vote_count = vote_count
    ds.license_name = license_name
    ds.tags = tags or []
    return ds


class TestBuscarDatasetsKaggle:
    def setup_method(self):
        """Reseta o mock antes de cada teste."""
        _kaggle_mock.reset_mock()
        _kaggle_mock.api.authenticate.return_value = None
        _kaggle_mock.api.dataset_list.return_value = []

    def test_retorna_lista_de_dicts(self):
        _kaggle_mock.api.dataset_list.return_value = [_make_ds()]
        resultado = buscar_datasets_kaggle('water quality')
        assert isinstance(resultado, list)
        assert resultado[0]['fonte'] == 'kaggle'

    def test_campos_obrigatorios_presentes(self):
        _kaggle_mock.api.dataset_list.return_value = [_make_ds()]
        resultado = buscar_datasets_kaggle('test')
        assert {'titulo', 'ref', 'url', 'downloads', 'votos', 'licenca'}.issubset(resultado[0])

    def test_respeita_max_results(self):
        _kaggle_mock.api.dataset_list.return_value = [_make_ds(ref=f'owner/ds{i}') for i in range(20)]
        resultado = buscar_datasets_kaggle('test', max_results=5)
        assert len(resultado) <= 5

    def test_erro_de_autenticacao_retorna_lista_vazia(self):
        _kaggle_mock.api.authenticate.side_effect = Exception('401 Unauthorized')
        resultado = buscar_datasets_kaggle('test')
        assert resultado == []
