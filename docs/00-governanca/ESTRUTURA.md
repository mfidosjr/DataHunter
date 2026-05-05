# Estrutura de Engenharia e Arquitetura de IA

## Finalidade

Explicar como organizar documentos, código, dados, testes, operação e governança no projeto.

## Como usar

Use este arquivo como mapa de organização do repositório. Atualize quando novas pastas, artefatos ou padrões forem adicionados.

Premissas:

- Estrutura clara reduz retrabalho.
- Documentos devem ter lugar definido.
- Código, dados, prompts e governança devem ser separados.

## Princípios

1. Separar visão de negócio de implementação.
2. Manter rastreabilidade entre CONOPS, requisitos, arquitetura, testes e backlog.
3. Tratar agentes como componentes governados.
4. Tratar prompts como artefatos versionados.
5. Separar dados e conhecimento de código.
6. Planejar avaliação desde o início.
7. Projetar observabilidade e auditoria como requisitos centrais.
8. Preservar segurança, privacidade e conformidade por design.

## Sequência Documental

| Ordem | Artefato | Local |
| --- | --- | --- |
| 1 | CONOPS | `docs/01-produto/CONOPS.md` |
| 2 | README executivo | `README.md` |
| 3 | SRS | `docs/02-requisitos/SRS.md` |
| 4 | SSS | `docs/03-arquitetura/SSS.md` |
| 5 | Modelo de Dados e Conhecimento | `docs/04-dados/MODELO-DADOS-CONHECIMENTO.md` |
| 6 | SSDD | `docs/03-arquitetura/SSDD.md` |
| 7 | Agentes | `docs/05-agentes/definicoes/` |
| 8 | Integrações | `docs/09-integracoes/` |
| 9 | Testes e avaliação | `docs/07-llmops/avaliacao/` |
| 10 | Backlog | `docs/11-backlog/` |
| 11 | Operação | `docs/10-operacao/` |

## Exemplo de uso

| Necessidade | Onde colocar |
| --- | --- |
| Novo requisito | `docs/02-requisitos/SRS.md` |
| Nova decisão arquitetural | `docs/03-arquitetura/decisoes/` |
| Nova fonte de conhecimento | `docs/04-dados/catalogo-fontes/` |
| Novo agente | `docs/05-agentes/definicoes/` |
| Novo runbook | `docs/10-operacao/runbooks/` |
