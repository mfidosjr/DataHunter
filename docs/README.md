# Documentação

Esta pasta organiza os artefatos de produto, engenharia, arquitetura, governança, segurança e operação.

## Como usar

Leia os documentos nesta ordem:

1. `01-produto/CONOPS.md`
2. `02-requisitos/SRS.md`
3. `03-arquitetura/SSS.md`
4. `04-dados/MODELO-DADOS-CONHECIMENTO.md`
5. `03-arquitetura/SSDD.md`

Premissa: a documentação deve reduzir retrabalho. Se uma decisão ainda não existe, registre como questão aberta, premissa ou risco.

| Pasta | Finalidade |
| --- | --- |
| `00-governanca/` | Estrutura, RACI, Definition of Done, stack e referências. |
| `01-produto/` | CONOPS e visão do produto. |
| `02-requisitos/` | SRS, requisitos, critérios de aceite e rastreabilidade. |
| `03-arquitetura/` | SSS, SSDD, arquitetura, ADRs e contrato dos agentes. |
| `04-dados/` | Modelo de dados e conhecimento, fontes, ingestão e qualidade. |
| `05-agentes/` | Definições, políticas, ferramentas e limites operacionais dos agentes. |
| `06-prompts/` | Templates, políticas, versionamento e avaliação de prompts. |
| `07-llmops/` | Avaliação, custos, observabilidade e AgentOps. |
| `08-seguranca-lgpd/` | Segurança, privacidade, ameaças, controles e retenção. |
| `09-integracoes/` | Integrações externas. |
| `10-operacao/` | Runbooks, auditoria, SLO/SLA e sustentação. |
| `11-backlog/` | Backlog, roadmap, épicos e histórias. |
| `12-riscos/` | Riscos, premissas, restrições e mitigação. |

## Referências

A biblioteca central fica em `00-governanca/referencias/` e pode ser usada por projetos derivados como fonte-base.

| Arquivo | Uso |
| --- | --- |
| `00-governanca/referencias/README.md` | Índice, categorias, regras de uso e mapeamento por camada. |
| `00-governanca/referencias/llm-rag-agentes.md` | Papers, frameworks e avaliação de LLM/RAG/agentes. |
| `00-governanca/referencias/normas-governanca.md` | Normas, leis e frameworks de governança de IA. |

## Exemplo de fluxo de preenchimento

| Etapa | Ação |
| --- | --- |
| CONOPS | Definir problema, usuários, operação, MVP e critérios de sucesso. |
| SRS | Transformar CONOPS em requisitos testáveis. |
| SSS | Alocar requisitos em subsistemas. |
| DKM | Modelar fontes, dados, evidências e lacunas. |
| SSDD | Descrever como construir a solução. |
