# tests/integration/test_web_integration.py
"""
Testes de integração para busca web (DuckDuckGo) e downloader.
Rodar com: pytest tests/integration/test_web_integration.py -v
"""
import os
import pytest

pytestmark = pytest.mark.integration

# URL de um CSV público pequeno e estável para testar o downloader
CSV_PUBLICO = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"


class TestWebBusca:
    def test_busca_retorna_urls(self):
        from search import buscar_paginas
        resultado = buscar_paginas("iris dataset csv download", max_results=10)
        assert isinstance(resultado, list)
        assert len(resultado) > 0, "DuckDuckGo não retornou resultados"

    def test_resultado_sao_urls_validas(self):
        from search import buscar_paginas
        resultado = buscar_paginas("open data csv", max_results=5)
        for url in resultado:
            assert url.startswith("http"), f"URL inválida: {url}"

    def test_fontes_preferidas_priorizadas(self):
        from search import buscar_paginas, FONTES_PREFERIDAS
        resultado = buscar_paginas("water quality dataset", max_results=30)
        # Verifica que existe pelo menos uma fonte preferida nos primeiros resultados
        primeiros = resultado[:10]
        tem_preferida = any(
            any(fonte in url for fonte in FONTES_PREFERIDAS)
            for url in primeiros
        )
        assert tem_preferida, "Nenhuma fonte preferida nos primeiros 10 resultados"


class TestDownloader:
    def test_download_csv_publico(self, tmp_path):
        from downloader import baixar_arquivo
        caminho = baixar_arquivo(CSV_PUBLICO, destino_pasta=str(tmp_path))
        assert caminho is not None, "Download retornou None"
        assert os.path.exists(caminho)
        assert os.path.getsize(caminho) > 0

    def test_arquivo_baixado_e_csv_valido(self, tmp_path):
        from downloader import baixar_arquivo
        import pandas as pd
        caminho = baixar_arquivo(CSV_PUBLICO, destino_pasta=str(tmp_path))
        assert caminho is not None
        df = pd.read_csv(caminho)
        assert df.shape[0] > 0
        assert df.shape[1] > 0

    def test_url_invalida_retorna_none(self, tmp_path):
        from downloader import baixar_arquivo
        resultado = baixar_arquivo("https://nao-existe-mesmo.xyz/dados.csv", destino_pasta=str(tmp_path))
        assert resultado is None
