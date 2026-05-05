# CONOPS - Concept of Operations

## DataHunter

**Arquitetura-alvo:** Python + Streamlit + Groq + DuckDuckGo + Kaggle/HF/Zenodo
**Padrão de referência:** Arquitetura de IA em 8 camadas
**Tipo de sistema:** Sistema de Descoberta e Curadoria de Dados (AI-powered)
**Versão:** 6.9
**Status:** Baseline operacional / Documento de governança
**Classificação:** Pesquisa e Descoberta Técnica
**Canal inicial:** Streamlit Web UI
**Canal futuro:** API de Integração / MCP Server
**Domínio:** Descoberta de Datasets e Curadoria de Conhecimento Externo
**Escopo inicial:** Busca multi-fonte, Expansão semântica e Ranking de relevância
**Público-alvo:** Pesquisadores, Data Scientists e Sistemas de IA (PKGL)

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

## 15. Requisitos Operacionais
