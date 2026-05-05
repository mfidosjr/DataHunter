# SSS - System/Subsystem Specification

## Finalidade

Especificar subsistemas, responsabilidades, interfaces, limites operacionais e alocação de requisitos.

## Como usar este documento

Use o SSS depois do SRS. O objetivo é decompor o sistema em subsistemas claros antes de desenhar a implementação detalhada no SSDD.

Premissas:

- Requisitos principais já existem.
- A arquitetura em 8 camadas foi aceita.
- Integrações e agentes principais foram identificados.

## Subsistemas iniciais

- Experiência.
- Backend/API.
- Orquestração.
- Agentes.
- Tool gateway.
- Conhecimento/RAG.
- Modelos.
- Dados/auditoria.
- Integrações.
- Operação.

## Modelo de especificação de subsistema

### O que preencher

Para cada subsistema, informe:

- objetivo;
- responsabilidades;
- entradas;
- saídas;
- interfaces;
- dados usados;
- requisitos alocados;
- limites operacionais;
- falhas esperadas;
- métricas.

### Exemplo

| Campo | Exemplo |
| --- | --- |
| Subsistema | Orquestração |
| Objetivo | Coordenar estados, agentes, ferramentas e decisões. |
| Entradas | Mensagem, sessão, contexto, políticas. |
| Saídas | Resposta, bloqueio, esclarecimento ou handoff. |
| Requisitos | RF-001, RF-002, RNF-004. |
| Limites | Não executa ferramenta fora de allowlist. |

## Alocação de requisitos

| Requisito | Subsistema responsável | Subsistemas consultados |
| --- | --- | --- |
| `RF-001` | Orquestração | Modelos, Dados |
