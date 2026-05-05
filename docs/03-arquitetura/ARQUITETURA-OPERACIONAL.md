# Arquitetura Operacional

## Finalidade

Descrever como a solução opera em tempo de execução: canais, APIs, orquestração, agentes, ferramentas, conhecimento, modelos, dados e observabilidade.

## Como preencher

Use este documento para explicar o fluxo operacional antes de detalhar o SSDD.

Premissas:

- A arquitetura deve refletir as 8 camadas.
- Falhas e decisões devem aparecer no fluxo.
- Observabilidade é parte da arquitetura.

## Visão

Descreva componentes, fluxos, camadas, decisões e pontos de observabilidade.

```text
Canal -> API -> Orquestração -> Agentes -> Ferramentas/Conhecimento -> Validação -> Resposta/Handoff -> Logs/Métricas
```

## Exemplo de componentes

| Componente | Responsabilidade | Evidência |
| --- | --- | --- |
| Orquestrador | Decidir próximo estado | Log do caminho percorrido |
| Validador | Aprovar, bloquear ou escalar | Decisão registrada |
