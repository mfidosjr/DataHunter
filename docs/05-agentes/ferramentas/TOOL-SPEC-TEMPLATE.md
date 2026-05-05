# Template de Especificação de Ferramenta

## Finalidade

Padrão de documentação para ferramentas (tools/actions) usadas por agentes. Crie um arquivo por ferramenta, nomeado `TOOL-<nome>.md`.

---

## Identificação

| Campo | Valor |
| --- | --- |
| **Nome** | `tool_name_snake_case` |
| **Versão** | 1.0.0 |
| **Categoria** | busca / escrita / integração / validação / sistema |
| **Owner** | equipe responsável |
| **Status** | rascunho / ativo / depreciado |
| **Agentes autorizados** | lista de agentes que podem invocar esta ferramenta |

## Objetivo

Uma frase descrevendo o que a ferramenta faz e o resultado esperado.

## Esquema de entrada

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "param_obrigatorio": {
      "type": "string",
      "description": "Descrição do parâmetro",
      "maxLength": 500
    },
    "param_opcional": {
      "type": "integer",
      "description": "Descrição do parâmetro",
      "default": 10,
      "minimum": 1,
      "maximum": 100
    }
  },
  "required": ["param_obrigatorio"],
  "additionalProperties": false
}
```

## Esquema de saída

```json
{
  "type": "object",
  "properties": {
    "resultado": { "type": "string" },
    "fonte": { "type": "string", "description": "Identificador da fonte utilizada" },
    "confianca": { "type": "number", "minimum": 0, "maximum": 1 }
  },
  "required": ["resultado"]
}
```

## Validações e pré-condições

- [ ] Parâmetros obrigatórios presentes e dentro dos limites definidos no schema
- [ ] Agente invocante está na lista de autorizados
- [ ] Autenticação/permissões com sistema externo verificadas antes da execução
- [ ] Input sanitizado: sem caracteres de controle, injeções ou payloads maliciosos

## Limites de execução

| Parâmetro | Valor |
| --- | --- |
| Timeout | 30s |
| Máximo de retries | 2 |
| Backoff | exponencial, início 1s |
| Rate limit | 10 req/min por sessão |
| Tamanho máximo de entrada | 4.000 caracteres |
| Side effects permitidos | somente leitura (ou descrever escrita se aplicável) |

## Comportamento de fallback

O que acontece quando a ferramenta falha, timeout ou retorna resultado inválido:

1. **Tentativas 1-2:** retry com backoff exponencial.
2. **Após 2 retries:** retornar erro estruturado para o agente decidir continuação.
3. **Nunca:** propagar exceção não tratada para o usuário final.

Erro estruturado retornado:

```json
{
  "error": true,
  "error_code": "TOOL_TIMEOUT | TOOL_INVALID_RESPONSE | TOOL_AUTH_FAILED | TOOL_NOT_FOUND",
  "message": "mensagem legível para o agente",
  "retry_after_seconds": 60
}
```

## Segurança

| Risco | Controle |
| --- | --- |
| Injeção via parâmetro | Validar contra JSON Schema; rejeitar `additionalProperties` |
| Escopo excessivo | Allowlist de agentes autorizados; operações permitidas explícitas |
| Vazamento de dados | Mascarar PII em logs; não logar payloads completos |
| Side effects indesejados | Operações de escrita requerem confirmação explícita do agente |
| Prompt injection via resposta externa | Não repassar respostas de APIs externas sem sanitização |

## Métricas (OTel)

| Atributo / Métrica | Descrição | Alerta |
| --- | --- | --- |
| `tool.name` | Nome da ferramenta (atributo de span) | — |
| `tool.latency_ms` | Latência de execução | p95 > 5.000ms |
| `tool.error_rate` | Taxa de erros (4xx/5xx + exceções) | > 5% em 5min |
| `tool.retry_count` | Retries realizados | > 20% das chamadas |
| `tool.timeout_rate` | Taxa de timeouts | > 2% em 5min |

## Exemplos

### Chamada válida

```python
result = await tool.run({
    "param_obrigatorio": "valor de exemplo",
    "param_opcional": 5
})
# result = {"resultado": "...", "fonte": "fonte-id", "confianca": 0.92}
```

### Retorno de erro esperado

```json
{
  "error": true,
  "error_code": "TOOL_NOT_FOUND",
  "message": "Recurso não encontrado para o parâmetro informado.",
  "retry_after_seconds": 0
}
```

## Histórico de versões

| Versão | Data | Mudança |
| --- | --- | --- |
| 1.0.0 | YYYY-MM-DD | Versão inicial |
