# SRS - Software Requirements Specification

## Finalidade

Detalhar requisitos funcionais, não funcionais, interfaces, métricas, critérios de aceite, testes e rastreabilidade.

## Como usar este documento

Use o SRS depois do CONOPS. Cada requisito deve ser claro, testável, rastreável e possuir critério de aceite.

Premissas:

- O CONOPS foi revisado.
- Casos de uso e cenários operacionais estão identificados.
- O MVP tem escopo mínimo definido.

## Estrutura

1. Escopo.
2. Requisitos funcionais.
3. Requisitos não funcionais.
4. Requisitos por camada.
5. Interfaces.
6. Dados e conhecimento.
7. Segurança e privacidade.
8. Observabilidade.
9. Critérios de aceite.
10. Rastreabilidade.

## 1. Escopo

### O que é

Define o que o software deve cobrir no MVP e o que fica fora.

### Como preencher

Descreva limites funcionais, canais, integrações, dados, usuários e exclusões.

### Exemplo

`O MVP cobre consulta informacional via chat web e handoff humano. Não cobre transações, pagamento ou automação ativa sem aprovação.`

## 2. Requisitos funcionais

### O que é

Comportamentos que o sistema deve executar.

### Como preencher

Use IDs `RF-001`, verbos obrigatórios e critério de aceite.

### Exemplo

| ID | Requisito | Prioridade | Critério de aceite |
| --- | --- | --- | --- |
| RF-001 | O sistema deve classificar a intenção da mensagem do usuário. | Alta | Dado um conjunto de perguntas de teste, deve retornar intenção e confiança. |

## 3. Requisitos não funcionais

### O que é

Qualidades do sistema: segurança, privacidade, latência, disponibilidade, observabilidade, custo e manutenibilidade.

### Exemplo

| ID | Categoria | Requisito | Métrica |
| --- | --- | --- | --- |
| RNF-001 | Observabilidade | O sistema deve registrar modelo, tokens e custo por interação. | 100% das chamadas ao modelo. |

## 4. Requisitos por camada

### O que é

Organização dos requisitos pelas 8 camadas de arquitetura.

### Exemplo

| Camada | Requisito relacionado |
| --- | --- |
| Conhecimento | Respostas operacionais devem possuir fonte autorizada. |
| Operação | O painel deve mostrar taxa de handoff e custo estimado. |

## 5. Rastreabilidade

### O que é

Conecta requisitos a objetivos, casos de uso, cenários, testes e DoD.

### Exemplo

| Requisito | Caso de uso | Cenário | Teste | DoD |
| --- | --- | --- | --- | --- |
| RF-001 | UC-01 | SC-01 | `test_intent_classifier` | DoD por caso de uso |
