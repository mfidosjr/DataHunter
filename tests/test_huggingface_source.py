# tests/test_huggingface_source.py
import pytest
from unittest.mock import patch, MagicMock

from huggingface_source import buscar_datasets_hf


def _make_ds(id='owner/dataset', downloads=50, likes=5, tags=None):
    ds = MagicMock()
    ds.id = id
    ds.downloads = downloads
    ds.likes = likes
    ds.tags = tags or ['license:apache-2.0']
    return ds


class TestBuscarDatasetsHF:
    def test_retorna_lista_de_dicts(self):
        with patch('huggingface_hub.HfApi') as MockApi:
            MockApi.return_value.list_datasets.return_value = [_make_ds()]
            resultado = buscar_datasets_hf('water quality')
            assert isinstance(resultado, list)
            assert resultado[0]['fonte'] == 'huggingface'

    def test_campos_obrigatorios_presentes(self):
        with patch('huggingface_hub.HfApi') as MockApi:
            MockApi.return_value.list_datasets.return_value = [_make_ds()]
            resultado = buscar_datasets_hf('test')
            assert {'titulo', 'ref', 'url', 'downloads', 'likes', 'licenca'}.issubset(resultado[0])

    def test_extrai_licenca_das_tags(self):
        with patch('huggingface_hub.HfApi') as MockApi:
            MockApi.return_value.list_datasets.return_value = [_make_ds(tags=['license:mit'])]
            resultado = buscar_datasets_hf('test')
            assert resultado[0]['licenca'] == 'mit'

    def test_sem_licenca_retorna_desconhecida(self):
        with patch('huggingface_hub.HfApi') as MockApi:
            MockApi.return_value.list_datasets.return_value = [_make_ds(tags=['task:classification'])]
            resultado = buscar_datasets_hf('test')
            assert resultado[0]['licenca'] == 'desconhecida'

    def test_erro_retorna_lista_vazia(self):
        with patch('huggingface_hub.HfApi', side_effect=Exception('API error')):
            resultado = buscar_datasets_hf('test')
            assert resultado == []
