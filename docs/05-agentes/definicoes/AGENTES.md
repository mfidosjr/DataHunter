# Agentes

## Finalidade

Documentar agentes previstos, escopo, owner, entradas, saídas, ferramentas, fontes, limites, validação e métricas.

## Como preencher

Crie uma seção por agente. Todo agente deve obedecer ao contrato operacional.

Premissas:

- Agente sem owner não entra em produção.
- Agente sem fonte ou ferramenta autorizada deve ter escopo limitado.
- Agente deve ser testável.

## Modelo

| Campo | Como preencher | Exemplo |
| --- | --- | --- |
| Nome | Nome funcional | Agente de Suporte |
| Objetivo | Resultado esperado | Responder dúvidas sobre uso do produto |
| Owner | Área responsável | Atendimento |
| Entradas | Dados necessários | Mensagem, sessão, domínio |
| Saídas | Resposta ou decisão | Resposta candidata |
| Ferramentas | Tools permitidas | Retrieval FAQ |
| Limites | O que não faz | Não cancela contrato |
| Métricas | Como avaliar | Respostas com fonte |
