# CONOPS - Concept of Operations

## DataHunter

**Arquitetura-alvo:** Ecossistema agêntico local-first (detalhado em [ARQUITETURA-BASELINE](../03-arquitetura/ARQUITETURA-BASELINE.md)).
**Padrão de referência:** Arquitetura de IA em 8 camadas (AIT Standard).
**Tipo de sistema:** Sistema de Descoberta, "Caça" e Curadoria de Dados (AI-powered).
**Versão:** 1.0 (Baseline Conceitual)
**Status:** Baseline operacional / Documento de governança
**Classificação:** Pesquisa, Descoberta Técnica e Apoio à Decisão.
**Canais Iniciais:** Interface de Curadoria (Web) e API Headless (Sistêmica).
**Canais Futuros:** Model Context Protocol (MCP) Server / Extensões de IDE.
**Domínio:** Descoberta de Datasets e Curadoria de Conhecimento Externo para Ecossistemas de IA.
**Escopo:** Orquestração de busca técnica, Expansão semântica e Ranking de autoridade.
**Público-alvo:** Pesquisadores, Engenheiros de Dados e Orquestradores de Conhecimento (PKGL).

> **Como usar este documento:** O CONOPS descreve como o DataHunter é usado, operado e governado do ponto de vista de seus usuários (humanos e sistêmicos). Ele serve como a ponte entre a necessidade de descoberta de dados e a arquitetura técnica de 8 camadas.

## Sumário Executivo

O **DataHunter** é uma capacidade operacional de IA voltada para a automação da descoberta e qualificação de datasets técnicos e científicos. O sistema resolve o problema crítico da fragmentação e lentidão na localização de dados abertos, automatizando a tradução de intenções em linguagem natural para consultas técnicas complexas.

A solução é concebida sob a arquitetura de oito camadas, garantindo que o processo de "caça" de dados seja auditável, rastreável e passível de integração sistêmica. Utilizando LLMs para expansão de query e scoring semântico, o DataHunter não apenas localiza arquivos, mas qualifica sua relevância real, atuando como um fornecedor estratégico de sinais externos para o ecossistema de governança de conhecimento (PKGL).

## Sumário

| # | Seção |
| --- | --- |
| 1 | [Visão e Motivação](#1-visão-e-motivação) |
| 2 | [Modelo Operacional — Interpretar, Refinar, Capturar e Qualificar](#2-modelo-operacional--interpretar-refinar-capturar-e-qualificar) |
| 3 | [Contexto Operacional](#3-contexto-operacional) |
| 4 | [Ambiente Atual](#4-ambiente-atual) |
| 5 | [Justificativa para Mudança](#5-justificativa-para-mudança) |
| 6 | [Ambiente Proposto](#6-ambiente-proposto) |
| 7 | [Atores e Stakeholders](#7-atores-e-stakeholders) |
| 8 | [Conceito de Sistema Multiagentes Gerenciados](#8-conceito-de-sistema-multiagentes-gerenciados) |
| 9 | [Conceito Operacional do Orquestrador](#9-conceito-operacional-do-orquestrador) |
| 10 | [Integração com Fontes de Dados (Kaggle/HF/Zenodo/Web)](#10-integração-com-fontes-de-dados-kagglehfzenodoweb) |
| 11 | [Integração com PKGL (Sinais de Confronto)](#11-integração-com-pkgl-sinais-de-confronto) |
| 12 | [Casos de Uso Operacionais](#12-casos-de-uso-operacionais) |
| 13 | [Cenários Operacionais](#13-cenários-operacionais) |
| 14 | [Painel de Gestão, Observabilidade e Auditoria](#14-painel-de-gestão-observabilidade-e-auditoria) |
| 15 | [Requisitos Operacionais](#15-requisitos-operacionais) |
| 16 | [Segurança, Privacidade e Conformidade](#16-segurança-privacidade-e-conformidade) |
| 17 | [Premissas](#17-premissas) |
| 18 | [Restrições](#18-restrições) |
| 19 | [Critérios de Sucesso do MVP](#19-critérios-de-sucesso-do-mvp) |
| 20 | [Roteiro Operacional (Roadmap)](#20-roteiro-operacional-roadmap) |
| 21 | [Questões Abertas](#21-questões-abertas-e-decisões-pendentes) |
| — | [Pilha Tecnológica (Stack)](../03-arquitetura/ARQUITETURA-BASELINE.md) |
| 22 | [Conclusão](#22-conclusão) |
| — | [Matriz de Rastreabilidade](#rastreabilidade-documental-do-conops) |

---


## 1. Visão e Motivação

### 1.1 O problema que o DataHunter resolve

A descoberta de datasets públicos de alta qualidade é um processo manual, lento e fragmentado. Atualmente, pesquisadores e cientistas de dados precisam navegar individualmente por diversos portais (Kaggle, Hugging Face, Zenodo, repositórios governamentais) e validar manualmente a relevância técnica de cada arquivo encontrado.

O **DataHunter** resolve o "gargalo da descoberta", automatizando a tradução de intenções em linguagem natural para consultas técnicas complexas, realizando buscas paralelas em múltiplas fontes e aplicando critérios de ranqueamento semântico para entregar dados prontos para análise em minutos, não horas.

### 1.2 Princípio de design fundamental: Descoberta Refinada e Assistida por IA

O princípio central do DataHunter é que uma busca bem-sucedida começa com um entendimento profundo da intenção do usuário. Em vez de uma barra de busca estática, o sistema utiliza uma interface conversacional e um motor de expansão de queries que injeta vocabulário técnico de domínio (ex: termos de RF, Clima ou Saúde) automaticamente. 

Além disso, o DataHunter é desenhado para operar como um **Serviço de Descoberta sob Demanda**. Isso significa que ele não apenas atende a usuários humanos via interface, mas também atua como um fornecedor de sinais e evidências externas para outros sistemas de governança (como o PKGL), permitindo ciclos de confronto e validação de conhecimento baseados em contratos explícitos de integração.

### 1.3 Ciclo Operacional de Descoberta de Dados

O funcionamento do DataHunter segue um fluxo cíclico de refinamento e validação:

1.  **Refinamento Conversacional**: O assistente de IA interage com o usuário para extrair keywords técnicas e delimitar o escopo da busca.
2.  **Expansão Inteligente**: O motor gera múltiplas variantes da consulta (em PT e EN) para maximizar o recall em diferentes repositórios.
3.  **Busca e Captura Paralela**: O sistema consulta simultaneamente fontes Web, Kaggle, Hugging Face e Zenodo, validando links e metadados.
4.  **Avaliação e Scoring**: Cada dataset capturado passa por uma análise de qualidade estrutural (nulos, tipos) e uma avaliação de relevância semântica via LLM contra a intenção original.
5.  **Ranqueamento e Entrega**: Os resultados são consolidados em um ranking curado, permitindo o download imediato dos datasets mais relevantes.

---

## 2. Modelo Operacional — Interpretar, Refinar, Capturar e Qualificar

O modelo operacional do DataHunter baseia-se na transformação de uma demanda de informação em um conjunto de evidências validadas e ranqueadas. Ele atua como um sistema de suporte à decisão que segue um ciclo rigoroso de quatro estágios, operando como um componente de "Confronto Externo" para a arquitetura multiagente.

### 2.1 Propósito e Modos de Operação

O sistema opera para atender a dois modos de consumo:
*   **Modo Assistido (UI)**: Focado na experiência humana, onde a fase de Interpretação ocorre via chat conversacional.
*   **Modo Serviço (API/Contrato)**: Focado na integração sistêmica (ex: PKGL), onde a fase de Interpretação recebe queries técnicas ou necessidades de confronto pré-definidas.

### 2.2 Os Quatro Pilares Operacionais

1.  **Interpretar**: Recebe a demanda em linguagem natural ou via contrato sistêmico e extrai a intenção core do usuário/agente.
2.  **Refinar**: Expande a intenção em múltiplas variantes de consulta, injetando vocabulário técnico de domínio e otimizando o plano de busca.
3.  **Capturar**: Executa a busca paralela em repositórios Web e APIs científicas (Kaggle, Zenodo, HF), realizando o download streaming dos arquivos.
4.  **Qualificar**: Aplica scoring estrutural e semântico via LLM, ranqueando os datasets por relevância real em relação à demanda original.

### 2.3 Capacidades Principais (Arquitetura em 8 Camadas)

| Camada | Capacidade | Estágio do Modelo |
| --- | --- | --- |
| **Experiência** | Interface Conversacional | Interpretar |
| **Segurança** | Gestão de Vault/Keys | Capturar |
| **Orquestração** | Engine de Expansão de Query | Refinar |
| **Ação** | Conectores de Repositório | Capturar |
| **Conhecimento** | Ranking de Relevância | Qualificar |
| **Modelos** | LLM Scoring (Llama 3) | Refinar / Qualificar |
| **Dados** | Persistência de Sessão | Interpretar / Qualificar |
| **Operação** | Suite de Avaliação (Golden) | Qualificar |

---

## 3. Contexto Operacional

O DataHunter opera em um ambiente de descoberta e curadoria técnica, onde a velocidade de localização de dados e a precisão da relevância são críticas. Ele funciona como uma ponte entre a necessidade de informação (demanda) e os repositórios globais de dados abertos.

### 3.1 Ambiente de Uso

O sistema é utilizado em contextos de pesquisa científica, análise regulatória e desenvolvimento de modelos de IA. Ele pode ser operado de forma **autônoma** (via interface Streamlit) ou como um **componente escravo** de orquestradores de conhecimento maiores (como o PKGL), que delegam ao DataHunter a tarefa de "caçar" evidências externas para ciclos de confronto de conhecimento.

### 3.2 Usuários e Papéis Operacionais

| Papel | Necessidade Operacional |
| --- | --- |
| **Pesquisador / Data Scientist** | Localizar rapidamente datasets técnicos (ex: RF, Saúde, Clima) sem busca manual exaustiva. |
| **Sistemas Multiagentes (ex: PKGL)** | Acionar o DataHunter para validar uma hipótese interna contra sinais externos da Web/Kaggle. |
| **Analista de Domínio** | Encontrar documentos e tabelas em portais regulatórios (.gov, .edu) usando linguagem natural. |
| **Mantenedor de Tecnologia** | Gerenciar conectores de API e garantir a integridade dos pipelines de download e análise. |

### 3.3 Informação Operada

O sistema processa e transforma as seguintes categorias de informação:
*   **Demandas**: Intenções de busca expressas em linguagem natural.
*   **Variantes Técnicas**: Keywords e termos de domínio gerados via LLM para expansão de query.
*   **Sinais Externos**: Metadados de páginas (título, descrição) e de datasets (votos, licenças, autores).
*   **Artefatos de Dados**: Arquivos capturados em formatos como CSV, JSON, Parquet, NetCDF e ZIP.
*   **Métricas de Qualidade**: Scores estruturais e de relevância semântica gerados pelo pipeline de análise.

### 3.4 Canais e Integrações

| Categoria | Exemplos | Função no Contexto |
| --- | --- | --- |
| **Interface** | Streamlit UI | Canal primário de interação humana e visualização de progresso. |
| **Fontes de Dados** | Kaggle, HF, Zenodo, Web | Repositórios alvos para a "captura" de conhecimento. |
| **Modelos de IA** | Llama 3 (via Groq) | Motor para a "Interpretação", "Refinamento" e "Qualificação". |
| **Sistemas Parceiros** | PKGL | Consumidor principal dos sinais de confronto e evidências externas. |
| **Persistência** | SQLite Local | Cache de buscas e histórico de sessões operacionais. |

### 3.5 Condições Operacionais

*   **Dependência de Credenciais**: O acesso pleno (Kaggle/Zenodo/Groq) requer chaves de API configuradas.
*   **Modo Degradado**: Na ausência de chaves de IA, o sistema opera via busca por palavras-chave puras (sem expansão semântica).
*   **Limites de Captura**: Downloads são limitados (default 80MB) para preservar a estabilidade da infraestrutura local.
*   **Latência de Rede**: A performance da fase de "Capturar" é sensível à disponibilidade e rate limits das fontes externas.

---

## 4. Ambiente Atual

Atualmente, a descoberta de datasets técnicos e científicos (ex: dados de emissores eletromagnéticos, saúde pública ou clima) é um processo predominantemente manual, fragmentado e realizado em silos. O pesquisador ou cientista de dados precisa navegar individualmente por múltiplos portais, validar links, baixar arquivos e avaliar a relevância técnica de forma artesanal.

| Limitação | Impacto |
| --- | --- |
| **Busca Fragmentada** | Alto esforço manual para consultar Kaggle, Hugging Face, Zenodo e portais .gov separadamente. |
| **Baixo Recall Técnico** | Consultas simples não capturam variações terminológicas ou sinônimos técnicos em EN/PT. |
| **Avaliação Cega** | O usuário precisa baixar e processar o arquivo para entender se o conteúdo é realmente relevante. |
| **Inexistência de Scoring** | Resultados são ordenados por popularidade ou data, ignorando a aderência semântica à intenção. |
| **Dificuldade de Proveniência** | Perda de rastro sobre a origem, licença e confiabilidade do dado no momento da coleta. |
| **Isolamento Sistêmico** | Impossibilidade de integração com orquestradores (ex: PKGL) para validação automática de conhecimento. |

---

## 5. Justificativa para Mudança

O DataHunter transforma o "garimpo manual" de dados em uma **capacidade operacional de caça assistida**. A justificativa para a mudança reside na necessidade de escala (lidar com o volume de dados abertos), precisão (filtro semântico) e integração (servir ao ecossistema de governança).

| Necessidade Identificada | Resposta Operacional do DataHunter |
| --- | --- |
| **Centralizar a Descoberta** | Orquestrador de busca paralela que consolida múltiplas fontes em uma única interface/API. |
| **Injetar Inteligência de Domínio** | Engine de expansão de query que utiliza LLMs para garantir que o "alvo" seja encontrado. |
| **Qualificar antes do Consumo** | Uso de Scoring Semântico para filtrar ruído e entregar apenas o que é tecnicamente útil. |
| **Garantir Rastreabilidade** | Registro automático de metadados ricos, fontes e licenças desde o momento da captura. |
| **Habilitar o Confronto Externo** | Fornecimento de sinais e evidências para validar o conhecimento interno de sistemas parceiros. |
| **Medir Eficácia de Busca** | Suite de avaliação (Golden Dataset) para garantir melhoria contínua da precisão da busca. |

Os requisitos funcionais detalhados desta justificativa são mantidos em [02-requisitos/README.md](../02-requisitos/.gitkeep).

---

## 6. Ambiente Proposto

O ambiente proposto introduz o DataHunter como uma infraestrutura centralizada de **descoberta e curadoria técnica automatizada**. Ele atua como uma camada inteligente entre os repositórios globais de dados abertos e as necessidades de informação de humanos e agentes, substituindo o garimpo manual por um pipeline assistido por IA que qualifica o conhecimento externo antes de sua entrega.

### 6.1 Visão Operacional Macro

```text
Usuário Humano / PKGL (Sistema Demandante)
  -> 1. Interpretar: Interface Chat ou Contrato de Integração
  -> 2. Refinar: Expansão semântica e injeção de domínio via LLM
  -> 3. Capturar: Busca paralela massiva (Web, Kaggle, HF, Zenodo)
  -> 4. Qualificar: Scoring semântico, estrutural e ranking de relevância
  -> 5. Fornecer: Entrega de ranking curado, metadados ricos e sinais de confronto
  -> Ecossistema: Modelagem ML, Pesquisa Técnica, Governança de Conhecimento
```

### 6.2 Princípios Operacionais

| Princípio | Aplicação no DataHunter |
| --- | --- |
| **Qualificar antes do Consumo** | Nenhum dataset é entregue sem uma avaliação de relevância semântica contra a demanda. |
| **Transparência de Proveniência** | O sistema preserva o rastro completo de origem, autor e licença de cada arquivo capturado. |
| **Paralelismo por Padrão** | A arquitetura prioriza buscas e downloads simultâneos para reduzir a latência de descoberta. |
| **IA como Filtro de Verdade** | O LLM é usado para validar a aderência do dado real à intenção, não para geração sintética. |
| **Operação sob Demanda (SaaS)** | O sistema funciona como um fornecedor de sinais para orquestradores externos (ex: PKGL). |
| **Melhoria via Golden Dataset** | A precisão da descoberta é medida continuamente contra queries de referência técnica. |

### 6.3 Referência às 8 Camadas

| Camada | Papel no Ambiente Proposto |
| --- | --- |
| **Experiência** | Interface Streamlit (humana) e API de sinais de confronto (sistêmica). |
| **Segurança** | Gestão segura de chaves de API e isolamento de ambientes de download. |
| **Orquestração** | Motor de expansão de query e coordenação do pipeline de busca paralela. |
| **Ação** | Conectores especializados para Kaggle, HF, Zenodo e Web Crawling. |
| **Conhecimento** | Algoritmos de scoring semântico e estrutural para qualificação de dados. |
| **Modelos** | Uso de Llama 3 (via Groq) para interpretação de domínio e análise de metadados. |
| **Dados** | SQLite para persistência de histórico e cache local de metadados capturados. |
| **Operação** | Dashboard de performance de busca e suite de avaliação de recall (Golden Dataset). |

Os requisitos não funcionais e a arquitetura detalhada deste ambiente proposto são mantidos em [03-arquitetura/README.md](../03-arquitetura/.gitkeep).

---

## 7. Atores e Stakeholders

O DataHunter opera em um ecossistema que conecta necessidades humanas de pesquisa a processos automatizados de descoberta técnica. Seus stakeholders incluem desde o usuário final que busca datasets até sistemas orquestradores que dependem de suas evidências para processos de governança de conhecimento e tomada de decisão.

| Ator/Stakeholder | Tipo | Interesse Principal | Responsabilidade no CONOPS |
| --- | --- | --- | --- |
| **Pesquisador / Data Scientist** | Usuário | Localizar datasets técnicos de alta relevância com baixo esforço manual. | Define as intenções de busca e avalia a utilidade final dos dados capturados. |
| **Sistemas Multiagentes (ex: PKGL)** | Usuário Sistêmico | Obter evidências externas e sinais de confronto de forma confiável e automatizada. | Consome os resultados via contrato de integração e os incorpora no ciclo de governança cognitiva. |
| **Analista de Domínio** | Usuário | Validar hipóteses técnicas contra a produção científica e regulatória global. | Realiza a curadoria técnica dos resultados e valida o vocabulário de domínio injetado. |
| **Mantenedor de Tecnologia** | Técnico | Garantir a integridade dos conectores de API e a escalabilidade da busca paralela. | Implementação de novos conectores, gestão de segurança de chaves e sustentação da infraestrutura. |
| **Governança / Compliance** | Governança | Garantir que a captura de dados respeite licenças, proveniência e limites de uso. | Define políticas de rastreabilidade, auditoria de captura e conformidade com termos das fontes. |
| **Gestão Executiva** | Patrocínio | Medir a eficiência operacional na redução do tempo de descoberta e qualidade da informação. | Define prioridades estratégicas, novos domínios de expansão e orçamentos de infraestrutura/API. |

As responsabilidades detalhadas de execução e os papéis técnicos de desenvolvimento são mantidos na [MATRIZ-RACI.md](../00-governanca/.gitkeep).

---

## 8. Conceito de Sistema Multiagentes Gerenciados

No DataHunter, os componentes do pipeline de descoberta são concebidos como **agentes gerenciados**. Isso significa que cada módulo funcional (expansão, busca, captura e qualificação) opera sob um escopo explícito, com limites operacionais definidos e sob a coordenação de um orquestrador central que garante a integridade e a rastreabilidade do processo de "caça" de dados.

### 8.1 Princípios de Gerenciamento dos Agentes

| Princípio | Aplicação Prática no DataHunter |
| --- | --- |
| **Escopo Explícito** | Cada agente atua exclusivamente em sua fase (ex: o Qualificador não realiza buscas na web). |
| **Trilha de Auditoria** | Toda variante gerada, link encontrado e score atribuído deve ser registrado para conferência posterior. |
| **Validação de Contrato** | A saída de um agente (ex: links do Explorador) deve ser validada antes de ser consumida pelo próximo (ex: Captura). |
| **Resiliência e Fallback** | Falhas em conectores específicos ou modelos de IA não devem interromper o ciclo operacional das demais fontes. |
| **Limites de Agência** | Agentes não possuem autonomia para alterar configurações de segurança ou custos de API sem autorização central. |

### 8.2 Agentes e Componentes Previstos

| Agente / Componente | Responsabilidade | Entradas Principais | Saídas Esperadas | Limites Operacionais |
| --- | --- | --- | --- | --- |
| **Orquestrador Central** | Coordenar o fluxo completo e gerenciar o estado da descoberta. | Demanda do usuário, Políticas de busca. | Ranking final, Logs de execução. | Não altera parâmetros de segurança ou limites globais. |
| **Agente Expansor** | Transformar intenção em consultas técnicas multi-idioma. | Intenção core, Vocabulário de domínio. | Variantes técnicas (EN/PT). | Limitado a um range fixo de variantes por query. |
| **Agente Explorador** | Localizar links e capturar metadados em silos globais. | Variantes de query, Fontes autorizadas. | Links de datasets, Metadados ricos. | Respeita rigorosamente rate limits e robots.txt. |
| **Agente de Captura** | Realizar o download e descompressão de artefatos. | Links validados por tipo de arquivo. | Arquivos brutos (CSV, Parquet, etc). | Limite de tamanho por arquivo e validação de extensão. |
| **Agente Qualificador** | Atribuir scores de relevância semântica e qualidade. | Metadados capturados, Intenção original. | Scores (0-100), Descrição semântica. | Baseia-se exclusivamente em evidência capturada. |

O detalhamento dos contratos técnicos entre esses agentes será mantido em [03-arquitetura/CONTRATO-OPERACIONAL-DOS-AGENTES.md](../03-arquitetura/.gitkeep).

---

## 9. Conceito Operacional do Orquestrador

O Orquestrador do DataHunter é o núcleo de inteligência que coordena o pipeline de descoberta técnica. Ele não é apenas um executor sequencial de scripts, mas o componente responsável por gerenciar a complexidade da expansão semântica, a execução paralela massiva e a consolidação de evidências multimodais (web, arquivos e APIs).

### 9.1 Processamento por Complexidade (Sistema 1 e 2)

O orquestrador adota uma lógica de bifurcação operacional baseada na clareza da demanda:
*   **Caminho Direto (Sistema 1)**: Para consultas com termos técnicos explícitos e fontes já conhecidas. O orquestrador minimiza o uso de LLM na fase de refinamento e prioriza a velocidade de captura.
*   **Caminho Profundo (Sistema 2)**: Para intenções em linguagem natural ou domínios novos. O sistema ativa o diálogo de interpretação e a engine de expansão semântica para garantir que nenhum dado relevante seja ignorado por falta de vocabulário técnico.

### 9.2 Grafo Operacional de Alto Nível

```text
START
  -> Interpretar: Extração de intenção via chat ou contrato PKGL
  -> Decidir Rota: Avaliação de complexidade e necessidade de expansão
  -> Refinar: Geração de variantes técnicas (EN/PT) e injeção de domínio
  -> Disparar Captura: Orquestração paralela de agentes exploradores
  -> Monitorar: Gestão de rate limits, timeouts e integridade de download
  -> Qualificar: Execução de scoring semântico e estrutural
  -> Consolidar: Geração de ranking curado e relatório de evidências
END
```

### 9.3 Decisões Críticas de Orquestração

*   **Priorização de Fontes**: O orquestrador aplica uma "heurística de autoridade", priorizando resultados de portais governamentais (.gov), acadêmicos (.edu) e repositórios científicos (Zenodo/HF) no ranking final.
*   **Gestão de Recursos**: Limita o paralelismo (default 10 threads) e o tamanho total de captura por sessão (80MB/arquivo) para garantir a estabilidade operacional em ambientes locais.
*   **Formatação de Sinais**: Quando operando em modo "Serviço" para o PKGL, o orquestrador traduz os achados em "Sinais de Confronto", estruturados para alimentar diretamente os motores de validação de conhecimento do orquestrador parceiro.

---

## 10. Integração com Fontes de Dados (Kaggle/HF/Zenodo/Web)

O DataHunter integra silos globais de dados abertos para permitir uma descoberta unificada e qualificada. Diferente de buscadores genéricos, a integração ocorre sob demanda através de conectores especializados que traduzem a intenção refinada em requisições nativas para cada repositório, garantindo a captura de metadados ricos e proveniência.

### 10.1 Conectores e Repositórios Autorizados

| Fonte | Tipo | Método de Integração | Papel Operacional |
| --- | --- | --- | --- |
| **Web (DuckDuckGo)** | Geral | Scraping de busca + Crawling de contexto | Descoberta de portais regulatórios (.gov), acadêmicos (.edu) e dados abertos dispersos. |
| **Kaggle** | Datasets | Kaggle REST API (`kaggle-api`) | Acesso a datasets curados com estatísticas de download, votos e licenças explícitas. |
| **Hugging Face** | ML/IA | `huggingface-hub` API | Recuperação de datasets voltados para treinamento de modelos, benchmarks e NLP. |
| **Zenodo** | Científico | Zenodo REST API | Localização de dados de pesquisa, papers científicos e benchmarks acadêmicos (CERN/OpenAIRE). |

### 10.2 Princípios de Integração de Fontes

| Princípio | Aplicação no DataHunter |
| --- | --- |
| **Metadado antes de Download** | O sistema valida a descrição semântica e o título antes de iniciar o custo de captura do arquivo bruto. |
| **Preservação de Licença** | Tentativa obrigatória de extração da licença de uso (ex: CC‑BY, MIT, GPL) para garantir conformidade. |
| **Polidez e Rate Limit** | Implementação de retries exponenciais e respeito aos limites das APIs de terceiros para evitar bloqueios. |
| **Fallback Transparente** | Se uma fonte falha ou não possui credencial, o orquestrador a ignora sem interromper o fluxo das demais. |
| **Interoperabilidade de Formatos** | Priorização de formatos abertos e estruturados: CSV, JSON, Parquet, NetCDF, HDF5 e ZIP. |

### 10.3 Gestão de Credenciais e Segurança

As credenciais para fontes autenticadas (Kaggle Key, HF Token, Zenodo Token) são gerenciadas via variáveis de ambiente ou cofre de segredos local. O sistema valida a presença das chaves no início da sessão e ajusta as capacidades dos agentes de captura dinamicamente.

---

## 11. Integração com PKGL (Sinais de Confronto)

O DataHunter atua como o **motor de confronto externo** para o ecossistema PKGL. Esta integração permite que a governança de conhecimento não fique restrita ao que é produzido em sessões isoladas, mas seja continuamente validada contra evidências reais do mundo técnico e científico.

### 11.1 O Conceito de Sinal de Confronto

Um "Sinal de Confronto" gerado pelo DataHunter para o PKGL é um artefato estruturado que contém mais do que links; ele fornece o substrato para a validação de confiança:

| Componente do Sinal | Função Operacional no PKGL |
| --- | --- |
| **Evidência Corroborativa** | Metadados e amostras que confirmam uma premissa ou memória interna. |
| **Ponto de Divergência** | Dados que contradizem o conhecimento interno (ex: novas versões, métricas conflitantes). |
| **Gaps de Disponibilidade** | Registro de que, após busca exaustiva, nenhum dado foi localizado para aquele domínio. |
| **Confidence Score** | Métrica (0-100) baseada na autoridade da fonte e precisão do scoring semântico. |
| **Search Trace ID** | Identificador que permite ao PKGL rastrear exatamente como aquela evidência foi "caçada". |

### 11.2 Fluxo Operacional Sistêmico

O ciclo de integração segue o modelo de **Demanda como Serviço**:

1.  **Gatilho de Confronto**: O orquestrador do PKGL identifica uma dúvida técnica, um artefato de baixa confiança ou um agendamento de revisão e dispara uma requisição para o DataHunter.
2.  **Execução em Background**: O DataHunter recebe a demanda e aciona seu pipeline agêntico (Interpretar -> Refinar -> Capturar -> Qualificar) em modo *headless*.
3.  **Injeção de Evidências**: O ranking curado e os metadados são devolvidos ao PKGL no formato de `References`.
4.  **Atualização Cognitiva**: O PKGL utiliza esses sinais para elevar o status de confiança de uma memória, marcar um conhecimento como obsoleto ou propor uma nova "Unidade de Conhecimento" baseada no achado externo.

### 11.3 Contrato de Serviço e Auditoria

A integração entre os sistemas deve garantir que toda descoberta externa seja auditável. No ambiente proposto, o DataHunter fornece ao PKGL não apenas o dado, mas a **justificativa do achado**, permitindo que o curador humano entenda por que aquela fonte foi considerada relevante para o confronto de conhecimento em questão.

---

## 12. Casos de Uso Operacionais

Os casos de uso operacionais do DataHunter descrevem como o sistema é acionado para resolver o problema da descoberta de dados, tanto por humanos quanto por sistemas orquestradores. Eles detalham o gatilho, os componentes envolvidos e o valor entregue ao final do pipeline.

### 12.1 Casos de Uso da Versão Atual (Baseline)

| ID | Caso de Uso | Gatilho Típico | Componente Principal | Resultado Esperado | Fallback |
| --- | --- | --- | --- | --- | --- |
| **UC-01** | Busca de Dataset Técnico | Pesquisador digita intenção no Streamlit (ex: "dados de RF no Brasil"). | Orquestrador / Expansor | Ranking de datasets curados com scores de relevância e links. | Busca por palavras-chave puras (Web) se as APIs falharem. |
| **UC-02** | Confronto de Conhecimento | PKGL envia demanda técnica para validar memória interna. | Orquestrador / Qualificador | Sinal de Confronto (Evidência/Gap) formatado para o PKGL. | Relatório de "Dados Não Localizados" após busca exaustiva. |
| **UC-03** | Localização Regulátoria | Usuário busca tabelas ou documentos em portais .gov/.edu. | Agente Explorador (Web) | Lista de arquivos diretos e páginas de autoridade regulatória. | Sugestão de refinamento manual de termos de domínio. |
| **UC-04** | Captura e Qualificação | Usuário seleciona item do ranking para inspeção local. | Agente de Captura | Arquivo baixado, descompressão e exibição de metadados ricos. | Alerta de limite de tamanho (>80MB) ou formato não suportado. |
| **UC-05** | Auditoria de Precisão | Mantenedor executa suite de testes de recall técnico. | Operação / Golden Dataset | Relatório comparativo de Precisão/Recall vs Ground Truth técnico. | Log de instabilidade de modelos de IA (Groq/Llama). |

### 12.2 Casos de Uso Candidatos para Evolução

| ID | Caso de Uso | Valor Esperado | Motivo para Fase Posterior |
| --- | --- | --- | --- |
| **UC-F01** | MCP Server Nativo | Permitir que agentes externos (Claude/Cursor) usem o DataHunter como ferramenta. | Necessidade de estabilização do contrato de API de sinais. |
| **UC-F02** | Deep Data Scoring | Analisar amostras internas dos arquivos (CSV/Parquet) para score de fidelidade. | Alto consumo de tokens e latência de processamento atual. |
| **UC-F03** | Monitoramento de Gap | Notificar o PKGL quando novos dados de um domínio "vazio" surgirem na web. | Requer infraestrutura de agendamento e persistência de longo prazo. |

---

## 13. Cenários Operacionais

Os cenários operacionais descrevem como o DataHunter se comporta em condições reais de uso, falha, degradação e integração. Eles definem as expectativas de resiliência do sistema e garantem que a descoberta de dados permaneça auditável mesmo em situações adversas.

### 13.1 Cenários de Operação da Solução

| ID | Cenário | Condição | Comportamento Esperado | Camadas Críticas | Evidência Esperada |
| --- | --- | --- | --- | --- | --- |
| **SC-01** | Operação Nominal | Demanda clara, APIs online e credenciais válidas. | Execução completa do pipeline com ranking de alta relevância e metadados. | Orquestração, Ação, Modelos | Ranking curado, logs de sucesso e arquivos capturados. |
| **SC-02** | Demanda Ambígua | Intenção de busca genérica ou mal formulada. | O sistema solicita esclarecimento (Chat) ou gera variantes amplas para cobrir o campo. | Experiência, Orquestração | Pergunta de esclarecimento na UI e log de variantes amplas. |
| **SC-03** | Falha de Conector | API do Kaggle, HF ou Zenodo retorna erro ou timeout. | O orquestrador isola a falha e prossegue a busca nas demais fontes disponíveis. | Ação, Orquestração | Log de erro do conector e resultado consolidado parcial. |
| **SC-04** | Ausência de IA (Modo Degradado) | Chaves de LLM (Groq) não configuradas ou indisponíveis. | O sistema opera via busca por palavras-chave puras, desativando a expansão semântica. | Segurança, Orquestração | Alerta de "IA Offline" e histórico de busca simplificado. |
| **SC-05** | Limite de Volume | Dataset localizado excede o limite de segurança (default 80MB). | O download é bloqueado preventivamente com notificação de "Tamanho Excedido". | Ação, Dados | Log de auditoria de tamanho e mensagem de alerta na UI. |
| **SC-06** | Demanda PKGL (Headless) | Requisição recebida via contrato de integração sistêmica. | Execução silenciosa (sem UI) com saída exclusiva em JSON de Sinais de Confronto. | Experiência (API), Orquestração | Payload JSON estruturado e ID de rastreabilidade. |
| **SC-07** | Busca Vazia (Gap) | Nenhuma fonte autorizada retorna resultados relevantes. | O sistema gera um relatório de "Gap de Disponibilidade" para o demandante. | Ação, Conhecimento | Log de busca exaustiva e classificação de gap no sinal. |

### 13.2 Cenários de Degradação Controlada

| Situação | Comportamento Aceitável | Comportamento Não Aceitável |
| --- | --- | --- |
| **Instabilidade de LLM** | Fallback para busca léxica (palavras-chave) e heurísticas locais. | Paralisar o pipeline ou exibir erros técnicos brutos ao usuário. |
| **Rate Limit de Fontes** | Aumentar intervalo de retry (backoff) ou suspender fonte temporariamente. | Ignorar limites e causar bloqueio de IP ou revogação de chaves. |
| **Espaço em Disco Crítico** | Limpeza automática de cache de capturas antigas e alerta de manutenção. | Falha silenciosa de escrita que corrompa o banco de histórico. |

---

## 14. Painel de Gestão, Observabilidade e Auditoria

O DataHunter oferece transparência total sobre o processo de "caça" e qualificação de dados. O painel operacional (integrado nativamente na interface Streamlit e disponível via logs estruturados) permite que usuários, gestores e sistemas parceiros acompanhem a eficácia da descoberta e o custo da inteligência aplicada.

### 14.1 Visões Mínimas do Painel

| Visão | Pergunta Operacional Respondida | Público Principal |
| --- | --- | --- |
| **Monitor de Caça** | Quais fontes estão sendo consultadas em tempo real e qual o status dos conectores? | Usuário Final |
| **Ranking Qualificado** | Quais datasets são os mais relevantes e quais evidências sustentam o score atribuído? | Pesquisador / Data Scientist |
| **Log de Auditoria** | Qual variante de query localizou o dado e qual a licença original detectada? | Governança / Compliance |
| **Consumo de IA** | Quantos tokens foram usados para interpretar e qualificar a demanda nesta sessão? | Gestão / Mantenedor |
| **Status de Captura** | Quais downloads foram concluídos, bloqueados por tamanho ou falharam por rede? | Operação Técnica |

### 14.2 Indicadores e Métricas (KPIs)

*   **Eficiência de Recall**: Percentual de fontes autorizadas que retornaram achados úteis para a demanda.
*   **Precisão de Scoring**: Média de relevância semântica dos Top 5 resultados do ranking.
*   **Latência de Descoberta**: Tempo total decorrido entre a intenção original e a entrega do ranking curado.
*   **Custo Operacional de IA**: Volume de tokens processados via Groq para tarefas de NLP por sessão.
*   **Taxa de Sucesso de Captura**: Relação entre links identificados e arquivos efetivamente baixados e validados.

### 14.3 Eventos de Observabilidade e Rastreabilidade

O sistema registra e expõe eventos para cada transição de estado do orquestrador:
*   **Variantes Geradas**: Registro das keywords e termos de domínio injetados pelo Agente Expansor.
*   **Trilha de Origem**: Associação direta entre cada arquivo capturado e a URL/API de proveniência.
*   **Decisões de Filtro**: Justificativa para o bloqueio de downloads (ex: tamanho, extensão não suportada).
*   **Sinal de Saída**: Registro do payload enviado para o PKGL, incluindo o `search_trace_id`.

### 14.4 Regras de Auditoria e Conformidade

Toda descoberta realizada pelo DataHunter deve manter um rastro imutável que permita reconstruir o caminho da caça. Isso inclui a persistência da intenção original, o estado das APIs no momento da busca e o veredito do Agente Qualificador. O objetivo é garantir que a base cognitiva alimentada pelo DataHunter (como no caso do PKGL) possua evidências auditáveis de sua origem externa.

---

## 15. Requisitos Operacionais por Camada

Esta seção consolida os requisitos operacionais essenciais para que o DataHunter entregue seu conceito de descoberta e curadoria governada. O objetivo é garantir que cada camada da arquitetura de IA contribua para a rastreabilidade, segurança e eficácia da descoberta de dados técnicos.

### 15.1 Camada de Experiência

| ID | Requisito Operacional |
| --- | --- |
| **REQ-EXP-01** | O sistema deve permitir ao usuário inserir demandas técnicas em linguagem natural e visualizar rankings curados através de uma interface de curadoria dedicada. |
| **REQ-EXP-02** | Deve exibir feedback em tempo real sobre o progresso das buscas paralelas e o status de cada conector de fonte. |
| **REQ-EXP-03** | Deve possibilitar a visualização detalhada de metadados e a seleção manual de arquivos para download. |
| **REQ-EXP-04** | Deve oferecer uma interface de saída estruturada para integração sistêmica com o PKGL (modo headless). |
| **REQ-EXP-05** | Deve suportar um chat de refinamento para sanar ambiguidades antes do disparo da captura massiva. |

### 15.2 Camada de Segurança

| ID | Requisito Operacional |
| --- | --- |
| **REQ-SEG-01** | O sistema deve operar local-first por padrão, mantendo chaves, histórico e rankings no ambiente do usuário. |
| **REQ-SEG-02** | Deve proteger segredos e tokens de serviços externos fora de arquivos versionados e logs operacionais. |
| **REQ-SEG-03** | Deve implementar bloqueio automático para arquivos executáveis (.exe, .sh) ou de procedência duvidosa. |
| **REQ-SEG-04** | Deve registrar obrigatoriamente a proveniência e o licenciamento de cada dado capturado como requisito de governança. |
| **REQ-SEG-05** | Deve validar permissões e integridade de chaves antes de iniciar orquestrações que gerem custos de tokens. |

### 15.3 Camada de Orquestração

| ID | Requisito Operacional |
| --- | --- |
| **REQ-ORQ-01** | O orquestrador deve coordenar o pipeline completo: Interpretar -> Refinar -> Capturar -> Qualificar. |
| **REQ-ORQ-02** | Deve gerenciar o paralelismo entre múltiplos conectores web e API sem perda de integridade dos resultados. |
| **REQ-ORQ-03** | Deve aplicar a lógica de bifurcação (Sistema 1 e 2) baseada na complexidade da intenção de busca. |
| **REQ-ORQ-04** | Deve implementar gestão de timeouts e retries exponenciais para garantir resiliência contra falhas de fontes externas. |
| **REQ-ORQ-05** | Deve gerar um `Search Trace ID` único para cada sessão, permitindo auditoria ponta-a-ponta dos achados. |

### 15.4 Camada de Ação

| ID | Requisito Operacional |
| --- | --- |
| **REQ-ACA-01** | O sistema deve integrar conectores nativos para motores de busca web e repositórios de dados técnicos (Kaggle, Hugging Face, Zenodo). |
| **REQ-ACA-02** | Deve realizar a captura de metadados técnicos brutos (título, descrição, tags) de cada fonte identificada. |
| **REQ-ACA-03** | Deve aplicar um teto mandatório de download (default 80MB) para evitar esgotamento de recursos locais. |
| **REQ-ACA-04** | Deve suportar captura via streaming para arquivos estruturados, permitindo validação prévia de cabeçalhos. |
| **REQ-ACA-05** | Deve respeitar as políticas de `robots.txt` e os limites de frequência (rate limits) impostos pelos provedores. |

### 15.5 Camada de Conhecimento

| ID | Requisito Operacional |
| --- | --- |
| **REQ-CON-01** | O sistema deve representar achados como objetos de conhecimento ricos em metadados de proveniência e confiança. |
| **REQ-CON-02** | Deve gerar Sinais de Confronto (Evidência/Gap/Divergência) formatados para o grafo de conhecimento do PKGL. |
| **REQ-CON-03** | Deve manter um histórico persistente de rankings e decisões para otimizar futuras caçadas no mesmo domínio. |
| **REQ-CON-04** | Deve classificar a autoridade da fonte (Oficial/Gov, Acadêmica/Edu ou Comunitária) no cálculo do score final. |
| **REQ-CON-05** | Deve extrair e catalogar informações de licenciamento para garantir conformidade no uso dos dados descobertos. |

### 15.6 Camada de Modelos

| ID | Requisito Operacional |
| --- | --- |
| **REQ-MOD-01** | O sistema deve utilizar modelos de linguagem de alta performance para tarefas de expansão semântica e qualificação. |
| **REQ-MOD-02** | Deve registrar o modelo utilizado, tokens consumidos e latência para cada etapa do pipeline agêntico. |
| **REQ-MOD-03** | Deve suportar modo de fallback para busca léxica (palavras-chave) caso os serviços de IA estejam offline. |
| **REQ-MOD-04** | O modelo de qualificação deve obrigatoriamente apontar evidências textuais nos metadados para justificar o score. |
| **REQ-MOD-05** | Deve permitir a troca de provedores de IA (Cloud ou Local) caso a política de segurança do projeto mude. |

### 15.7 Camada de Dados

| ID | Requisito Operacional |
| --- | --- |
| **REQ-DAD-01** | O sistema deve persistir histórico de buscas, rankings e configurações em camada de persistência local auditável. |
| **REQ-DAD-02** | Deve gerenciar o cache temporário de arquivos baixados de forma segura, garantindo limpeza após análise. |
| **REQ-DAD-03** | Deve suportar metadados de versão e integridade (hashes) para os artefatos técnicos capturados. |
| **REQ-DAD-04** | Deve permitir a exportação da base de histórico para fins de backup ou auditoria de governança externa. |

### 15.8 Camada de Operação

| ID | Requisito Operacional |
| --- | --- |
| **REQ-OPE-01** | O sistema deve disponibilizar um monitor de KPIs operacionais (Latência, Eficácia de Recall, Custo de IA). |
| **REQ-OPE-02** | Deve permitir a execução de suites de teste de precisão automatizadas contra um "Golden Dataset" técnico. |
| **REQ-OPE-03** | Deve gerar alertas claros para conectores de fontes offline ou chaves de API com erro recorrente. |
| **REQ-OPE-04** | Deve garantir a reconstrução completa de qualquer ranking ou decisão a partir do Search Trace ID. |

---

## 16. Segurança, Privacidade e Conformidade

O DataHunter deve ser concebido com segurança, privacidade e governança desde o desenho inicial. Como o sistema atua na fronteira entre a necessidade interna de conhecimento e a captura de dados em fontes globais, sua superfície de risco abrange não apenas o armazenamento e APIs, mas também a integridade da proveniência, o respeito ao licenciamento e a proteção contra manipulação de intenções via IA.

As diretrizes desta seção devem ser detalhadas nos documentos de suporte: requisitos testáveis no `docs/02-requisitos/SRS.md`, ameaças em `docs/08-seguranca-lgpd/ameacas/` e riscos em `docs/12-riscos/RISCOS.md`.

### 16.1 Princípios Obrigatórios

| Princípio | Aplicação no DataHunter |
| --- | --- |
| **Local-first** | A orquestração, o ranking e o histórico de caça devem permanecer locais por padrão. |
| **Proveniência** | Todo dado capturado deve possuir URL, API de origem, timestamp e variante de busca rastreável. |
| **Menor Privilégio** | Conectores e agentes de captura devem possuir permissões restritas ao escopo da tarefa atual. |
| **Minimização** | Somente metadados e amostras estritamente necessários para o scoring devem ser processados. |
| **Supervisão Humana** | Downloads de grande volume ou fontes de baixa autoridade exigem validação explícita. |
| **Reversibilidade** | Ações de limpeza de cache ou deleção de histórico devem ser auditáveis e controladas. |

### 16.2 Dados Pessoais e Conformidade (LGPD)

| Controle | Requisito Operacional |
| --- | --- |
| **Finalidade** | A busca de dados deve estar vinculada a uma intenção técnica ou científica explícita. |
| **Dados Sensíveis** | Identificação e sinalização de datasets que possam conter PII (Personally Identifiable Information). |
| **Retenção** | Política de limpeza automática de arquivos temporários e caches de download não catalogados. |
| **Rastreabilidade** | Localização imediata da origem de qualquer dado questionado por questões de privacidade ou licença. |
| **Acesso** | Proteção de logs de busca que possam revelar estratégias ou áreas de pesquisa sensíveis. |

### 16.3 Segurança de IA Generativa e Agentes

| Risco | Controle Esperado |
| --- | --- |
| **Prompt Injection** | Isolamento entre as instruções de sistema do Agente Expansor e a intenção de busca do usuário. |
| **Alucinação de Fonte** | Proibição de geração de links sintéticos; validação obrigatória de existência via HEAD request. |
| **Vazamento de Demanda** | Proteção de intenções de busca sensíveis (ex: projetos confidenciais) em chamadas de API externas. |
| **Agência Excessiva** | Bloqueio de navegação profunda em sites não autorizados ou execução de scripts de crawling agressivos. |
| **Alucinação de Qualidade** | Exigência de que o Agente Qualificador aponte o trecho exato do metadado que justifica o score. |
| **Dependência de Provedor** | Garantia de fallback para busca léxica (keywords) caso o provedor de LLM (Groq) falhe. |

### 16.4 O que o Sistema Não Deve Fazer

O DataHunter não deve:
*   Transformar toda busca web em um sinal de confiança automática.
*   Executar ou interpretar scripts e binários contidos nos arquivos capturados.
*   Compartilhar ou persistir chaves de API em logs ou artefatos distribuídos.
*   Ignorar metadados de licença (ex: CC‑BY‑ND) ao sugerir o uso de um dataset.
*   Operar como um proxy anônimo para atividades não relacionadas à descoberta de dados.
*   Consolidar rankings baseados puramente em popularidade, sem critério de autoridade (.gov/.edu).

### 16.5 Incidentes e Auditoria

Eventos de falha de conector, detecção de arquivos maliciosos, vazamento de demanda ou erro grave de qualificação devem ser registrados e classificados. Cada incidente deve permitir reconstruir:
*   A intenção original que disparou a caça.
*   As variantes de busca geradas pela IA.
*   Os conectores e agentes envolvidos na falha.
*   A URL/Fonte externa que causou o alerta ou incidente.

### 16.6 Métricas de Segurança e Governança

| Métrica | Finalidade |
| --- | --- |
| **% de Fontes com Proveniência** | Medir a auditabilidade da base de achados. |
| **Bloqueios por Extensão/Tamanho** | Avaliar a eficácia dos filtros preventivos de captura. |
| **Incidentes de IA (Alucinação)** | Monitorar casos onde links gerados pela IA não foram validados. |
| **Uso de API com Política Ativa** | Garantir que 100% das chamadas externas seguem as regras de escopo. |

---

## 17. Premissas

As premissas são condições assumidas como verdadeiras para orientar o desenho e a operação do DataHunter. Elas não são garantias absolutas: caso uma premissa deixe de ser válida, o impacto deve ser tratado como risco ou necessidade de ajuste no roadmap e na arquitetura.

### 17.1 Premissas de Produto e Operação

| ID | Premissa |
| --- | --- |
| **PR-OP-01** | O pesquisador técnico valoriza a autoridade da fonte e a exaustividade da descoberta acima da simplicidade de busca. |
| **PR-OP-02** | A primeira entrega será focada em pesquisadores individuais e sistemas agênticos (PKGL) em ambiente controlado. |
| **PR-OP-03** | A qualificação semântica (scoring) é o principal diferencial em relação a motores de busca genéricos. |
| **PR-OP-04** | O valor operacional é demonstrado pela redução do tempo de localização de evidências técnicas e científicas. |

### 17.2 Premissas de Canais e Experiência

| ID | Premissa |
| --- | --- |
| **PR-CAN-01** | A interface de curadoria via web é suficiente para a validação do conceito e uso humano no ciclo inicial. |
| **PR-CAN-02** | A integração sistêmica via API Headless é a premissa para o funcionamento do ecossistema de governança. |
| **PR-CAN-03** | O usuário precisa de visibilidade sobre o "raciocínio" de expansão da IA para confiar nos resultados do ranking. |

### 17.3 Premissas Tecnológicas

| ID | Premissa |
| --- | --- |
| **PR-TEC-01** | O provedor de inferência manterá a latência baixa o suficiente para permitir expansão semântica em tempo real. |
| **PR-TEC-02** | A arquitetura de conectores modulares permitirá a injeção de novas APIs de dados sem alteração no núcleo. |
| **PR-TEC-03** | O uso de processamento paralelo é mandatório para a viabilidade da busca em múltiplos silos. |
| **PR-TEC-04** | Modelos de linguagem de tamanho médio (ex: 70B) são suficientes para tarefas de qualificação de metadados técnicos. |

### 17.4 Premissas de Dados e Conhecimento

| ID | Premissa |
| --- | --- |
| **PR-DAD-01** | Os metadados brutos (título, descrição, tags) são substrato suficiente para um scoring semântico de alta precisão. |
| **PR-DAD-02** | O licenciamento detectado é tratado como "Best Effort" e deve ser validado pelo curador humano no destino final. |
| **PR-DAD-03** | O histórico de buscas servirá como base para evitar redundância de processamento e consumo de tokens de inferência. |

### 17.5 Premissas de Integração e Ecossistema

| ID | Premissa |
| --- | --- |
| **PR-INT-01** | O DataHunter atua como um provedor de "Sinais de Confronto" independente, sem depender do estado do PKGL. |
| **PR-INT-02** | O Model Context Protocol (MCP) será o padrão adotado para a distribuição de descobertas para IDEs e Agentes Claude/GPT. |
| **PR-INT-03** | Falhas em conectores externos serão tratadas como degradação parcial, nunca como falha total do orquestrador. |

### 17.6 Premissas de Segurança e Governança

| ID | Premissa |
| --- | --- |
| **PR-SEG-01** | O usuário é o detentor das chaves de API (ByoK) e responsável pelo custo de tokens associado às suas buscas. |
| **PR-SEG-02** | O sistema deve preservar a privacidade das intenções de busca, não compartilhando demandas entre usuários ou sessões. |
| **PR-SEG-03** | A rastreabilidade via Trace ID é a premissa básica para a auditoria de qualquer conhecimento derivado do DataHunter. |

---

## 18. Restrições

Restrições são limites obrigatórios para a primeira entrega e para a evolução controlada do DataHunter. Diferente das premissas, elas não são hipóteses: devem ser tratadas como regras de contorno. Qualquer alteração relevante deve gerar decisão arquitetural, atualização de requisitos ou revisão de risco.

### 18.1 Restrições de Escopo da Primeira Entrega

| ID | Restrição |
| --- | --- |
| **RT-ESC-01** | A primeira entrega deve focar exclusivamente em descoberta via web e repositórios abertos, sem suporte inicial a scraping de sites de acesso restrito. |
| **RT-ESC-02** | O sistema não deve tentar realizar o download de arquivos que exijam autenticação manual (captcha) ou fluxos de subscrição paga. |
| **RT-ESC-03** | A interface de usuário inicial deve garantir agilidade na validação operacional através de frameworks leves de UI. |

### 18.2 Restrições Tecnológicas

| ID | Restrição |
| --- | --- |
| **RT-TEC-01** | O núcleo de orquestração deve permanecer independente de provedores de infraestrutura cloud proprietária (Cloud Agnostic). |
| **RT-TEC-02** | O uso de uma camada de persistência local leve é mandatório para o MVP, visando simplicidade e portabilidade. |
| **RT-TEC-03** | Toda integração com APIs de IA deve possuir mecanismos de timeout e fallback explícitos para evitar travamentos do orquestrador. |

### 18.3 Restrições de Dados e Conhecimento

| ID | Restrição |
| --- | --- |
| **RT-DAD-01** | Arquivos identificados como executáveis (.exe, .sh, .bin) ou scripts não devem ser processados ou baixados pelo sistema. |
| **RT-DAD-02** | O limite de 80MB por download individual é mandatório para preservar a integridade da infraestrutura local do usuário. |
| **RT-DAD-03** | Achados que não possuam URL de proveniência ou fonte verificável não devem ser incluídos nos rankings qualificados. |

### 18.4 Restrições de Segurança, Privacidade e Conformidade

| ID | Restrição |
| --- | --- |
| **RT-SEG-01** | Segredos, tokens e chaves de API não devem ser persistidos no banco de dados de histórico ou em logs operacionais. |
| **RT-SEG-02** | O sistema deve respeitar as diretrizes de `robots.txt` e não deve contornar proteções de acesso impostas pelos sites de origem. |
| **RT-SEG-03** | Os dados brutos baixados para fins de qualificação técnica devem ser tratados como temporários e limpos periodicamente. |

### 18.5 Restrições de Integração

| ID | Restrição |
| --- | --- |
| **RT-INT-01** | A saída de dados para o PKGL deve seguir rigorosamente o esquema JSON do "Contrato de Sinais de Confronto". |
| **RT-INT-02** | Falhas de conexão em uma fonte específica (ex: Kaggle offline) não devem impedir a conclusão da busca nas demais fontes. |
| **RT-INT-03** | O sistema não deve exigir privilégios de administrador do sistema operacional para sua execução padrão. |

---

## 19. Critérios de Sucesso da Solução

Os critérios de sucesso definem quando o DataHunter entrega valor real como uma solução de descoberta e curadoria governada, indo além da simples funcionalidade técnica. O MVP é a base de validação para os mecanismos essenciais de "caça" agêntica.

### 19.1 Critérios de Prontidão do MVP

| Critério | Meta Inicial Sugerida | Evidência |
| --- | --- | --- |
| **Operação Local-first** | Execução completa em ambiente local sem dependência de persistência cloud. | Logs de execução e banco SQLite populado localmente. |
| **Descoberta Multi-fonte** | Integração funcional de Web (DDG) e pelo menos uma API técnica (Kaggle/HF). | Ranking consolidado com achados de origens distintas. |
| **Orquestração Agêntica** | Uso de Sistema 1 e 2 para expansão semântica e qualificação. | Trace ID registrando as variantes de busca e scores atribuídos. |
| **Handoff Sistêmico** | Geração de payload JSON no formato de "Sinais de Confronto". | Arquivo ou endpoint JSON validado pelo esquema do PKGL. |

### 19.2 Critérios de Sucesso Operacional

| Critério | Meta Inicial Sugerida | Evidência |
| --- | --- | --- |
| **Eficácia de Recall** | Presença de fontes de alta autoridade (.gov, .edu, Zenodo) em 80% das buscas. | Relatório de fontes por categoria de autoridade. |
| **Latência de Ranking** | Tempo total de geração de ranking qualificado inferior a 60 segundos. | Métricas de latência registradas por Trace ID. |
| **Precisão Semântica** | Score de relevância superior a 0.7 para o Top 3 (validação humana). | Logs de qualificação com justificativa textual da IA. |
| **Resiliência de Captura** | Taxa de sucesso em downloads e extração de metadados superior a 90%. | Relatório de erros e retries dos conectores. |

### 19.3 Critérios de Maturidade e Governança

| Critério | Meta Inicial Sugerida | Evidência |
| --- | --- | --- |
| **Monitoramento de KPIs** | Dashboard ou CLI exibindo Latência, Recall e Consumo de Tokens. | Interface de operação com indicadores ativos. |
| **Rastreabilidade Total** | 100% dos achados vinculados a uma URL de proveniência e Trace ID. | Consulta auditável no banco de dados SQLite. |
| **Conformidade de Licença** | Detecção e sinalização automática de licenças em 70% dos datasets capturados. | Campo de licença preenchido nos metadados do ranking. |
| **Governança Documental** | Sincronia total entre CONOPS, SRS e matriz de riscos. | Matriz de rastreabilidade documental atualizada. |

### 19.4 Critérios de Segurança e Conformidade

| Critério | Meta Inicial Sugerida | Evidência |
| --- | --- | --- |
| **Proteção de Segredos** | Zero ocorrências de chaves de API em arquivos versionados ou logs. | Checklist de auditoria de segredos e varredura de repositório. |
| **Filtro de Integridade** | 100% de bloqueio para extensões executáveis (.exe, .sh, .bin). | Logs de rejeição do conector de download. |
| **Minimização de Dados** | Limpeza de caches temporários de download após 24h de inatividade. | Rotina de limpeza automática verificada. |
| **Validação de Links** | 100% dos links reportados validados via HTTP HEAD para evitar alucinações. | Log de validação prévia ao ranking. |

### 19.5 Critérios Bloqueantes

A solução não deve ser considerada estável ou avançar para fases de maior automação se ocorrer uma ou mais das condições abaixo:
*   Achados incluídos no ranking qualificado sem URL de proveniência verificável.
*   Exposição de chaves de API (Groq, Kaggle, etc.) em qualquer artefato persistente ou log.
*   Download de arquivos que excedam o teto de 80MB sem autorização explícita do usuário.
*   Consolidação de rankings baseada em "alucinações" de modelos (links inexistentes gerados pela IA).
*   Falha na geração de Sinais de Confronto que respeitem o contrato sistêmico com o PKGL.

---

## 20. Roteiro Operacional da Solução

O roteiro operacional organiza a evolução do DataHunter, partindo de uma primeira entrega funcional de busca técnica até uma solução madura de descoberta agêntica integrada ao ecossistema de governança. Ele não substitui o roadmap detalhado, mas explicita a lógica de amadurecimento e os critérios de passagem entre fases.

### 20.1 Fases de Evolução

| Fase | Objetivo Operacional | Capacidades Principais | Evidência de Saída |
| --- | --- | --- | --- |
| **Fase 0 - Fundação** | Consolidar a visão e governança inicial do projeto. | CONOPS, SRS inicial, Matriz de Riscos e Estrutura AIT. | Documentos sincronizados e commitados. |
| **Fase 1 - Baseline** | Provar a busca multi-fonte via interface de curadoria inicial. | Orquestrador Sistema 1/2, Conectores iniciais, Scoring semântico via LLM. | Ranking curado com Trace ID e proveniência. |
| **Fase 2 - Expansão** | Ampliar a base de descoberta para repositórios técnicos globais. | Conectores nativos para Hugging Face, Zenodo e portais governamentais. | Diversidade de fontes em buscas complexas. |
| **Fase 3 - Sinais** | Estabelecer a integração sistêmica estável com o PKGL. | API Headless, payload de "Sinais de Confronto", contrato JSON. | Consumo automatizado de achados pelo grafo PKGL. |
| **Fase 4 - MCP** | Tornar o DataHunter um provedor de contexto para o trabalho de dev/pesquisa. | Model Context Protocol (MCP) Server, integração com Cursor/Agentes. | Uso do DataHunter direto em IDEs e chats de IA externos. |
| **Fase 5 - Deep Score** | Aumentar a fidelidade do ranking via inspeção interna dos dados. | Análise de amostras (inspeção de CSV/JSON), estatísticas de fidelidade. | Score de relevância baseado em conteúdo real, não apenas metadados. |
| **Fase 6 - Maturidade** | Operar como infraestrutura de descoberta para múltiplos sistemas. | Ecossistema maduro, monitoramento pleno de KPIs, governança total. | Produto operacional estável com métricas de recall e custo. |

### 20.2 Critérios de Passagem entre Fases

Uma fase só deve avançar para a seguinte quando:
*   As evidências de saída da fase atual estiverem registradas e auditáveis.
*   Riscos críticos associados às capacidades da fase foram mitigados.
*   Os requisitos operacionais (Item 15) foram revisados e atualizados.
*   Métricas mínimas de sucesso (Item 19) foram coletadas e analisadas.
*   O fallback para o modo de operação degradado foi testado e validado.

### 20.3 Relação com a Governança Documental

| Documento | Papel no Roteiro |
| --- | --- |
| **CONOPS** | Orientar a visão e a lógica operacional de longo prazo. |
| **SRS** | Detalhar os requisitos técnicos para implementação em cada fase. |
| **RISCOS.md** | Monitorar os gatilhos e mitigações que podem atrasar o roteiro. |
| **PLANO-AVALIACAO.md** | Definir as métricas de qualidade para declarar uma fase como concluída. |

### 20.4 Princípios de Evolução

O DataHunter deve evoluir preservando os seguintes pilares:
1.  **Local-first como Base de Confiança**: A operação principal não deve depender de persistência cloud obrigatória.
2.  **Autoridade sobre Popularidade**: O algoritmo de ranking deve sempre priorizar fontes oficiais e verificáveis.
3.  **Interoperabilidade via Contratos**: Integrações devem seguir padrões abertos (JSON, MCP, APIs rest).
4.  **Transparência Semântica**: O usuário deve sempre saber por que um dado foi classificado como relevante.
5.  **Segurança By Design**: Novos conectores ou capacidades devem nascer com os filtros de integridade (Item 16) ativos.

---

## 21. Questões Abertas e Decisões Pendentes

Questões abertas são decisões ainda não estabilizadas que podem afetar o escopo, a arquitetura, a segurança ou o roadmap do DataHunter. Elas não devem permanecer indefinidamente no CONOPS: cada questão precisa ter um destino documental, um critério de fechamento e, quando aplicável, um risco ou ADR associado.

### 21.1 Questões Prioritárias

| ID | Questão Aberta | Impacto se não Decidir | Destino da Decisão | Critério de Fechamento |
| --- | --- | --- | --- | --- |
| **Q-01** | Qual o melhor modelo de persistência para caches de datasets de longo prazo? | Afeta o custo de storage e a performance de re-ranking. | `docs/04-dados/` | Definição de política de cache e storage engine. |
| **Q-02** | Suporte a modelos locais (Ollama) para qualificação em ambientes offline. | Afeta a premissa de soberania total e requisitos de hardware. | `docs/06-modelos/` | Validação de performance do Llama 3 local vs API. |
| **Q-03** | Granularidade dos Sinais de Confronto enviados para o PKGL. | Afeta a utilidade dos achados para a curadoria do grafo. | `docs/09-integracoes/` | Contrato JSON finalizado e testado com o PKGL. |
| **Q-04** | Implementação de agentes de "deep research" (multi-hop links). | Afeta a latência e o risco de bloqueio de IP/Rate limits. | `docs/05-agentes/` | Teste de viabilidade técnica e definição de profundidade. |
| **Q-05** | Estratégia de gestão de custos de tokens para uso multiusuário. | Afeta a sustentabilidade financeira e cotas de uso. | `docs/10-operacao/` | Implementação de contador de tokens e limites por Trace ID. |

### 21.2 Regras de Gestão das Questões

| Regra | Aplicação |
| --- | --- |
| **Questão sem owner vira risco** | Se não houver responsável por fechar a decisão, ela deve ser registrada em `docs/12-riscos/RISCOS.md`. |
| **Questão técnica vira ADR** | Se a decisão alterar a arquitetura ou contrato, deve gerar um *Architecture Decision Record* (ADR). |
| **Questão de escopo vira backlog** | Se afetar a entrega de uma fase, deve ser registrada como item de backlog técnico. |
| **Questão de segurança vira controle** | Se afetar privacidade ou exposição, deve gerar um novo controle em `docs/08-seguranca-lgpd/`. |

### 21.3 Critérios para Remover uma Questão do CONOPS

Uma questão pode ser removida desta seção quando:
1.  A decisão final estiver formalmente registrada no documento de destino indicado.
2.  Houver um responsável (owner) claro pela implementação da decisão.
3.  Os impactos em requisitos, arquitetura e riscos tiverem sido propagados para os documentos correlatos.
4.  A decisão puder ser verificada por evidência técnica ou teste operacional.

---

## 22. Conclusão

O DataHunter propõe uma camada agêntica e governada para a descoberta de evidências externas e datasets técnicos, essencial para o amadurecimento de ecossistemas de IA local-first. Sua finalidade não é ser apenas mais um motor de busca, mas sim o braço operacional de "caça" que preenche a lacuna entre a necessidade de conhecimento e a localização de fontes de alta autoridade (.gov, .edu, Zenodo, Kaggle).

A tese central deste CONOPS é que, em um ambiente de governança cognitiva (liderado pelo PKGL), a descoberta de dados não pode ser um processo manual, disperso e sem proveniência. Sem o DataHunter, pesquisadores e sistemas de IA permanecem limitados ao conhecimento já persistido ou a buscas web superficiais e alucinatórias. Com o DataHunter, a descoberta passa a ter ciclo de vida, score de relevância, rastro de auditoria (Trace ID) e integração sistêmica via Sinais de Confronto.

O desenho operacional adotado separa a **Baseline Operacional** da ambição total do produto. A primeira entrega foca na eficácia da busca multi-fonte via Streamlit, garantindo segurança (bloqueio de executáveis), transparência (justificativa de score) e interoperabilidade (JSON para PKGL). A solução completa, por sua vez, evolui para a integração massiva de repositórios globais, o fornecimento de contexto via Model Context Protocol (MCP) e o "Deep Scoring" baseado na inspeção real dos dados capturados.

Essa evolução só é aceitável se preservar os princípios definidos neste documento: soberania local-first, priorização da autoridade sobre a popularidade, minimização de riscos de IA e rastreabilidade documental rigorosa. O DataHunter deve crescer como um serviço confiável sem perder o controle sobre a procedência de cada sinal que injeta no ecossistema.

As próximas etapas recomendadas para o projeto são:
*   Manter a sincronização contínua entre este CONOPS e os documentos de suporte (SRS, Riscos, Segurança).
*   Transformar os critérios de sucesso e requisitos por camada em testes operacionais verificáveis.
*   Estabelecer os contratos de dados e eventos para a API Headless de integração com o PKGL.
*   Fechar as questões abertas priorizadas (Q-IDs) antes de avançar para a Fase 2 do roteiro.
*   Preparar o terreno tecnológico para a implementação do MCP Server como padrão de distribuição.

Conclui-se que o DataHunter deve ser tratado como uma infraestrutura crítica de descoberta técnica. Seu valor reside em permitir que humanos e agentes confrontem suas bases internas com a vastidão de dados externos de forma qualificada, reduzindo o risco de alucinação, aumentando a base de evidências e preservando a soberania cognitiva do usuário ao longo de todo o pipeline de pesquisa.

---

## Rastreabilidade Documental do CONOPS

| Item do CONOPS | Documento de Detalhamento |
| --- | --- |
| 1-7 (Visão e Contexto) | `README.md` |
| 8-9 (Multiagentes e Orquestrador) | `docs/03-arquitetura/ARCHITECTURE.md` |
| 10-11 (Integrações) | `docs/09-integracoes/CONTRACTS.md` |
| 12-13 (Casos e Cenários) | `docs/07-llmops/avaliacao/TEST_PLANS.md` |
| 14-15 (Gestão e Requisitos) | `docs/02-requisitos/SRS.md` |
| 16 (Segurança) | `docs/08-seguranca-lgpd/CONTROLS.md` |

---

## Histórico de Versões

| Versão | Data | Autor | Descrição |
| --- | --- | --- | --- |
| 0.1 | 2026-05-05 | Antigravity | Estrutura inicial e migração para pastas AIT. |
| 1.0 | 2026-05-05 | Antigravity | Baseline completa (Items 1-22) alinhada ao PKGL e AIT-Template. |
