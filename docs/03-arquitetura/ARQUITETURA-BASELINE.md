# Arquitetura Técnica - Baseline Operacional

Este documento detalha a pilha tecnológica (stack) escolhida para a implementação da **Fase 1 (Baseline)** do DataHunter. Estas definições são de natureza técnica e podem evoluir conforme o roteiro operacional definido no [CONOPS](../01-produto/CONOPS.md).

## 1. Pilha Tecnológica Principal

| Camada | Tecnologia Escolhida | Justificativa |
| --- | --- | --- |
| **Execução** | Python 3.10+ | Ecossistema maduro para IA, data science e integração de APIs. |
| **Interface (UI)** | Streamlit | Agilidade na criação de interfaces de dados e validação de protótipos. |
| **Inferência (LLM)** | Groq (Llama 3 70B) | Extrema baixa latência necessária para expansão semântica em tempo real. |
| **Persistência** | SQLite | Local-first, sem necessidade de servidor externo, auditável e portável. |
| **Orquestração** | Multi-threading (Python) | Necessário para realizar buscas paralelas em múltiplos silos simultaneamente. |

## 2. Conectores de Descoberta (Fase 1)

| Fonte | Tecnologia/API | Papel |
| --- | --- | --- |
| **Web Search** | DuckDuckGo API/Scraper | Motor primário para descoberta exaustiva na web aberta. |
| **Datasets** | Kaggle API | Repositório técnico principal para dados de ciência e ML. |
| **AI Assets** | Hugging Face Hub | Localização de modelos e datasets voltados para IA. |
| **Scientific Data** | Zenodo API | Acesso a dados acadêmicos e repositórios de proveniência forte. |

## 3. Protocolos de Integração

*   **Sinais de Confronto**: Payload JSON estruturado para integração com o PKGL.
*   **Contexto Agêntico**: Suporte inicial ao Model Context Protocol (MCP) para uso em IDEs.

## 4. Evolução da Stack

| Item | Alternativa Futura | Gatilho de Mudança |
| --- | --- | --- |
| **Modelos** | Ollama / Local Models | Necessidade de operação 100% offline ou privacidade extrema. |
| **Storage** | Qdrant / ChromaDB | Evolução para busca vetorial complexa e RAG avançado. |
| **Interface** | Next.js / React | Necessidade de UI multiusuário escalável ou customização avançada. |
