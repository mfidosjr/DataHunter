# tests/integration/conftest.py
import pytest

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration: testes que fazem chamadas reais de rede e API"
    )
