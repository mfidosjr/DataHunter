# Stack

## Finalidade

Registrar tecnologias, versões, comandos e decisões de stack do projeto.

## Como preencher

Mantenha este arquivo atualizado sempre que uma dependência estrutural for adicionada, removida ou substituída.

Premissas:

- O stack deve ser suficiente para desenvolvimento, teste e operação inicial.
- Dependências devem ter motivo claro.
- Segredos não devem ser documentados aqui.

Stack base sugerido:

- Python 3.12.
- uv.
- FastAPI.
- LangGraph.
- Azure OpenAI/OpenAI SDK.
- Pydantic.
- Pytest.
- Ruff.
- Mypy.
- OpenTelemetry/structlog, quando aplicável.

## Comandos

```bash
uv sync --all-extras
uv run --extra dev pytest
uv run uvicorn ai_system_template.api.main:app --reload
```

## Exemplo de decisão de stack

| Tecnologia | Uso | Motivo |
| --- | --- | --- |
| FastAPI | API HTTP | Simples, tipado e compatível com testes locais. |
| LangGraph | Orquestração | Grafo de estados auditáveis com `conditional_edge` para roteamento dual Sistema 1 (caminho rápido) / Sistema 2 (caminho profundo). |
