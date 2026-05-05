# Definition of Done do MVP

## Finalidade

Define critérios mínimos para considerar o MVP pronto para piloto controlado.

## Como usar este documento

Use como checklist de passagem. Cada item deve ter evidência antes de aprovar o MVP.

Premissas:

- O MVP tem escopo menor que o produto final.
- Demo funcionando não é suficiente.
- Segurança, observabilidade e fallback fazem parte do pronto.

## Dentro do MVP

- Canal inicial definido.
- Domínios prioritários definidos.
- Orquestração com grafo controlado.
- Agentes essenciais definidos.
- Fontes autorizadas e rastreáveis.
- Handoff humano definido.
- Observabilidade mínima.
- Segurança e privacidade por design.

### Como preencher

Substitua a lista acima pelo escopo real do MVP.

### Exemplo

`Canal inicial: chat web. Domínios: suporte, faturamento e dúvidas de produto. Handoff: ferramenta de tickets.`

## Fora do MVP

- Multicanalidade ampla.
- Personalização avançada.
- Transações complexas.
- Automação ativa sem aprovação humana.
- Knowledge graph avançado.

### Como preencher

Declare explicitamente o que fica para próxima versão para evitar expansão informal de escopo.

## Critérios bloqueantes

O MVP não deve avançar se houver resposta sem fonte confiável, exposição de dado sensível, ausência de logs críticos, falta de fallback ou handoff sem contexto mínimo.

### Exemplo

| Critério bloqueante | Evidência esperada |
| --- | --- |
| Resposta sem fonte confiável | Teste ou amostra demonstrando bloqueio |
| Handoff sem contexto | Payload com resumo, categoria e motivo |
