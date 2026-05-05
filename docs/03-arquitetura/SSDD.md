# SSDD - System/Software Design Description

## Finalidade

Descrever o desenho técnico da solução.

## Como usar este documento

Use o SSDD após CONOPS, SRS, SSS e Modelo de Dados e Conhecimento. Ele deve explicar como construir a solução, incluindo componentes, fluxos, APIs, estados, dados, segurança, observabilidade e implantação.

Premissas:

- Os subsistemas foram definidos no SSS.
- As fontes e dados foram modelados no DKM.
- Os critérios de DoD estão claros.

## Estrutura

1. Visão arquitetural.
2. Componentes.
3. Grafos e fluxos.
4. Estados e decisões.
5. APIs.
6. Integrações.
7. Dados, logs e auditoria.
8. Segurança e privacidade.
9. Observabilidade.
10. Fallback e degradação.
11. Implantação.

## 1. Visão arquitetural

### Como preencher

Descreva a arquitetura em diagrama textual ou Mermaid, destacando camadas e componentes.

### Exemplo

```text
Canal -> API -> Orquestração -> Agentes -> Ferramentas/RAG -> Validação -> Resposta/Handoff -> Logs
```

## 2. Componentes

### Como preencher

Para cada componente, descreva responsabilidade, tecnologia, interfaces e métricas.

### Exemplo

| Componente | Responsabilidade | Tecnologia |
| --- | --- | --- |
| API | Receber mensagens e gerenciar sessão | FastAPI |

## 3. Estados e decisões

### Como preencher

Liste estados, transições, entradas, saídas e decisões.

### Exemplo

| Estado | Entrada | Decisão | Saída |
| --- | --- | --- | --- |
| `validate_answer` | Resposta candidata | Aprovar, bloquear ou escalar | Resultado validado |

## 4. Fallback

### Como preencher

Para cada falha relevante, defina comportamento controlado.

### Exemplo

| Falha | Fallback | Evidência |
| --- | --- | --- |
| Fonte indisponível | Usar cache válido ou escalar | Log de erro e decisão |
