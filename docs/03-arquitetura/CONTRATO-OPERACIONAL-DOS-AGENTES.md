# Contrato Operacional dos Agentes

## Finalidade

Definir o mínimo necessário para criar, validar, operar e auditar agentes de IA.

## Como usar este documento

Preencha um contrato por agente ou use esta tabela como checklist antes de liberar um agente para MVP/piloto.

Premissas:

- Agentes são componentes governados, não prompts soltos.
- Cada agente possui limites, owner, ferramentas e fontes autorizadas.
- Todo agente deve ser observável e testável.

Nenhum agente deve entrar em produção sem:

- escopo definido;
- owner;
- entradas esperadas;
- saídas permitidas;
- ferramentas autorizadas;
- fontes autorizadas;
- limites operacionais;
- critérios de validação;
- fallback;
- métricas;
- auditoria;
- testes.

## Modelo de especificação

| Campo | Como preencher | Exemplo |
| --- | --- | --- |
| Nome | Nome funcional do agente | Agente de Atendimento |
| Objetivo | Resultado que o agente entrega | Responder dúvidas informacionais |
| Entradas | Dados mínimos necessários | Mensagem, sessão, domínio |
| Saídas | O que pode produzir | Resposta candidata ou pedido de contexto |
| Ferramentas | Tools autorizadas | Retrieval, API de status |
| Limites | O que não pode fazer | Não altera dados cadastrais |
| Fallback | O que fazer em erro/dúvida | Escalar para humano |
| Métricas | Como medir | Taxa de resposta com fonte |

## Exemplo preenchido

| Campo | Valor |
| --- | --- |
| Nome | Validador |
| Objetivo | Aprovar, bloquear ou escalar respostas candidatas. |
| Entradas | Resposta candidata, evidências, política, confiança. |
| Saídas | `approved`, `blocked`, `clarify`, `handoff`. |
| Limites | Não gera resposta final de domínio. |
| Métricas | Taxa de bloqueio correto e erros críticos evitados. |
