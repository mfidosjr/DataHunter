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
