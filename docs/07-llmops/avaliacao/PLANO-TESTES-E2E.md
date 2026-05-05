# Plano de Testes E2E

Defina testes ponta a ponta para canais, APIs, agentes, fontes, integrações, fallback e auditoria.

## Como preencher

Para cada cenário, defina entrada, passos, resultado esperado, evidência e automação.

## Exemplo

| ID | Cenário | Entrada | Resultado esperado | Evidência |
| --- | --- | --- | --- | --- |
| E2E-001 | Pergunta com fonte confiável | Pergunta simples do domínio | Resposta com fonte | Log com agente, fonte e decisão |
| E2E-002 | Fonte ausente | Pergunta fora da base | Bloqueio ou handoff | Evento de baixa confiança |
