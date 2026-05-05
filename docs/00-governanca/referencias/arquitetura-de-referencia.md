# Arquitetura de Referência para Sistemas de Inteligência Artificial

> Documento de referência técnica do template AIT. Descreve o modelo arquitetural
> em oito camadas adotado como padrão de projeto e as referências que embasam cada
> decisão de design.

## Sumário

- [1 Introdução](#1-introdução)
- [2 Modelo em 8 Camadas](#2-modelo-em-8-camadas)
- [3 Base de Referência](#3-base-de-referência)
  - [3.1 Documentação e Notação Arquitetural](#31-documentação-e-notação-arquitetural)
  - [3.2 Arquiteturas de Referência em Nuvem](#32-arquiteturas-de-referência-em-nuvem)
  - [3.3 Fundamentos Científicos](#33-fundamentos-científicos)
  - [3.4 Segurança, Governança e Conformidade Regulatória](#34-segurança-governança-e-conformidade-regulatória)
  - [3.5 Infraestrutura de Conhecimento e Dados Semânticos](#35-infraestrutura-de-conhecimento-e-dados-semânticos)
  - [3.6 Observabilidade e Avaliação de Sistemas de IA](#36-observabilidade-e-avaliação-de-sistemas-de-ia)
- [4 Camadas da Arquitetura](#4-camadas-da-arquitetura)
  - [4.1 Camada 1 — Experiência](#41-camada-1--experiência)
  - [4.2 Camada 2 — Segurança](#42-camada-2--segurança)
  - [4.3 Camada 3 — Orquestração](#43-camada-3--orquestração)
  - [4.4 Camada 4 — Ação](#44-camada-4--ação)
  - [4.5 Camada 5 — Conhecimento](#45-camada-5--conhecimento)
  - [4.6 Camada 6 — Modelos](#46-camada-6--modelos)
  - [4.7 Camada 7 — Dados](#47-camada-7--dados)
  - [4.8 Camada 8 — Operação](#48-camada-8--operação)
- [5 Referências](#5-referências)

## 1 Introdução

A construção de sistemas de inteligência artificial para produção demanda uma abordagem
arquitetural que transcenda o modelo isolado. Sistemas inteligentes modernos combinam
raciocínio probabilístico, recuperação de conhecimento, execução de ações externas e
operação contínua em ambientes dinâmicos — características que impõem separação clara
de responsabilidades entre seus componentes (BASS; CLEMENTS; KAZMAN, 2022).

Este documento descreve um modelo de arquitetura em oito camadas proposto como padrão
de projeto para sistemas de IA. Para sua elaboração, foram consultadas referências de
mercado e literatura científica que contribuíram com padrões, práticas e terminologia
utilizados na caracterização de cada camada. As seções a seguir apresentam o modelo,
a estrutura das camadas e a contribuição específica de cada base de referência adotada.

## 2 Modelo em 8 Camadas

O modelo organiza um sistema de IA em oito camadas verticais, dispostas em ordem
decrescente de abstração — da interface com o usuário até a infraestrutura de operação.
A Figura 1 ilustra a estrutura geral.

```
┌──────────────────────────────────────────────────────────────────────┐
│  1 · EXPERIÊNCIA    Chat Web · WhatsApp · REST API · Streaming        │
│                     Copilot embarcado                                 │
├──────────────────────────────────────────────────────────────────────┤
│  2 · SEGURANÇA      AuthN/AuthZ · RBAC · Agent Auth · Secrets Mgr    │
│                     Auditoria · Policy Engine                         │
├──────────────────────────────────────────────────────────────────────┤
│  3 · ORQUESTRAÇÃO   Planner · Executor · Agent Loop · Tool Selection  │
│                     Guardrails · Human-in-the-Loop                    │
├──────────────────────────────────────────────────────────────────────┤
│  4 · AÇÃO           Tool Gateway · API Calls · SQL · ERP/CRM          │
│                     File I/O · Schema Validation                      │
├──────────────────────────────────────────────────────────────────────┤
│  5 · CONHECIMENTO   Session Context · Short/Long-term Memory · RAG    │
│                     Knowledge Graph · Reranker                        │
├──────────────────────────────────────────────────────────────────────┤
│  6 · MODELOS        Foundation Models · Model Router · Embeddings     │
│                     Classifiers · Fallback · Multi-model              │
├──────────────────────────────────────────────────────────────────────┤
│  7 · DADOS          ETL/ELT · Vector Store · Relational DB · Cache    │
│                     Event Streams · Data Governance                   │
├──────────────────────────────────────────────────────────────────────┤
│  8 · OPERAÇÃO       Distributed Tracing · Prompt Logs · Latency       │
│                     Cost Tracking · CI/CD · SLO/SLA                   │
└──────────────────────────────────────────────────────────────────────┘
```

**Figura 1** — Modelo de arquitetura de referência em oito camadas.

A separação em camadas segue o princípio de responsabilidade única aplicado à escala
arquitetural: cada camada encapsula decisões de design coesas e expõe interfaces bem
definidas para as camadas adjacentes. A documentação das camadas adota as convenções
de notação do C4 Model (BROWN, 2022) e o template estrutural do arc42 (STARKE;
HRUSCHKA, 2022), com decisões de design registradas no formato ADR (NYGARD, 2011).

## 3 Base de Referência

As referências consultadas foram organizadas em seis grupos temáticos. Cada grupo
descreve as obras e documentos utilizados e sua contribuição específica para este
documento.

### 3.1 Documentação e Notação Arquitetural

**C4 Model** (BROWN, 2022) contribui com o sistema de notação adotado para os diagramas
de arquitetura: contexto (nível 1), contêiner (nível 2), componente (nível 3) e código
(nível 4). A hierarquia do C4 Model permite comunicar a mesma arquitetura para públicos
técnicos e não técnicos com um conjunto mínimo de artefatos, sem ambiguidade de símbolos.

**arc42** (STARKE; HRUSCHKA, 2022) fornece o template estrutural para documentação de
arquitetura de software. Seus doze tópicos — contexto, restrições, visão de solução,
estratégia de decomposição, visões de construção e runtime, infraestrutura, conceitos
transversais, decisões, requisitos de qualidade, riscos e glossário — são referenciados
na organização dos documentos SSDD e SSS do template AIT.

**Architecture Decision Records — ADR** (NYGARD, 2011) estabelece a prática de registrar
decisões arquiteturais como documentos versionados, com contexto, alternativas
consideradas e consequências. O template AIT adota o formato ADR para todas as decisões
de design que envolvam trade-offs relevantes entre camadas.

**NASA Systems Engineering Handbook** (NASA, 2016) e o **Systems Engineering Body of
Knowledge — SEBoK** (INCOSE, 2023) contribuem com o arcabouço de engenharia de sistemas
aplicado ao ciclo de vida do produto: Conceito de Operações (ConOps), requisitos,
arquitetura, verificação e validação. Esses documentos embasam a sequência de artefatos
de engenharia do template AIT.

### 3.2 Arquiteturas de Referência em Nuvem

**Azure Well-Architected Framework for AI** (MICROSOFT, 2024a) contribui com os cinco
pilares de design para workloads de IA em produção: confiabilidade, segurança, otimização
de custos, excelência operacional e eficiência de desempenho. Esses pilares fundamentaram
a definição dos critérios de qualidade das Camadas 2 (Segurança) e 8 (Operação).

**Azure Responsible AI** (MICROSOFT, 2024b) complementa o framework anterior com
diretrizes para IA responsável: equidade, confiabilidade, privacidade, inclusão,
transparência e responsabilização. Essas diretrizes informam os controles da Camada 2
e os requisitos de Guardrails e Human-in-the-Loop da Camada 3 (Orquestração).

**Google Cloud RAG Reference Architectures** (GOOGLE, 2024a) documenta padrões de RAG
(*Retrieval-Augmented Generation*), busca vetorial, GraphRAG e CI/CD para pipelines de
recuperação. Suas arquiteturas de referência embasaram o detalhamento dos componentes
da Camada 5 (Conhecimento) e da Camada 7 (Dados).

**Google Cloud MLOps** (GOOGLE, 2021) e o **MLOps Whitepaper** (GOOGLE, 2024b) descrevem
os níveis de maturidade para entrega contínua e automação de pipelines de machine
learning (CI/CD/CT). Esses padrões fundamentam os componentes de CI/CD e SLO/SLA da
Camada 8 (Operação).

**AWS Generative AI CDK Constructs** (AWS, 2024a) e os **AWS GenAI CDK Constructs Samples**
(AWS, 2024b) fornecem exemplos de infraestrutura como código (*Infrastructure as Code*)
para padrões GenAI na AWS — RAG, agentes e bases de conhecimento. São referência de
implementação para as Camadas 4 (Ação) e 7 (Dados).

### 3.3 Fundamentos Científicos

**Retrieval-Augmented Generation** (LEWIS et al., 2020) é o artigo fundacional do padrão
RAG, que combina recuperação de documentos com geração de linguagem natural. Define os
fundamentos teóricos do componente RAG da Camada 5 (Conhecimento).

**Self-RAG** (ASAI et al., 2023) estende o RAG com reflexão adaptativa: o modelo decide
quando recuperar, avalia a relevância dos trechos recuperados e critica suas próprias
respostas. Contribui para o design do componente Reranker e os critérios de avaliação
da Camada 5.

**ReAct: Reasoning and Acting** (YAO et al., 2022) propõe a integração de raciocínio
em linguagem natural com execução de ações externas em um loop único. É o fundamento
teórico do padrão Agent Loop da Camada 3 (Orquestração).

**Chain-of-Thought Prompting** (WEI et al., 2022) demonstra que solicitar ao modelo a
explicitação do raciocínio melhora consistentemente a qualidade em tarefas complexas.
Contribui para o design do componente Planner e das estratégias de Guardrails da
Camada 3.

**Tree of Thoughts** (YAO et al., 2023) generaliza o Chain-of-Thought para exploração
de múltiplos caminhos de raciocínio com busca e backtracking. Referência para o
componente Executor da Camada 3 em cenários que exigem deliberação estruturada.

**Self-Consistency** (WANG et al., 2022) propõe a geração de múltiplas cadeias de
raciocínio independentes com votação majoritária para aumentar a robustez das respostas.
Informa a estratégia de Fallback da Camada 6 (Modelos).

**DSPy** (KHATTAB et al., 2023) apresenta um framework de programação declarativa para
pipelines de LLM, com otimização automática de prompts via compilação. Contribui para
o design do componente Tool Selection da Camada 3 e do Model Router da Camada 6.

**Toolformer** (SCHICK et al., 2023) demonstra que modelos de linguagem podem aprender
a usar ferramentas externas de forma autossupervisionada. É referência conceitual para
o Tool Gateway da Camada 4 (Ação).

**Knowledge Graphs** (HOGAN et al., 2020) define os fundamentos teóricos e práticos de
grafos de conhecimento — representação, consulta, raciocínio e aplicações. Embasa o
componente Knowledge Graph da Camada 5 e as tecnologias semânticas da Camada 7 (Dados).

**Attention Is All You Need** (VASWANI et al., 2017) apresenta a arquitetura Transformer,
que fundamenta todos os Foundation Models utilizados na Camada 6 (Modelos). Referência
obrigatória para compreensão dos princípios dos modelos de linguagem de grande escala.

**Hidden Technical Debt in ML Systems** (SCULLEY et al., 2015) documenta formas de dívida
técnica específicas de sistemas de ML — dependências ocultas, erosão de abstração,
feedback loops — e orienta as práticas de governança das Camadas 7 (Dados) e 8 (Operação).

**The ML Test Score** (BRECK et al., 2017) propõe um rubric de prontidão para produção de
sistemas de ML, com testes organizados em quatro áreas: dados, modelos, infraestrutura de
ML e monitoramento. Complementa o Hidden Technical Debt como referência para os critérios
de qualidade da Camada 8 (Operação) e para a estratégia de testes da Camada 7 (Dados).

**RAGAS** (ES et al., 2023) propõe um framework de avaliação sem referência para sistemas
RAG, com métricas de fidelidade, relevância contextual e resposta. Contribui para os
critérios de avaliação da Camada 5 e os indicadores de SLO/SLA da Camada 8.

### 3.4 Segurança, Governança e Conformidade Regulatória

**NIST AI Risk Management Framework — AI RMF 1.0** (NIST, 2023a) define um framework
voluntário para gerenciamento de riscos em sistemas de IA, organizado nas funções
Govern, Map, Measure e Manage. Fundamenta os controles de governança transversais a
todas as camadas, com ênfase nas Camadas 2 (Segurança) e 8 (Operação).

**NIST AI 600-1 — Generative AI Profile** (NIST, 2024) especializa o AI RMF para sistemas
de IA generativa, endereçando riscos como alucinação, viés, uso indevido e privacidade.
Informa diretamente os componentes Guardrails e Policy Engine das Camadas 2 e 3.

**OWASP Top 10 for LLM Applications** (OWASP, 2025) cataloga as dez vulnerabilidades
mais críticas em aplicações baseadas em LLMs: prompt injection, vazamento de dados,
execução insegura de ferramentas, entre outras. É referência central para o design de
segurança das Camadas 2, 3 e 4.

**EU AI Act — Regulation (EU) 2024/1689** (PARLAMENTO EUROPEU, 2024) é o regulamento
europeu de IA, que classifica sistemas por nível de risco e define obrigações de
conformidade, transparência e supervisão humana. Contribui para os requisitos da
Camada 2 e para o componente Human-in-the-Loop da Camada 3.

**LGPD — Lei Geral de Proteção de Dados** (BRASIL, 2018) estabelece os princípios e
obrigações para tratamento de dados pessoais no Brasil. Informa os requisitos de
privacidade e anonimização da Camada 7 (Dados) e os mecanismos de auditoria da
Camada 2 (Segurança).

**PL 2338/2023** (BRASIL, 2023) é o projeto de lei brasileiro de regulação de IA em
tramitação no Congresso Nacional. Seus dispositivos sobre responsabilidade, transparência
e direitos dos usuários são monitorados como requisitos prospectivos para as Camadas 2
e 3.

### 3.5 Infraestrutura de Conhecimento e Dados Semânticos

**W3C OWL 2** (W3C, 2012), **W3C RDF 1.1** (W3C, 2014), **W3C SHACL** (W3C, 2017) e
**W3C PROV** (W3C, 2013) formam o conjunto de padrões semânticos adotados para
representação de conhecimento estruturado. OWL 2 define ontologias formais; RDF 1.1
provê o modelo de dados em grafo; SHACL especifica restrições e validação de grafos;
PROV registra proveniência de dados e rastreabilidade de decisões. Esses padrões embasam
o Knowledge Graph da Camada 5 e os requisitos de rastreabilidade da Camada 7.

**Microsoft GraphRAG** (MICROSOFT, 2024c) implementa RAG sobre grafos de conhecimento
extraídos automaticamente de corpora de texto, combinando busca local e global. Contribui
para o design do componente Knowledge Graph integrado ao RAG na Camada 5.

### 3.6 Observabilidade e Avaliação de Sistemas de IA

**OpenTelemetry** (OPENTELEMETRY, 2024a) é o padrão aberto para instrumentação de
sistemas distribuídos — traces, métricas e logs. A especificação **GenAI Semantic
Conventions** (OPENTELEMETRY, 2024b) define os atributos específicos para instrumentação
de chamadas a LLMs: prompt, tokens, latência e custo. Esses padrões fundamentam os
componentes Distributed Tracing e Prompt Logs da Camada 8 (Operação).

**Prometheus** (PROMETHEUS, 2024) é o sistema de coleta e armazenamento de métricas
time-series amplamente adotado em ambientes cloud-native. Referência para os componentes
Latency Metrics e Cost Tracking da Camada 8.

**TruLens** (TRUERA, 2024), **DeepEval** (CONFIDENT AI, 2024), **RAGAS** (ES et al.,
2023) e **OpenAI Evals** (OPENAI, 2024) formam o conjunto de ferramentas de avaliação
de sistemas de IA generativa. Cobrem avaliação de relevância, fidelidade, grounding e
segurança de respostas — insumos para os indicadores de SLO/SLA da Camada 8 e para
os testes de regressão no pipeline CI/CD.

## 4 Camadas da Arquitetura

> **Nota de uso**: os componentes listados em cada camada são exemplos representativos
> do padrão arquitetural. Cada projeto seleciona os componentes aplicáveis ao seu
> contexto e registra as decisões de inclusão, exclusão ou substituição em ADRs
> específicos (NYGARD, 2011).

### 4.1 Camada 1 — Experiência

A Camada de Experiência é o ponto de contato entre o sistema de IA e seus usuários.
Ela concentra os canais de interação e os adaptadores de protocolo responsáveis por
receber entradas, formatar respostas e entregar a experiência de uso — sem conter lógica
de raciocínio ou acesso direto a dados.

**Componentes:**

| Componente | Descrição | Exemplos de Implementação |
|---|---|---|
| Interface Conversacional | Canal síncrono de interação textual com o sistema. | Chat Web, Slack, Microsoft Teams |
| Canal de Mensageria | Integração com plataformas de mensagens assíncronas. | WhatsApp, Telegram, SMS |
| API de Integração | Interface programática para sistemas externos e aplicações cliente. | REST, GraphQL, gRPC |
| Entrega em Tempo Real | Protocolo de streaming incremental de respostas, reduzindo latência percebida. | Server-Sent Events (SSE), WebSocket |
| Interface Embarcada | Componente de assistência contextual embutido em sistemas existentes. | Copilot, widget, plugin |

**Responsabilidades:**

- Receber e normalizar entradas de múltiplos canais para um formato interno único
- Encaminhar requisições à Camada 2 (Segurança) para autenticação antes da orquestração
- Serializar e entregar respostas no formato e protocolo esperados por cada canal
- Gerenciar sessão de usuário e contexto de janela de conversa no nível do canal

**Interfaces:**

- *Para baixo (Camada 2 — Segurança)*: toda requisição oriunda desta camada atravessa
  os controles de autenticação e autorização antes de alcançar a orquestração.
- *Fronteira externa*: não há camada superior — este é o limite do sistema com o
  ambiente externo.

**Padrões de design:**

A separação entre canal e lógica de negócio segue o padrão *Adapter*, que permite
adicionar novos canais sem modificar a orquestração subjacente.
O suporte a múltiplos canais simultâneos é consistente com as arquiteturas de referência
GenAI da AWS (AWS, 2024a; 2024b), que tratam a camada de experiência como conjunto de
adaptadores independentes sobre uma mesma base orquestral.

**Decisões de design e trade-offs:**

- Manter a camada *stateless* sempre que possível; estado de sessão deve ser gerenciado
  por componente externo (cache ou session store na Camada 7).
- Limitar o tamanho máximo de entrada por canal para mitigar riscos de prompt injection
  identificados pelo OWASP (OWASP, 2025).
- Implementar rate limiting e throttling nesta camada para proteção contra uso abusivo,
  antes do custo de processamento ser incorrido nas camadas internas.
- A escolha do protocolo de streaming (SSE vs. WebSocket) impacta a compatibilidade
  com proxies corporativos e deve ser registrada em ADR.

### 4.2 Camada 2 — Segurança

A Camada de Segurança é transversal ao sistema: posicionada entre a Experiência e a
Orquestração, ela intercepta todas as requisições e respostas, aplicando controles de
identidade, autorização, sigilo e auditoria. Nenhuma requisição alcança a lógica de
negócio sem passar por esta camada.

Sistemas de raciocínio baseados em IA introduzem vetores de ataque que não existem em
sistemas de software tradicionais. Frameworks de segurança genéricos — focados em
autenticação, autorização e criptografia — são necessários, mas insuficientes para
endereçar ameaças como manipulação do raciocínio do modelo, extração de informações
privilegiadas via prompt e execução não autorizada de ações por agentes autônomos
(OWASP, 2025; NIST, 2024). Por essa razão, os componentes desta camada são organizados
em dois grupos: controles de infraestrutura, comuns a qualquer sistema de software, e
controles específicos de sistemas de IA, que endereçam os riscos introduzidos pelo uso
de modelos de linguagem e agentes.

**Grupo A — Controles de Infraestrutura**

Controles estabelecidos de segurança de sistemas, aplicáveis a qualquer arquitetura de
software (NIST, 2023b).

| Componente | Descrição | Exemplos de Implementação |
|---|---|---|
| Autenticação e Autorização | Verificação de identidade (AuthN) e de permissões (AuthZ) de usuários e serviços (NIST, 2020, AC-2, IA-2). | OAuth 2.0, OpenID Connect, SAML |
| Controle de Acesso por Papel | Define o que cada perfil pode solicitar ao sistema — *Role-Based Access Control* (NIST, 2020, AC-3, AC-6). | OPA, AWS IAM, Azure RBAC |
| Autenticação entre Agentes | Mecanismo de autenticação entre agentes internos, prevenindo escalação de privilégios entre componentes (NIST, 2020, IA-9). | JWT de curta duração, mTLS |
| Gerenciador de Segredos | Armazenamento centralizado de credenciais, chaves de API e certificados, com rotação automática (NIST, 2020, SC-12, SC-28). | HashiCorp Vault, AWS Secrets Manager, Azure Key Vault |
| Auditoria | Registro imutável de eventos de segurança: autenticações, autorizações, acessos a dados e execuções de ferramentas (NIST, 2020, AU-2; OPENTELEMETRY, 2024a). | OpenTelemetry Logs, AWS CloudTrail, Splunk |
| Motor de Políticas | Avalia regras de acesso e conformidade em tempo de execução (NIST, 2020, AC-3, CM-7). | OPA, Cedar, Azure Policy |

**Grupo B — Controles Específicos de Sistemas de IA**

Controles que endereçam ameaças exclusivas de sistemas baseados em modelos de linguagem
e agentes, catalogadas pelo OWASP Top 10 for LLM Applications (OWASP, 2025) e pelo
NIST AI 600-1 (NIST, 2024).

| Componente | Ameaça Endereçada (OWASP LLM) | Descrição | Exemplos de Implementação |
|---|---|---|---|
| Filtro de Entrada | LLM01 — Prompt Injection | Detecta e bloqueia instruções maliciosas embutidas na entrada do usuário que tentam manipular o comportamento do modelo. | LLM Guard, Rebuff, regras customizadas |
| Filtro de Saída | LLM02 — Insecure Output Handling; LLM06 — Sensitive Information Disclosure; LLM07 — System Prompt Leakage | Inspeciona respostas do modelo antes da entrega: remove PII, bloqueia vazamento de system prompt e sanitiza conteúdo usado em pipelines downstream. | LLM Guard, Microsoft Presidio |
| Controle de Escopo do Agente | LLM08 — Excessive Agency | Limita explicitamente as ferramentas e ações que cada agente pode invocar, aplicando o princípio de privilégio mínimo ao plano de execução. | Listas de permissão por papel, sandbox de execução |
| Detecção de Conteúdo Nocivo | LLM09 — Misinformation; EU AI Act Art. 9 (PARLAMENTO EUROPEU, 2024) | Classifica inputs e outputs para identificar desinformação, conteúdo proibido e alucinações de alto impacto em contextos sensíveis. | Azure Content Safety, OpenAI Moderation API |

**Responsabilidades:**

- Verificar a identidade de usuários e serviços antes de encaminhar requisições à
  orquestração
- Aplicar políticas de autorização por papel, recurso e contexto
- Garantir que agentes internos operem com privilégios mínimos em ambos os grupos de
  controles
- Inspecionar entradas e saídas para ameaças específicas de LLMs antes e após a
  orquestração
- Registrar todos os eventos relevantes para auditoria e rastreabilidade forense
- Enforçar políticas de retenção e anonimização de dados em conformidade com a LGPD
  (BRASIL, 2018)

**Interfaces:**

- *Para cima (Camada 1 — Experiência)*: recebe requisições dos canais e devolve
  respostas autorizadas, ou rejeições com código de erro padronizado.
- *Para baixo (Camada 3 — Orquestração)*: encaminha requisições autenticadas,
  filtradas e enriquecidas com contexto de identidade e permissões.
- *Bidirecional*: o Filtro de Saída inspeciona também as respostas produzidas pela
  Orquestração antes de devolvê-las à Camada 1.

**Padrões de design:**

O NIST AI RMF (NIST, 2023a) organiza o gerenciamento de riscos em IA nas funções
Govern, Map, Measure e Manage. A Camada de Segurança implementa os controles
operacionais das funções Map e Measure. O NIST AI 600-1 (NIST, 2024) especializa esses
controles para sistemas generativos, mapeando riscos como *prompt injection*,
alucinação e uso indevido a controles técnicos concretos — incluindo os do Grupo B
acima.

O EU AI Act (PARLAMENTO EUROPEU, 2024) exige, para sistemas de alto risco, robustez
contra manipulação, supervisão humana e rastreabilidade de decisões. O Azure Responsible
AI framework (MICROSOFT, 2024b) operacionaliza esses requisitos em práticas de design,
incluindo filtragem de conteúdo e mecanismos de contenção de agentes.

**Decisões de design e trade-offs:**

- A granularidade do RBAC impacta a manutenibilidade: papéis muito específicos aumentam
  o controle, mas elevam o custo de gestão de identidade — registrar a decisão em ADR.
- Autenticação entre agentes internos deve usar tokens de curta duração; nunca
  credenciais de longa vida compartilhadas entre componentes.
- O Motor de Políticas centraliza regras de autorização, mas introduz latência em cada
  requisição — avaliar cache de decisões para políticas estáticas.
- Filtros de entrada e saída adicionam latência ao caminho crítico; avaliar execução
  assíncrona para casos onde a latência de segurança é inaceitável para o SLO.
- Logs de auditoria devem ser armazenados em destino separado e imutável, nunca no
  mesmo store das operações do sistema.

### 4.3 Camada 3 — Orquestração

A Camada de Orquestração é o núcleo decisório do sistema de IA. Ela coordena o fluxo
de execução entre agentes especializados, mantém o estado da conversa, seleciona
ferramentas, aplica guardrails e decide quando envolver um humano no processo. Diferente
de uma cadeia linear de chamadas, a orquestração é estruturada como um grafo de estados
com transições explícitas e auditáveis (YAO et al., 2022).

A arquitetura desta camada reflete a teoria dual-process de Kahneman (2003): um
*Sistema 1* rápido e automático, responsável por respostas diretas a consultas de baixa
complexidade, e um *Sistema 2* deliberativo e custoso, acionado apenas quando a consulta
exige planejamento, uso de ferramentas ou raciocínio multi-etapa. Rotear toda interação
pelo Sistema 2 seria funcionalmente correto, mas operacionalmente inviável: a latência e
o custo de tokens de um ciclo ReAct completo são desproporcionais para perguntas simples.
O componente *Complexity Router* implementa essa distinção, classificando cada solicitação
antes de comprometer recursos de raciocínio profundo.

A adoção do padrão *ReAct* — raciocínio intercalado com ação — como fundamento do
Sistema 2 implica que o modelo não apenas gera respostas, mas delibera sobre quais ações
tomar, observa resultados e revisa sua estratégia em cada passo (YAO et al., 2022).
Esse ciclo introduz riscos de agência excessiva quando não há controles explícitos sobre
o escopo de ação dos agentes (OWASP, 2025, LLM08).

**Componentes:**

| Componente | Descrição | Exemplos de Implementação |
|---|---|---|
| Complexity Router | Classifica cada solicitação por complexidade e risco antes de comprometer o ciclo de raciocínio. Consultas simples, de alta confiança e sem necessidade de ferramentas seguem o caminho rápido (Sistema 1 — resposta direta); demais seguem o caminho profundo (Sistema 2 — Agent Loop). A classificação usa um LLM leve ou regras heurísticas sobre intenção, domínio e histórico (KAHNEMAN, 2003). | LangGraph conditional edge, classificador de intenção, regras de roteamento |
| Planner | Decompõe a intenção do usuário em subproblemas ou sequência de etapas, utilizando Chain-of-Thought (WEI et al., 2022) ou Tree of Thoughts (YAO et al., 2023). Acionado apenas no caminho Sistema 2. | LangGraph StateGraph, DSPy Predict |
| Executor | Orquestra a execução sequencial ou paralela dos passos planejados, gerenciando dependências e resultados intermediários. | LangGraph Executor, CrewAI, AutoGen |
| Agent Loop | Implementa o ciclo Reason–Act–Observe do Sistema 2: o agente raciocina, executa uma ação via Tool Gateway e incorpora o resultado ao contexto antes da próxima etapa (YAO et al., 2022). | LangGraph ReAct Agent, LangChain AgentExecutor |
| Tool Selection | Seleciona a ferramenta adequada para cada etapa com base na intenção classificada, na descrição das ferramentas disponíveis e nas permissões do agente. | Function calling, DSPy ReAct (KHATTAB et al., 2023) |
| Guardrails | Intercepta entradas e saídas do ciclo agente–modelo para aplicar restrições de escopo, políticas de segurança e limites de iteração. Aplicado em ambos os caminhos. | NeMo Guardrails, LLM Guard, regras customizadas |
| Human-in-the-Loop | Detecta condições que exigem intervenção ou aprovação humana — baixa confiança, ação de alto impacto, contexto sensível — e suspende a execução até que a decisão seja tomada (PARLAMENTO EUROPEU, 2024, Art. 14). | LangGraph interrupt, Slack approval flow |

**Responsabilidades:**

- Manter estado da conversa e contexto acumulado ao longo do ciclo de execução
- Classificar intenção e domínio da solicitação para roteamento correto de agentes
- Planejar e executar sequências de ações dentro dos limites autorizados pela Camada 2
- Selecionar ferramentas com base na intenção e nas permissões do agente ativo
- Aplicar guardrails antes e após cada chamada ao modelo ou ferramenta
- Detectar condições de escalada para humano e suspender execução quando necessário
- Registrar trilha de execução completa — agentes, ferramentas, decisões e contexto — para auditoria na Camada 8

**Interfaces:**

- *Para cima (Camada 2 — Segurança)*: recebe requisições autenticadas com contexto de
  identidade e permissões; devolve respostas após aplicação dos guardrails de saída.
- *Para baixo (Camada 4 — Ação)*: delega execução de ferramentas ao Tool Gateway,
  recebendo resultados estruturados para incorporação ao contexto.
- *Para baixo (Camada 5 — Conhecimento)*: solicita recuperação de contexto, memória e
  documentos relevantes para fundamentar o raciocínio.
- *Para baixo (Camada 6 — Modelos)*: envia prompts estruturados e recebe respostas dos
  modelos de linguagem.

**Padrões de design:**

A teoria dual-process (KAHNEMAN, 2003) fornece o fundamento conceitual da camada: o
*Sistema 1* (rápido, automático, baixo custo) responde diretamente a consultas simples;
o *Sistema 2* (deliberativo, multi-etapa, custoso) é reservado para raciocínio complexo.
O Complexity Router materializa essa distinção — toda interação passa pelo roteador, mas
apenas uma fração aciona o Agent Loop completo.

```
entrada → [Guardrails entrada] → [Complexity Router]
                                        │
                    ┌───────────────────┴────────────────────┐
                    ▼ Sistema 1 (simples)                     ▼ Sistema 2 (complexo)
             resposta direta                        [Planner] → [Executor]
             (chamada única                              │
              ao modelo)                          [Agent Loop: Reason–Act–Observe]
                    │                                    │
                    └─────────────┬──────────────────────┘
                                  ▼
                         [Guardrails saída] → resposta
```

O padrão *ReAct* (YAO et al., 2022) fundamenta a estrutura do Agent Loop do Sistema 2:
raciocínio explícito intercalado com ações observáveis torna o comportamento do agente
interpretável e depurável. *Chain-of-Thought* (WEI et al., 2022) e *Tree of Thoughts*
(YAO et al., 2023) especializam o componente Planner para cenários de complexidade
crescente.

*DSPy* (KHATTAB et al., 2023) contribui com uma abordagem alternativa ao prompting
manual: pipelines declarativos com otimização automática de prompts, reduzindo a
fragilidade do sistema a variações de formulação.

O EU AI Act (PARLAMENTO EUROPEU, 2024) exige supervisão humana em sistemas de IA de
alto risco. O componente Human-in-the-Loop implementa esse requisito de forma
estruturada, com estado suspenso e trilha de aprovação auditável.

**Decisões de design e trade-offs:**

- Os critérios de roteamento do Complexity Router — limiar de confiança, presença de
  necessidade de ferramenta, sensibilidade do domínio — devem ser definidos e calibrados
  empiricamente; registrar decisão e métricas de corte em ADR.
- O número máximo de iterações do Agent Loop deve ser configurável e limitado; loops
  sem limite superior são vulnerabilidade conhecida de custo e segurança — registrar em ADR.
- Guardrails síncronos no caminho crítico adicionam latência; avaliar execução assíncrona
  para políticas de baixo risco e latência restrita.
- Estado conversacional armazenado em memória do processo não escala horizontalmente;
  externalizar estado para Camada 7 (cache ou store) desde o design inicial.
- A decisão de usar um único agente orquestrador versus múltiplos agentes especializados
  em subgrafos impacta manutenibilidade e testabilidade — registrar em ADR com critérios
  de evolução.

### 4.4 Camada 4 — Ação

A Camada de Ação executa interações com sistemas externos — APIs, bancos de dados,
sistemas de arquivos, ERPs e qualquer recurso fora do processo de raciocínio. Ela atua
como intermediária controlada entre os agentes e o mundo externo: nenhum agente invoca
sistemas externos diretamente.

*Toolformer* (SCHICK et al., 2023) demonstrou que modelos de linguagem podem aprender
a usar ferramentas de forma autossupervisionada. Essa capacidade, no entanto, introduz
riscos de agência excessiva quando ferramentas poderosas são expostas sem controles de
escopo (OWASP, 2025, LLM08). A Camada de Ação endereça esse risco centralizando o
acesso a ferramentas em um gateway controlado com allowlist explícita por agente.

**Componentes:**

| Componente | Descrição | Exemplos de Implementação |
|---|---|---|
| Tool Gateway | Ponto único de acesso a todas as ferramentas externas. Aplica allowlist por agente, valida schemas de entrada e saída, registra execuções e aplica rate limiting. | LangChain Tools, LangGraph ToolNode |
| Conector de API | Realiza chamadas HTTP a APIs externas com retry, backoff exponencial, timeout e tratamento de erros estruturado. Inclui tratamento de `429` para APIs com throttling (MICROSOFT, 2025). | httpx, requests, aiohttp |
| Conector de Banco de Dados | Executa consultas SQL ou NoSQL com validação de parâmetros, controle de transação e sanitização de entradas para prevenção de SQL injection. | SQLAlchemy, asyncpg, motor |
| Conector de Sistema Corporativo | Integra ERPs, CRMs e sistemas legados via protocolos específicos, com mapeamento de schema e tratamento de inconsistências. | SAP connectors, Salesforce SDK, REST adapters |
| Conector de Sistema de Arquivos | Lê e escreve arquivos em storage local ou remoto com controle de permissão e validação de tipo. | Azure Blob, S3, SharePoint Graph API |
| Validação de Schema | Valida entradas enviadas às ferramentas e saídas recebidas antes de incorporá-las ao contexto do agente. Previne corrupção silenciosa de dados. | Pydantic, JSON Schema, protobuf |

**Responsabilidades:**

- Expor ferramentas aos agentes exclusivamente via Tool Gateway, nunca diretamente
- Aplicar allowlist de ferramentas por agente, domínio e nível de permissão
- Validar schemas de entrada antes de executar qualquer ação externa
- Validar schemas de saída antes de devolver resultados ao contexto do agente
- Implementar retry com backoff exponencial para falhas transientes
- Registrar todas as execuções de ferramentas com entrada, saída, latência e status
- Aplicar circuit breaker para sistemas externos com falhas recorrentes

**Interfaces:**

- *Para cima (Camada 3 — Orquestração)*: recebe solicitações de execução de ferramentas
  com parâmetros tipados; devolve resultados estruturados ou erros normalizados.
- *Para baixo (sistemas externos)*: acessa APIs, bancos de dados, sistemas de arquivos
  e plataformas corporativas conforme autorizações da Camada 2.
- *Para a Camada 8 — Operação*: emite eventos de telemetria para cada execução de
  ferramenta, incluindo latência, status e identificação do agente solicitante.

**Padrões de design:**

O padrão *Toolformer* (SCHICK et al., 2023) inspira a interface de ferramentas: cada
ferramenta é descrita por nome, assinatura e docstring que o modelo usa para seleção.
A validação com Pydantic ou JSON Schema implementa o princípio de *fail fast*: erros
de contrato são detectados antes da execução, não após.

As arquiteturas de referência da AWS (AWS, 2024a; 2024b) tratam a camada de ação como
conjunto de conectores isolados sobre um barramento de eventos, o que facilita
substituição de implementações e testes unitários independentes.

**Decisões de design e trade-offs:**

- Ferramentas de leitura e escrita devem ser separadas; expor apenas leitura para agentes
  que não precisam de modificação segue o princípio de privilégio mínimo (OWASP, 2025, LLM08).
- Idempotência deve ser propriedade explícita de ferramentas que modificam estado; não
  assumir idempotência por padrão — registrar em ADR por ferramenta.
- Resultados de ferramentas incorporados diretamente ao contexto do modelo são vetor
  de *prompt injection* indireta (OWASP, 2025, LLM01); sanitizar antes de inserir no prompt.
- O tamanho do resultado de ferramentas impacta o consumo de tokens; truncar ou resumir
  resultados longos antes de incorporá-los ao contexto.

### 4.5 Camada 5 — Conhecimento

A Camada de Conhecimento fornece a base factual e contextual que fundamenta as respostas
do sistema. Ela combina memória de sessão, recuperação de documentos via RAG e, opcionalmente,
raciocínio sobre grafos de conhecimento estruturado.

O padrão RAG (*Retrieval-Augmented Generation*) de Lewis et al. (2020) demonstrou que
combinar recuperação paramétrica — o conhecimento implícito do modelo — com recuperação
não paramétrica — documentos externos indexados — reduz significativamente a taxa de
alucinação e permite atualização do conhecimento sem re-treinamento do modelo. O
*Self-RAG* (ASAI et al., 2023) estende esse padrão com reflexão adaptativa: o modelo
avalia a relevância de cada trecho recuperado e critica sua própria resposta antes de
finalizá-la.

**Componentes:**

| Componente | Descrição | Exemplos de Implementação |
|---|---|---|
| Contexto de Sessão | Mantém o histórico relevante da conversa atual, com janela de contexto controlada para não exceder limites de tokens do modelo. | Buffer de mensagens, resumo progressivo |
| Memória de Curto Prazo | Armazena fatos e preferências inferidos durante a sessão atual, descartados ao encerrar a conversa. | Redis, variáveis de estado no grafo |
| Memória de Longo Prazo | Persiste conhecimento relevante entre sessões — preferências do usuário, histórico de interações, fatos aprendidos — com controles de acesso e retenção conformes à LGPD (BRASIL, 2018). | PostgreSQL + pgvector, Pinecone, Weaviate |
| RAG — Retrieval | Recupera trechos relevantes de uma base de documentos indexados usando busca vetorial densa, busca esparsa (BM25) ou busca híbrida. | LlamaIndex, Haystack, LangChain Retriever |
| RAG — Reranker | Reordena os trechos recuperados por relevância semântica antes de incorporá-los ao contexto, reduzindo ruído no prompt (ASAI et al., 2023). | Cohere Rerank, cross-encoder, BGE Reranker |
| Knowledge Graph | Representa conhecimento estruturado em triplas (sujeito–predicado–objeto), permitindo consultas relacionais e raciocínio simbólico sobre fatos (HOGAN et al., 2020). | Neo4j, Amazon Neptune, Microsoft GraphRAG (MICROSOFT, 2024c) |

**Responsabilidades:**

- Manter e recuperar contexto de sessão dentro dos limites de tokens do modelo ativo
- Recuperar trechos de documentos relevantes para a intenção classificada pelo orquestrador
- Reordenar trechos recuperados por relevância antes de incorporá-los ao prompt
- Fornecer rastreabilidade de fontes: documento, trecho, versão e data de ingestão
- Detectar ausência de evidência suficiente e sinalizar ao orquestrador para bloqueio ou escalonamento
- Gerenciar ciclo de vida da memória de longo prazo em conformidade com políticas de retenção

**Interfaces:**

- *Para cima (Camada 3 — Orquestração)*: recebe consultas de recuperação com intenção
  e contexto; devolve trechos ranqueados com metadados de proveniência.
- *Para baixo (Camada 7 — Dados)*: acessa índices vetoriais, bancos relacionais, stores
  de grafos e caches para recuperação e persistência.
- *Para a Camada 8 — Operação*: emite métricas de qualidade do retrieval — scores de
  relevância, ausências, conflitos e lacunas de conteúdo.

**Padrões de design:**

O padrão RAG (LEWIS et al., 2020) e sua extensão Self-RAG (ASAI et al., 2023) definem
o ciclo recuperar–avaliar–gerar adotado pelo componente RAG. Os padrões semânticos W3C
— OWL 2 (W3C, 2012), RDF 1.1 (W3C, 2014), SHACL (W3C, 2017) e PROV (W3C, 2013) —
fundamentam a representação formal do Knowledge Graph e os requisitos de rastreabilidade
de proveniência.

As arquiteturas de referência do Google Cloud (GOOGLE, 2024a) documentam variações de
RAG — vetorial, híbrido, GraphRAG e RAG multimodal — com trade-offs de precisão, custo
e latência para cada cenário. O Microsoft GraphRAG (MICROSOFT, 2024c) demonstra ganhos
de qualidade em consultas de alto nível que requerem síntese de múltiplos documentos.

**Decisões de design e trade-offs:**

- Busca vetorial pura pode perder termos exatos relevantes; busca híbrida (densa + esparsa)
  é mais robusta mas tem custo computacional e latência superiores — registrar em ADR.
- O tamanho do chunk impacta precisão e recall do retrieval; chunks menores aumentam
  precisão mas fragmentam contexto; testar com dados reais antes de fixar estratégia.
- Memória de longo prazo requer política explícita de retenção e direito ao esquecimento
  compatível com a LGPD (BRASIL, 2018, Art. 18) — não implementar sem governança de dados.
- Knowledge Graph aumenta qualidade de raciocínio relacional mas eleva complexidade de
  ingestão e manutenção; postergar para após validação do RAG básico em produção.

### 4.6 Camada 6 — Modelos

A Camada de Modelos gerencia o acesso e o uso de modelos de inteligência artificial —
modelos de linguagem de grande escala (LLMs), modelos de embedding, classificadores e
modelos especializados. Ela abstrai a complexidade dos provedores, controla custo e
latência, e garante que o uso de modelos seja rastreável e governado.

A arquitetura Transformer (VASWANI et al., 2017) é a base de todos os Foundation Models
utilizados nesta camada. Compreender seus princípios — atenção multi-cabeça, codificação
posicional, escala de parâmetros — é necessário para tomar decisões informadas sobre
seleção de modelos, parâmetros de geração e trade-offs de custo e qualidade.

**Componentes:**

| Componente | Descrição | Exemplos de Implementação |
|---|---|---|
| Foundation Models | Modelos de linguagem de grande escala usados para geração de texto, raciocínio e resposta ao usuário. | GPT-4o, Claude 3.x, Gemini 1.5, Llama 3 |
| Model Router | Seleciona o modelo mais adequado para cada tarefa com base em critérios de custo, latência, qualidade e domínio — sem expor a decisão ao orquestrador. | LiteLLM, RouteLLM, lógica customizada |
| Embeddings | Modelos que transformam texto em representações vetoriais densas para busca semântica e similaridade na Camada 5. | text-embedding-3-large, Cohere Embed, BGE |
| Classifiers | Modelos leves de classificação para detecção de intenção, domínio, sentimento, risco ou categoria — com latência inferior aos LLMs. | BERT fine-tuned, DistilBERT, modelos Azure AI |
| Fallback | Define a sequência de modelos alternativos acionados quando o modelo primário falha, está indisponível ou excede limites de custo. | LiteLLM fallback config, circuit breaker |
| Gestão de Parâmetros | Controla temperatura, top-p, max_tokens, frequência de penalidade e demais parâmetros de geração por caso de uso, evitando respostas não determinísticas indesejadas. | Configuração por prompt template, DSPy |

**Responsabilidades:**

- Abstrair provedores de modelos para o orquestrador: a Camada 3 solicita geração,
  não especifica o modelo concreto
- Selecionar o modelo adequado para cada tipo de tarefa com base em política configurada
- Registrar para cada chamada: modelo/deployment, versão, tokens de entrada e saída,
  latência e custo estimado
- Aplicar limites de tokens por sessão, agente ou domínio para controle de custo
- Gerenciar fallback em caso de falha, timeout ou limite de rate do modelo primário
- Versionar configurações de modelos, deployments e parâmetros para rastreabilidade

**Interfaces:**

- *Para cima (Camada 3 — Orquestração)*: recebe prompts estruturados com contexto e
  parâmetros; devolve respostas geradas com metadados de uso (tokens, modelo, latência).
- *Para cima (Camada 5 — Conhecimento)*: fornece embeddings para indexação e busca vetorial.
- *Para a Camada 8 — Operação*: emite eventos de telemetria com consumo de tokens, custo
  estimado, latência por modelo e ocorrências de fallback.

**Padrões de design:**

O NIST AI 600-1 (NIST, 2024) cataloga riscos específicos de modelos generativos —
alucinação, viés, uso indevido, inferência de atributos — e orienta controles de
avaliação e monitoramento. O Azure Well-Architected Framework (MICROSOFT, 2024a) define
práticas de otimização de custo para workloads de IA: seleção de modelo por complexidade
de tarefa, prompt caching e uso de modelos menores para tarefas de classificação.

*Self-Consistency* (WANG et al., 2022) e *DSPy* (KHATTAB et al., 2023) informam
estratégias de aumento de robustez: geração de múltiplas respostas com votação e
otimização automática de prompts para reduzir sensibilidade a variações de formulação.

**Decisões de design e trade-offs:**

- Usar o modelo mais capaz para todas as tarefas maximiza qualidade mas eleva custo e
  latência; classificadores e modelos menores devem ser preferidos para tarefas simples —
  registrar política de seleção em ADR.
- Parâmetros de geração como temperatura afetam reprodutibilidade; tarefas que exigem
  respostas determinísticas devem usar temperatura 0 ou mecanismo de cache de prompt.
- Versionamento de modelos deve ser explícito: a mesma query com versões diferentes do
  mesmo modelo pode produzir respostas distintas — incluir versão nos logs de auditoria.
- Prompt caching reduz custo e latência para prompts de sistema longos e estáticos;
  avaliar disponibilidade no provedor escolhido antes de definir estratégia de contexto.

### 4.7 Camada 7 — Dados

A Camada de Dados garante qualidade, disponibilidade, governança e ciclo de vida dos
dados que alimentam e são produzidos pelo sistema de IA. Ela abrange desde a ingestão de
fontes externas até a persistência de logs de auditoria, passando por indexação vetorial,
cache e gerenciamento de eventos.

*Hidden Technical Debt in ML Systems* (SCULLEY et al., 2015) documenta que a maior
parte do código de sistemas de ML não é o modelo em si, mas a infraestrutura de dados ao
redor — pipelines de ingestão, gerenciamento de features e serviços de configuração. Essa
constatação fundamenta o tratamento da Camada 7 como componente de primeira classe, não
como detalhe de implementação.

**Componentes:**

| Componente | Descrição | Exemplos de Implementação |
|---|---|---|
| Pipeline ETL/ELT | Extrai, transforma e carrega dados de fontes externas para o sistema, com rastreabilidade de versão e detecção de mudanças. | Apache Airflow, dbt, Azure Data Factory |
| Vector Store | Armazena e indexa embeddings para busca vetorial eficiente. Suporta filtros por metadados para retrieval governado. | Qdrant, Weaviate, Chroma, pgvector |
| Banco Relacional | Persiste dados estruturados — sessões, usuários, metadados de fontes, logs de handoff e configurações. | PostgreSQL, Azure SQL, SQLite (dev) |
| Cache | Reduz latência e custo de chamadas repetidas a modelos e APIs externas. Requer política de invalidação e TTL explícitos. | Redis, Memcached, Azure Cache for Redis |
| Event Streams | Propaga eventos de interação em tempo real para consumidores de observabilidade, analytics e pipelines de melhoria contínua. | Apache Kafka, Azure Event Hub, Pub/Sub |
| Governança de Dados | Gerencia inventário de fontes, metadados, linhagem, qualidade, retenção e controle de acesso em conformidade com a LGPD (BRASIL, 2018). | Data Catalog, Apache Atlas, políticas customizadas |

**Responsabilidades:**

- Ingerir, normalizar e versionar dados de fontes autorizadas com metadados de proveniência
- Manter índices vetoriais atualizados com os documentos válidos e seus metadados
- Persistir logs de conversas, decisões, fontes, agentes, tokens, custos e eventos de auditoria
- Aplicar políticas de retenção e exclusão de dados pessoais em conformidade com a LGPD
- Fornecer rastreabilidade de linhagem: origem, transformação e uso de cada dado
- Detectar e registrar mudanças em fontes externas para reprocessamento controlado

**Interfaces:**

- *Para cima (Camada 5 — Conhecimento)*: fornece acesso a índices vetoriais, bancos
  relacionais e stores de grafos para recuperação.
- *Para cima (Camada 8 — Operação)*: expõe logs, métricas e eventos para observabilidade
  e auditoria.
- *Para baixo (fontes externas)*: conecta-se a sistemas de origem — SharePoint, APIs,
  bancos legados — via pipeline de ingestão.
- *Para a Camada 2 — Segurança*: aplica controles de acesso e políticas de retenção
  definidos pela camada de governança.

**Padrões de design:**

Os padrões semânticos W3C — PROV (W3C, 2013) para proveniência e RDF/OWL para
representação de metadados — embasam os requisitos de linhagem e rastreabilidade. O
*ML Test Score* (BRECK et al., 2017) propõe testes específicos para dados em sistemas
de ML: cobertura de features, estabilidade de distribuição e monitoramento de skew entre
treino e produção — aplicáveis ao pipeline de ingestão desta camada.

As arquiteturas de referência do Google Cloud (GOOGLE, 2021; 2024b) definem os níveis
de maturidade de MLOps em função da automação dos pipelines de dados: desde ingestão
manual (nível 0) até CI/CD/CT completo com monitoramento de distribuição (nível 2).

**Decisões de design e trade-offs:**

- A escolha do Vector Store impacta escalabilidade, custo e filtragem por metadados;
  avaliar requisitos de filtros compostos antes de selecionar — registrar em ADR.
- Logs de auditoria com dados pessoais devem ter retenção limitada e acesso restrito;
  separar logs operacionais de logs de auditoria desde o design inicial.
- Cache sem política de invalidação é fonte de respostas desatualizadas; definir TTL
  e estratégia de invalidação por tipo de dado antes de habilitar.
- Event Streams introduzem complexidade operacional; para volumes baixos, logs síncronos
  são suficientes — postergar Kafka/Event Hub para quando o volume justificar.

### 4.8 Camada 8 — Operação

A Camada de Operação fornece visibilidade, controle e capacidade de melhoria contínua
sobre todas as outras camadas. Ela instrumenta o sistema com tracing distribuído, coleta
métricas de desempenho e qualidade, gerencia o pipeline de entrega contínua e define os
critérios de prontidão para produção.

Sistemas de IA em produção requerem observabilidade além do que métricas de infraestrutura
tradicionais oferecem: é necessário monitorar a qualidade das respostas geradas, o consumo
de tokens, a taxa de alucinação e o comportamento dos agentes — dimensões inexistentes
em sistemas de software convencionais (SCULLEY et al., 2015; BRECK et al., 2017).

**Componentes:**

| Componente | Descrição | Exemplos de Implementação |
|---|---|---|
| Distributed Tracing | Instrumenta todo o caminho de execução — da requisição à resposta — com spans e traces correlacionados por `trace_id`, usando o padrão OpenTelemetry (OPENTELEMETRY, 2024a). | Jaeger, Tempo, Azure Monitor, Datadog |
| Prompt Logs | Registra prompts enviados e respostas recebidas dos modelos com atributos semânticos padronizados pelo GenAI Semantic Conventions (OPENTELEMETRY, 2024b): modelo, tokens, latência e custo. | OpenTelemetry SDK, Langfuse, Helicone |
| Métricas de Latência | Coleta e agrega percentis de latência (p50, p95, p99) por camada, agente, ferramenta e modelo para definição e monitoramento de SLOs. | Prometheus (PROMETHEUS, 2024), Grafana |
| Cost Tracking | Monitora consumo de tokens e custo estimado por sessão, agente, domínio e período. Habilita alertas de custo anômalo e análise de FinOps de IA. | Relatórios de uso do provedor, métricas customizadas |
| Pipeline CI/CD | Automatiza build, testes, avaliações e deploy de modelos, prompts, agentes e configurações, mantendo rastreabilidade de versões. | GitHub Actions, Azure DevOps, Tekton |
| Avaliação de Qualidade | Mede fidelidade, relevância contextual e grounding das respostas geradas usando frameworks especializados (ES et al., 2023; CONFIDENT AI, 2024; TRUERA, 2024). | RAGAS, DeepEval, TruLens, OpenAI Evals |
| SLO/SLA | Define e monitora objetivos de nível de serviço para disponibilidade, latência, taxa de resolução automática e qualidade de resposta, com alertas de violação. | Prometheus Alertmanager, SLO exporter |
| Admin Console | Interface para gestão operacional: visualização de conversas, auditoria de decisões, análise de lacunas de conteúdo, revisão de amostras e acompanhamento de custos. | Aplicação web customizada, Grafana, Langfuse |

**Responsabilidades:**

- Instrumentar todas as camadas com traces, métricas e logs usando OpenTelemetry como padrão
- Coletar e agregar métricas de qualidade de respostas além de métricas de infraestrutura
- Monitorar custo de tokens por agente, modelo, domínio e período com alertas configuráveis
- Gerenciar o pipeline de entrega de prompts, agentes e configurações como artefatos versionados
- Executar avaliações automatizadas de qualidade no pipeline CI/CD antes de cada deploy
- Definir SLOs mensuráveis e monitorar conformidade em tempo real
- Fornecer interface para revisão humana de amostras, auditoria e análise de lacunas

**Interfaces:**

- *Para cima (todas as camadas)*: coleta telemetria emitida por cada camada via SDK
  OpenTelemetry, sem acoplamento direto.
- *Para baixo (infraestrutura)*: persiste traces, métricas e logs em backends de
  observabilidade na Camada 7.
- *Para o time de operação*: expõe painéis, alertas, relatórios e interface de auditoria
  para gestão contínua do sistema.

**Padrões de design:**

O OpenTelemetry (OPENTELEMETRY, 2024a) é o padrão de instrumentação adotado porque
unifica traces, métricas e logs em um único SDK, com exporters para múltiplos backends
e sem lock-in de fornecedor. O GenAI Semantic Conventions (OPENTELEMETRY, 2024b)
estende o padrão com atributos específicos de IA generativa, habilitando comparabilidade
entre sistemas.

O RAGAS (ES et al., 2023), DeepEval (CONFIDENT AI, 2024) e TruLens (TRUERA, 2024)
formam o conjunto de avaliação de qualidade: RAGAS é especializado em sistemas RAG com
métricas de fidelidade e relevância contextual; DeepEval e TruLens oferecem avaliação
mais ampla de sistemas conversacionais, incluindo grounding, toxicidade e segurança.

O *ML Test Score* (BRECK et al., 2017) organiza critérios de prontidão para produção
em quatro áreas — dados, modelos, infraestrutura de ML e monitoramento — e serve como
rubric de Definition of Done para cada release.

**Decisões de design e trade-offs:**

- OpenTelemetry com exporters configuráveis evita lock-in de observabilidade; investir
  na instrumentação correta desde o início é mais barato que instrumentar retroativamente.
- Avaliação de qualidade no CI/CD requer um conjunto de casos de teste representativos
  com respostas esperadas; construir esse dataset desde o piloto, não depois.
- SLOs muito restritivos aumentam custo de operação (over-engineering de confiabilidade);
  calibrar metas com base em baseline real de uso antes de fixar — registrar em ADR.
- Logs de prompts com dados sensíveis devem ter mascaramento automático antes de
  persistência; não assumir que prompts são inofensivos — aplicar controles da Camada 2.

## 5 Referências

ASAI, Akari; WU, Zeqiu; WANG, Yizhong; SAMNEE, Avirup; ZETTLEMOYER, Luke. **Self-RAG: learning to retrieve, generate, and critique through self-reflection**. arXiv, 2023. arXiv:2310.11511. Disponível em: <https://arxiv.org/abs/2310.11511>. Acesso em: 30 abr. 2026.

AUTIO, Chloe; SCHWARTZ, Reva; DUNIETZ, Jesse; JAIN, Shomik; STANLEY, Martin; TABASSI, Elham; HALL, Patrick; ROBERTS, Kamie. **Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile**. Gaithersburg: NIST, 2024. NIST AI 600-1. Disponível em: <https://doi.org/10.6028/NIST.AI.600-1>. Acesso em: 30 abr. 2026.

AMAZON WEB SERVICES. **AWS Generative AI CDK Constructs**. [S. l.]: AWS, 2024a. Disponível em: <https://github.com/awslabs/generative-ai-cdk-constructs>. Acesso em: 30 abr. 2026.

AMAZON WEB SERVICES. **AWS Generative AI CDK Constructs Samples**. [S. l.]: AWS, 2024b. Disponível em: <https://github.com/aws-samples/generative-ai-cdk-constructs-samples>. Acesso em: 30 abr. 2026.

BASS, Len; CLEMENTS, Paul; KAZMAN, Rick. **Software architecture in practice**. 4. ed. Boston: Addison-Wesley, 2022.

BRASIL. **Lei nº 13.709, de 14 de agosto de 2018: Lei Geral de Proteção de Dados Pessoais (LGPD)**. Brasília, DF: Presidência da República, 2018. Disponível em: <https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/L13709.htm>. Acesso em: 30 abr. 2026.

BRASIL. Congresso Nacional. **Projeto de Lei nº 2.338, de 2023**. Brasília, DF: Congresso Nacional, 2023. Disponível em: <https://www.congressonacional.leg.br/en/materias/materias-bicamerais/-/ver/pl-2338-2023>. Acesso em: 30 abr. 2026.

BRECK, Eric; CAI, Shanqing; NIELSEN, Eric; SALIB, Michael; SCULLEY, D. **The ML test score: a rubric for ML production readiness and technical debt reduction**. In: IEEE INTERNATIONAL CONFERENCE ON BIG DATA, 2017, Boston. **Proceedings…** [S. l.]: IEEE, 2017. Disponível em: <https://research.google/pubs/pub46555/>. Acesso em: 30 abr. 2026.

BROWN, Simon. **The C4 model for visualising software architecture**. [S. l.]: Simon Brown, 2022. Disponível em: <https://c4model.com>. Acesso em: 30 abr. 2026.

CONFIDENT AI. **DeepEval: the open-source LLM evaluation framework**. [S. l.]: Confident AI, 2024. Disponível em: <https://github.com/confident-ai/deepeval>. Acesso em: 30 abr. 2026.

ES, Shahul; JAMES, Jithin; ESPINOSA-ANKE, Luis; SCHOCKAERT, Steven. **RAGAS: automated evaluation of retrieval augmented generation**. arXiv, 2023. arXiv:2309.15217. Disponível em: <https://arxiv.org/abs/2309.15217>. Acesso em: 30 abr. 2026.

GOOGLE. **MLOps: continuous delivery and automation pipelines in machine learning**. [S. l.]: Google Cloud, 2021. Disponível em: <https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning>. Acesso em: 30 abr. 2026.

GOOGLE. **RAG reference architectures**. [S. l.]: Google Cloud, 2024a. Disponível em: <https://cloud.google.com/architecture/rag-reference-architectures>. Acesso em: 30 abr. 2026.

GOOGLE. **Practitioners guide to MLOps: a framework for continuous delivery and automation of machine learning**. [S. l.]: Google Cloud, 2024b. Disponível em: <https://cloud.google.com/resources/mlops-whitepaper>. Acesso em: 30 abr. 2026.

HOGAN, Aidan; BLOMQVIST, Eva; COCHEZ, Michael; D'AMATO, Claudia; DE MELO, Gerard; GUTIERREZ, Claudio; LODI, Sabrina; NAVIGLI, Roberto; NEUMAIER, Sebastian; NGOMO, Axel-Cyrille Ngonga; POLLERES, Axel; RASHID, Sabbir M.; RULA, Anisa; SCHMELZEISEN, Lukas; SEQUEDA, Juan F.; STAAB, Steffen; ZIMMERMANN, Antoine. **Knowledge graphs**. ACM Computing Surveys, v. 54, n. 4, p. 1–37, 2021. arXiv:2003.02320. Disponível em: <https://arxiv.org/abs/2003.02320>. Acesso em: 30 abr. 2026.

INCOSE. **Systems engineering body of knowledge (SEBoK)**. [S. l.]: INCOSE, 2023. Disponível em: <https://sebokwiki.org>. Acesso em: 30 abr. 2026.

KAHNEMAN, Daniel. Maps of bounded rationality: psychology for behavioral economics. **American Economic Review**, v. 93, n. 5, p. 1449–1475, 2003. Arquivo local: [kahneman-2003-maps-bounded-rationality.pdf](fontes/papers/kahneman-2003-maps-bounded-rationality.pdf).

KHATTAB, Omar; SINGHVI, Arnav; MAHESHWARI, Paridhi; ZHANG, Zhiyuan; SANTHANAM, Keshav; VARDHAMANAN, Sri; HATZ, Saiful; LIGER, Ashutosh; ZAHARIA, Matei; POTTS, Christopher; LIANG, Percy. **DSPy: compiling declarative language model calls into self-improving pipelines**. arXiv, 2023. arXiv:2310.03714. Disponível em: <https://arxiv.org/abs/2310.03714>. Acesso em: 30 abr. 2026.

LANGCHAIN. **LangGraph overview**. [S. l.]: LangChain, 2026. Disponível em: <https://langchain-ai.github.io/langgraph/>. Acesso em: 30 abr. 2026.

LEWIS, Patrick; PEREZ, Ethan; PIKTUS, Aleksandra; PETRONI, Fabio; KARPUKHIN, Vladimir; GOYAL, Naman; KÜTTLER, Heinrich; LEWIS, Mike; YIH, Wen-tau; ROCKTÄSCHEL, Tim; RIEDEL, Sebastian; KIELA, Douwe. **Retrieval-augmented generation for knowledge-intensive NLP tasks**. arXiv, 2020. arXiv:2005.11401. Disponível em: <https://arxiv.org/abs/2005.11401>. Acesso em: 30 abr. 2026.

MICROSOFT. **AI workload documentation: Azure Well-Architected Framework**. Redmond: Microsoft, 2024a. Disponível em: <https://learn.microsoft.com/en-us/azure/well-architected/ai/>. Acesso em: 30 abr. 2026.

MICROSOFT. **Responsible AI in Azure workloads**. Redmond: Microsoft, 2024b. Disponível em: <https://learn.microsoft.com/en-us/azure/well-architected/ai/responsible-ai>. Acesso em: 30 abr. 2026.

MICROSOFT. **GraphRAG**. [S. l.]: Microsoft, 2024c. Disponível em: <https://github.com/microsoft/graphrag>. Acesso em: 30 abr. 2026.

MICROSOFT. **Microsoft Graph throttling guidance**. Redmond: Microsoft, 2025. Disponível em: <https://learn.microsoft.com/en-us/graph/throttling>. Acesso em: 30 abr. 2026.

NASA. **NASA systems engineering handbook**. Washington, DC: NASA, 2016. NASA/SP-2016-6105. Disponível em: <https://www.nasa.gov/reference/nasa-systems-engineering-handbook/>. Acesso em: 30 abr. 2026.

NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY. **Artificial Intelligence Risk Management Framework (AI RMF 1.0)**. Gaithersburg: NIST, 2023a. NIST AI 100-1. Disponível em: <https://doi.org/10.6028/NIST.AI.100-1>. Acesso em: 30 abr. 2026.

NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY. **Security and privacy controls for information systems and organizations**. Gaithersburg: NIST, 2020. NIST SP 800-53 Rev. 5. Disponível em: <https://doi.org/10.6028/NIST.SP.800-53r5>. Acesso em: 30 abr. 2026.

NYGARD, Michael T. **Documenting architecture decisions**. [S. l.]: Cognitect, 2011. Disponível em: <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>. Acesso em: 30 abr. 2026.

OPENAI. **OpenAI Evals**. [S. l.]: OpenAI, 2024. Disponível em: <https://github.com/openai/evals>. Acesso em: 30 abr. 2026.

OPENTELEMETRY. **OpenTelemetry documentation**. [S. l.]: OpenTelemetry, 2024a. Disponível em: <https://opentelemetry.io/docs/>. Acesso em: 30 abr. 2026.

OPENTELEMETRY. **Semantic conventions for generative AI systems**. [S. l.]: OpenTelemetry, 2024b. Disponível em: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>. Acesso em: 30 abr. 2026.

OWASP FOUNDATION. **OWASP Top 10 for LLM Applications 2025**. [S. l.]: OWASP GenAI Security Project, 2025. Disponível em: <https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/>. Acesso em: 30 abr. 2026.

PARLAMENTO EUROPEU; CONSELHO DA UNIÃO EUROPEIA. **Regulamento (UE) 2024/1689, de 13 de junho de 2024 (Artificial Intelligence Act)**. Jornal Oficial da União Europeia, 12 jul. 2024. Disponível em: <https://eur-lex.europa.eu/eli/reg/2024/1689/oj>. Acesso em: 30 abr. 2026.

PROMETHEUS. **Prometheus monitoring system**. [S. l.]: Prometheus Authors, 2024. Disponível em: <https://github.com/prometheus/prometheus>. Acesso em: 30 abr. 2026.

SCHICK, Timo; DWIVEDI-YU, Jane; DESSÌ, Roberto; RAILEANU, Roberta; LOMELI, Maria; HAMBRO, Eric; ZETTLEMOYER, Luke; CANCEDDA, Nicola; SCIALOM, Thomas. **Toolformer: language models can teach themselves to use tools**. arXiv, 2023. arXiv:2302.04761. Disponível em: <https://arxiv.org/abs/2302.04761>. Acesso em: 30 abr. 2026.

SCULLEY, D.; HOLT, Gary; GOLOVIN, Daniel; DAVYDOV, Eugene; PHILLIPS, Todd; EBNER, Dietmar; CHAUDHARY, Vinay; YOUNG, Michael; CRESPO, Jean-François; DENNISON, Dan. **Hidden technical debt in machine learning systems**. In: ADVANCES IN NEURAL INFORMATION PROCESSING SYSTEMS, 28., 2015, Montreal. **Proceedings…** [S. l.]: NeurIPS, 2015. Disponível em: <https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems>. Acesso em: 30 abr. 2026.

STARKE, Gernot; HRUSCHKA, Peter. **arc42 template**. [S. l.]: arc42, 2022. Disponível em: <https://arc42.org>. Acesso em: 30 abr. 2026.

TRUERA. **TruLens: evaluation and tracking for LLM experiments**. [S. l.]: TruEra, 2024. Disponível em: <https://github.com/truera/trulens>. Acesso em: 30 abr. 2026.

VASWANI, Ashish; SHAZEER, Noam; PARMAR, Niki; USZKOREIT, Jakob; JONES, Llion; GOMEZ, Aidan N.; KAISER, Łukasz; POLOSUKHIN, Illia. **Attention is all you need**. arXiv, 2017. arXiv:1706.03762. Disponível em: <https://arxiv.org/abs/1706.03762>. Acesso em: 30 abr. 2026.

W3C. **OWL 2 Web Ontology Language document overview**. 2. ed. [S. l.]: W3C, 2012. Disponível em: <https://www.w3.org/TR/owl2-overview/>. Acesso em: 30 abr. 2026.

W3C. **PROV-Overview: an overview of the PROV family of documents**. [S. l.]: W3C, 2013. Disponível em: <https://www.w3.org/TR/prov-overview/>. Acesso em: 30 abr. 2026.

W3C. **RDF 1.1 concepts and abstract syntax**. [S. l.]: W3C, 2014. Disponível em: <https://www.w3.org/TR/rdf11-concepts/>. Acesso em: 30 abr. 2026.

W3C. **Shapes Constraint Language (SHACL)**. [S. l.]: W3C, 2017. Disponível em: <https://www.w3.org/TR/shacl/>. Acesso em: 30 abr. 2026.

WANG, Xuezhi; WEI, Jason; SCHUURMANS, Dale; LE, Quoc; CHI, Ed; NARANG, Sharan; CHOWDHERY, Aakanksha; ZHOU, Denny. **Self-consistency improves chain of thought reasoning in language models**. arXiv, 2022. arXiv:2203.11171. Disponível em: <https://arxiv.org/abs/2203.11171>. Acesso em: 30 abr. 2026.

WEI, Jason; WANG, Xuezhi; SCHUURMANS, Dale; BOSMA, Maarten; ICHTER, Brian; XIA, Fei; CHI, Ed; LE, Quoc; ZHOU, Denny. **Chain-of-thought prompting elicits reasoning in large language models**. arXiv, 2022. arXiv:2201.11903. Disponível em: <https://arxiv.org/abs/2201.11903>. Acesso em: 30 abr. 2026.

YAO, Shunyu; ZHAO, Jeffrey; YU, Dian; DU, Nan; SHAFRAN, Izhak; NARASIMHAN, Karthik; CAO, Yuan. **ReAct: synergizing reasoning and acting in language models**. arXiv, 2022. arXiv:2210.03629. Disponível em: <https://arxiv.org/abs/2210.03629>. Acesso em: 30 abr. 2026.

YAO, Shunyu; YU, Dian; ZHAO, Jeffrey; SHAFRAN, Izhak; GRIFFITHS, Thomas L.; CAO, Yuan; NARASIMHAN, Karthik. **Tree of thoughts: deliberate problem solving with large language models**. arXiv, 2023. arXiv:2305.10601. Disponível em: <https://arxiv.org/abs/2305.10601>. Acesso em: 30 abr. 2026.
