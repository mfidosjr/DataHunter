# tests/integration/test_hf_integration.py
"""
Testes de integração para o conector Hugging Face.
Funcionam sem HF_TOKEN (datasets públicos).
Rodar com: pytest tests/integration/test_hf_integration.py -v
"""
import pytest

pytestmark = pytest.mark.integration


class TestHuggingFaceBusca:
    def test_busca_retorna_lista_nao_vazia(self):
        from huggingface_source import buscar_datasets_hf
        resultado = buscar_datasets_hf("iris", max_results=5)
        assert isinstance(resultado, list)
        assert len(resultado) > 0, "HuggingFace não retornou nenhum dataset"

    def test_resultado_tem_campos_obrigatorios(self):
        from huggingface_source import buscar_datasets_hf
        resultado = buscar_datasets_hf("sentiment analysis", max_results=3)
        campos = {'fonte', 'titulo', 'ref', 'url', 'downloads', 'likes', 'licenca'}
        for ds in resultado:
            assert campos.issubset(ds.keys())

    def test_fonte_e_huggingface(self):
        from huggingface_source import buscar_datasets_hf
        resultado = buscar_datasets_hf("text classification", max_results=3)
        for ds in resultado:
            assert ds['fonte'] == 'huggingface'

    def test_url_aponta_para_hf(self):
        from huggingface_source import buscar_datasets_hf
        resultado = buscar_datasets_hf("iris", max_results=3)
        for ds in resultado:
            assert "huggingface.co/datasets/" in ds['url']

    def test_downloads_e_likes_sao_numericos(self):
        from huggingface_source import buscar_datasets_hf
        resultado = buscar_datasets_hf("iris", max_results=3)
        for ds in resultado:
            assert isinstance(ds['downloads'], int)
            assert isinstance(ds['likes'], int)
