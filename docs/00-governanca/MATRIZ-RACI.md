# Matriz RACI

## Finalidade

Definir quem é responsável, aprovador, consultado e informado nas atividades críticas do projeto.

## Como preencher

1. Substitua os papéis genéricos pelas áreas reais do projeto.
2. Cada atividade deve ter exatamente um aprovador principal sempre que possível.
3. Evite muitos responsáveis na mesma atividade.

Premissas:

- Responsabilidade explícita reduz retrabalho.
- Atividades sem aprovador tendem a ficar pendentes.

| Atividade | Produto | Engenharia | Dados | Segurança | Operação | Negócio |
| --- | --- | --- | --- | --- | --- | --- |
| Validar CONOPS | A | C | C | C | C | R |
| Detalhar SRS | A | R | C | C | C | C |
| Definir arquitetura | C | A/R | C | C | C | C |
| Governar fontes | C | C | A/R | C | C | R |
| Aprovar MVP | A | R | C | C | C | A/R |

Legenda: R = responsável; A = aprovador; C = consultado; I = informado.

## Exemplo de nova linha

| Atividade | Produto | Engenharia | Dados | Segurança | Operação | Negócio |
| --- | --- | --- | --- | --- | --- | --- |
| Aprovar nova fonte de conhecimento | C | C | R | A | I | C |
