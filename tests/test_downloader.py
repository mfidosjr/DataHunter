# tests/test_downloader.py
import os
import pytest
import zipfile
import tempfile
from unittest.mock import patch, MagicMock

import httpx

from downloader import limpar_nome_arquivo, baixar_arquivo


class TestLimparNomeArquivo:
    def test_extrai_nome_da_url(self):
        assert limpar_nome_arquivo('https://exemplo.com/dados.csv') == 'dados.csv'

    def test_remove_query_string(self):
        nome = limpar_nome_arquivo('https://exemplo.com/dados.csv?token=abc')
        assert '?' not in nome
        assert 'token' not in nome

    def test_substitui_caracteres_invalidos(self):
        nome = limpar_nome_arquivo('https://exemplo.com/dados com espaço.csv')
        assert ' ' not in nome

    def test_url_sem_nome_retorna_fallback(self):
        assert limpar_nome_arquivo('https://exemplo.com/') == 'arquivo_baixado'


class TestBaixarArquivo:
    def _mock_response(self, status=200, content=b'a,b\n1,2\n', content_type='text/csv'):
        resp = MagicMock(spec=httpx.Response)
        resp.status_code = status
        resp.content = content
        resp.headers = {'content-type': content_type}
        return resp

    def test_download_bem_sucedido_cria_arquivo(self, tmp_path):
        with patch('downloader._get_com_retry', return_value=self._mock_response()):
            caminho = baixar_arquivo('https://exemplo.com/dados.csv', destino_pasta=str(tmp_path))
            assert caminho is not None
            assert os.path.exists(caminho)

    def test_status_404_retorna_none(self, tmp_path):
        with patch('downloader._get_com_retry', return_value=self._mock_response(status=404)):
            assert baixar_arquivo('https://exemplo.com/dados.csv', destino_pasta=str(tmp_path)) is None

    def test_html_retorna_none(self, tmp_path):
        with patch('downloader._get_com_retry', return_value=self._mock_response(content_type='text/html')):
            assert baixar_arquivo('https://exemplo.com/dados.csv', destino_pasta=str(tmp_path)) is None

    def test_zip_e_descompactado(self, tmp_path):
        # Cria um ZIP em memória com um CSV dentro
        zip_buf = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
        with zipfile.ZipFile(zip_buf.name, 'w') as zf:
            zf.writestr('dados.csv', 'a,b\n1,2\n')
        with open(zip_buf.name, 'rb') as f:
            zip_content = f.read()
        os.unlink(zip_buf.name)

        with patch('downloader._get_com_retry', return_value=self._mock_response(content=zip_content, content_type='application/zip')):
            caminho = baixar_arquivo('https://exemplo.com/arquivo.zip', destino_pasta=str(tmp_path))
            # ZIP original removido após extração
            assert not os.path.exists(str(tmp_path / 'arquivo.zip'))
            # CSV extraído presente
            assert os.path.exists(str(tmp_path / 'dados.csv'))

    def test_falha_de_rede_retorna_none(self, tmp_path):
        with patch('downloader._get_com_retry', side_effect=httpx.NetworkError('timeout')):
            assert baixar_arquivo('https://exemplo.com/dados.csv', destino_pasta=str(tmp_path)) is None
