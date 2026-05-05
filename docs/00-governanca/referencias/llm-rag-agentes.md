# LLM, RAG, Agentes e Avaliação

> Papers como base conceitual — valide antes de produção. Frameworks e ferramentas: verifique licença, manutenção e segurança.

### Raciocínio e prompting

| Referência | Tipo | Uso | Link |
| --- | --- | --- | --- |
| Chain-of-Thought Prompting | Paper | Raciocínio passo a passo e limitações de prompting. | [local](fontes/papers/chain-of-thought-prompting-2201.11903.pdf) / https://arxiv.org/abs/2201.11903 |
| Self-Consistency Improves CoT | Paper | Amostragem de múltiplos caminhos de raciocínio. | [local](fontes/papers/self-consistency-cot-2203.11171.pdf) / https://arxiv.org/abs/2203.11171 |
| Tree of Thoughts | Paper | Exploração de múltiplos caminhos de raciocínio. | [local](fontes/papers/tree-of-thoughts-2305.10601.pdf) / https://arxiv.org/abs/2305.10601 |
| DSPy | Paper/Framework | Programação e otimização de pipelines com LMs. | [local](fontes/papers/dspy-2310.03714.pdf) / https://arxiv.org/abs/2310.03714 |
| Anthropic Prompt Engineering Guide | Guia | Técnicas de prompting, encadeamento, caching e otimização para modelos Claude. | [local](fontes/llm-rag-agentes/docs-anthropic-com-en-docs-build-with-claude-prompt-engineering-overview.pdf) / https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview |
| OpenAI Prompt Engineering Guide | Guia | Estratégias práticas: instruções claras, CoT, few-shot e referências externas. | [local](fontes/llm-rag-agentes/platform-openai-com-docs-guides-prompt-engineering.pdf) / https://platform.openai.com/docs/guides/prompt-engineering |

### Agentes e ferramentas

| Referência | Tipo | Uso | Link |
| --- | --- | --- | --- |
| ReAct: Synergizing Reasoning and Acting | Paper | Intercalar raciocínio e ação/ferramentas. | [local](fontes/papers/react-reasoning-acting-2210.03629.pdf) / https://arxiv.org/abs/2210.03629 |
| Toolformer | Paper | Uso autônomo de ferramentas por modelos de linguagem. | [local](fontes/papers/toolformer-2302.04761.pdf) / https://arxiv.org/abs/2302.04761 |
| LangGraph | Framework | Orquestração de agentes com estado, memória e human-in-the-loop. | [local](fontes/repositorios-referencia/github-com-langchain-ai-langgraph.pdf) / https://github.com/langchain-ai/langgraph |
| stanfordnlp/dspy | Framework | Programação e otimização de pipelines com LMs. | [local](fontes/repositorios-referencia/github-com-stanfordnlp-dspy.pdf) / https://github.com/stanfordnlp/dspy |

### RAG e conhecimento

| Referência | Tipo | Uso | Link |
| --- | --- | --- | --- |
| Retrieval-Augmented Generation | Paper | Geração fundamentada em recuperação. | [local](fontes/papers/rag-2005.11401.pdf) / https://arxiv.org/abs/2005.11401 |
| Self-RAG | Paper | Recuperação e crítica reflexiva. | [local](fontes/papers/self-rag-2310.11511.pdf) / https://arxiv.org/abs/2310.11511 |
| LlamaIndex | Framework | RAG, agentes documentais, parsing e indexação. | [local](fontes/repositorios-referencia/github-com-run-llama-llama_index.pdf) / https://github.com/run-llama/llama_index |
| Haystack | Framework | Pipelines RAG, agentes e busca semântica. | [local](fontes/repositorios-referencia/github-com-deepset-ai-haystack.pdf) / https://github.com/deepset-ai/haystack |
| Microsoft GraphRAG | Framework | RAG com grafos de conhecimento e comunidades. | [local](fontes/repositorios-referencia/github-com-microsoft-graphrag.pdf) / https://github.com/microsoft/graphrag |
| Knowledge Graphs — Hogan et al. | Survey | Fundamentos e aplicações de knowledge graphs. | [local](fontes/papers/knowledge-graphs-hogan-2003.02320.pdf) / https://arxiv.org/abs/2003.02320 |
| W3C PROV | Padrão | Provenance e rastreabilidade de entidades e atividades. | [local](fontes/conhecimento-raciocinio/w3-org-tr-prov-overview.pdf) / https://www.w3.org/TR/prov-overview/ |
| RDF 1.1 Concepts | Padrão | Modelo de dados para grafos semânticos. | [local](fontes/conhecimento-raciocinio/w3-org-tr-rdf11-concepts.pdf) / https://www.w3.org/TR/rdf11-concepts/ |
| OWL 2 Web Ontology Language | Padrão | Ontologias e modelagem semântica. | [local](fontes/conhecimento-raciocinio/w3-org-tr-owl2-overview.pdf) / https://www.w3.org/TR/owl2-overview/ |
| SHACL | Padrão | Validação de grafos RDF. | [local](fontes/conhecimento-raciocinio/w3-org-tr-shacl.pdf) / https://www.w3.org/TR/shacl/ |

### Vector DBs

| Referência | Tipo | Uso | Link |
| --- | --- | --- | --- |
| Qdrant | Vector DB | Alta performance para RAG em produção. | [local](fontes/repositorios-referencia/github-com-qdrant-qdrant.pdf) / https://github.com/qdrant/qdrant |
| Weaviate | Vector DB | Filtragem híbrida, grafos e multimodalidade. | [local](fontes/repositorios-referencia/github-com-weaviate-weaviate.pdf) / https://github.com/weaviate/weaviate |
| Chroma | Vector DB | Embutível, ideal para prototipagem e testes. | [local](fontes/repositorios-referencia/github-com-chroma-core-chroma.pdf) / https://github.com/chroma-core/chroma |

### Avaliação

| Referência | Tipo | Uso | Link |
| --- | --- | --- | --- |
| RAGAS: Automated Evaluation of RAG | Paper | Métricas automatizadas: fidelidade, relevância e cobertura contextual. | [local](fontes/avaliacao-llm/ragas-2309.15217.pdf) / https://arxiv.org/abs/2309.15217 |
| explodinggradients/ragas | Framework | Avaliação de fidelidade e relevância em pipelines RAG. | [local](fontes/repositorios-referencia/github-com-explodinggradients-ragas.pdf) / https://github.com/explodinggradients/ragas |
| confident-ai/deepeval | Framework | Testes de qualidade, alucinação e regressão para LLMs. | [local](fontes/repositorios-referencia/github-com-confident-ai-deepeval.pdf) / https://github.com/confident-ai/deepeval |
| truera/trulens | Framework | Feedback functions e análise de qualidade de agentes. | [local](fontes/repositorios-referencia/github-com-truera-trulens.pdf) / https://github.com/truera/trulens |
| openai/evals | Framework | Harness extensível para evals de LLMs e sistemas. | [local](fontes/repositorios-referencia/github-com-openai-evals.pdf) / https://github.com/openai/evals |

## Exemplo de aplicação

| Necessidade | Referências |
| --- | --- |
| Agente com ferramentas | ReAct, Toolformer, OWASP LLM Top 10 |
| RAG com fonte rastreável | RAG, Self-RAG, LlamaIndex, W3C PROV |
| Grafo controlado de estados | LangGraph |
| Otimização de prompts | Anthropic PE Guide, OpenAI PE Guide, DSPy |
| Escolha de vector DB | Qdrant (produção), Chroma (prototipagem), Weaviate (grafos) |
| Avaliar pipeline RAG | RAGAS: faithfulness + relevancy + context recall |
| Detectar regressão após mudança | DeepEval com test cases versionados |
| Registrar trecho e fonte usados | W3C PROV |
| Evoluir RAG para GraphRAG | GraphRAG, RDF/OWL |
