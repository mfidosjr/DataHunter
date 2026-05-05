# Biblioteca de Referências

Referências reutilizáveis para sistemas de IA: agentes, RAG, governança, segurança, arquitetura e operação. Projetos derivados copiam apenas as referências que efetivamente usam.

## Categorias

| Categoria | Arquivo |
| --- | --- |
| Normas, regulação e governança de IA | [normas-governanca.md](normas-governanca.md) |
| Engenharia de sistemas e requisitos | [engenharia-sistemas.md](engenharia-sistemas.md) |
| Arquitetura de software e referências | [arquitetura-de-referencia.md](arquitetura-de-referencia.md) |
| Sistemas de IA, MLOps e observabilidade | [sistemas-ia-mlops.md](sistemas-ia-mlops.md) |
| LLM, RAG, agentes e avaliação | [llm-rag-agentes.md](llm-rag-agentes.md) |

## Por camada da arquitetura

Detalhamento completo em [arquitetura-de-referencia.md](arquitetura-de-referencia.md).

| Camada | Referências úteis |
| --- | --- |
| Experiência | AWS GenAI CDK Constructs |
| Segurança | NIST SP 800-53 Rev. 5, NIST AI RMF, NIST AI 600-1, OWASP LLM Top 10, EU AI Act, LGPD, Azure Responsible AI, ISO 27001 *(sem arquivo local)* |
| Orquestração | LangGraph, ReAct, Chain-of-Thought, Tree of Thoughts, Self-Consistency, DSPy, Azure Responsible AI |
| Ação | Toolformer, OWASP LLM Top 10, AWS GenAI CDK Constructs |
| Conhecimento | RAG, Self-RAG, GraphRAG, W3C OWL2/RDF/SHACL/PROV, LlamaIndex, Qdrant, Weaviate, Chroma, Google Cloud RAG |
| Modelos | Attention Is All You Need, Self-Consistency, DSPy, Hidden Technical Debt, Anthropic Models, OpenAI Models |
| Dados | Hidden Technical Debt, ML Test Score, Google Cloud MLOps, W3C PROV, LGPD |
| Operação | OpenTelemetry, Prometheus, Google Cloud MLOps, Azure WAF AI, RAGAS, TruLens, DeepEval, OpenAI Evals |

## Todas as referências

### Normas e leis

| Referência | Tipo | Link |
| --- | --- | --- |
| ISO/IEC/IEEE 29148:2018 | Norma | https://www.iso.org/standard/72089.html |
| IEEE Std 1362-1998 | Norma histórica | https://standards.ieee.org/ |
| ISO/IEC 42001:2023 | Norma | https://www.iso.org/standard/42001 |
| ISO/IEC 27001:2022 | Norma | https://www.iso.org/standard/27001 *(sem arquivo local)* |
| EU AI Act — Reg. (UE) 2024/1689 | Lei (UE) | [local](fontes/normas-e-regulacao/eur-lex-europa-eu-eli-reg-2024-1689-oj.pdf) |
| LGPD — Lei nº 13.709/2018 | Lei (BR) | [local](fontes/normas-e-regulacao/planalto-gov-br-ccivil_03-_ato2015-2018-2018-lei-l13709.htm.pdf) |
| PL 2338/2023 | Proj. de lei (BR) | [local](fontes/normas-e-regulacao/congressonacional-leg-br-en-materias-materias-bicamerais---ver-pl-2338-2023.pdf) |

### Frameworks e guias

| Referência | Tipo | Link |
| --- | --- | --- |
| NIST AI RMF 1.0 | Framework | [local](fontes/frameworks/nist-ai-rmf-1.0.pdf) |
| NIST SP 800-53 Rev. 5 — Security and Privacy Controls | Framework | [local](fontes/frameworks/nist-sp-800-53r5.pdf) |
| NIST AI 600-1 Generative AI Profile | Framework | [local](fontes/frameworks/nist-ai-600-1-generative-ai-profile.pdf) |
| OWASP Top 10 for LLM Applications 2025 | Framework | [local](fontes/seguranca-governanca-ia/genai-owasp-org-resource-owasp-top-10-for-llm-applications-2025.pdf) |
| Microsoft Responsible AI (Azure WAF) | Guia | [local](fontes/arquiteturas-referencia/learn-microsoft-com-en-us-azure-well-architected-ai-responsible-ai.pdf) |
| Azure Well-Architected Framework for AI | Guia | [local](fontes/arquiteturas-referencia/learn-microsoft-com-en-us-azure-well-architected-ai.pdf) |
| Google Cloud RAG reference architectures | Guia | [local](fontes/arquiteturas-referencia/cloud-google-com-architecture-rag-reference-architectures.pdf) |
| Google Cloud MLOps architecture | Guia | [local](fontes/sistemas-ia-mlops/cloud-google-com-architecture-mlops-continuous-delivery-and-automation-pipelines-in-machine-learning.pdf) |
| Practitioners Guide to MLOps | Whitepaper | [local](fontes/sistemas-ia-mlops/cloud-google-com-resources-mlops-whitepaper.pdf) |
| Rules of Machine Learning | Guia | [local](fontes/sistemas-ia-mlops/developers-google-com-machine-learning-guides-rules-of-ml.pdf) |
| Anthropic Prompt Engineering Guide | Guia | [local](fontes/llm-rag-agentes/docs-anthropic-com-en-docs-build-with-claude-prompt-engineering-overview.pdf) |
| OpenAI Prompt Engineering Guide | Guia | [local](fontes/llm-rag-agentes/platform-openai-com-docs-guides-prompt-engineering.pdf) |
| Anthropic Models Overview | Referência | [local](fontes/sistemas-ia-mlops/docs-anthropic-com-en-docs-about-claude-models-overview.pdf) |
| OpenAI Models | Referência | [local](fontes/sistemas-ia-mlops/platform-openai-com-docs-models.pdf) |
| Anthropic Prompt Caching | Guia | [local](fontes/sistemas-ia-mlops/docs-anthropic-com-en-docs-build-with-claude-prompt-caching.pdf) |
| NASA Systems Engineering Handbook | Manual | [local](fontes/engenharia-sistemas/nasa-gov-reference-nasa-systems-engineering-handbook.pdf) |
| SEBoK | Base de conhecimento | [local](fontes/engenharia-sistemas/sebokwiki-org-index.pdf) |
| INCOSE SE Handbook | Guia | https://www.incose.org/publications/se-handbook |
| OpenTelemetry Documentation | Padrão/Framework | [local](fontes/observabilidade/opentelemetry-io-docs.pdf) |
| OpenTelemetry GenAI Semantic Conventions | Padrão | [local](fontes/observabilidade/opentelemetry-io-docs-specs-semconv-gen-ai.pdf) |

### Papers e surveys

| Referência | Tipo | Link |
| --- | --- | --- |
| Chain-of-Thought Prompting Elicits Reasoning | Paper | [local](fontes/papers/chain-of-thought-prompting-2201.11903.pdf) |
| Self-Consistency Improves Chain of Thought | Paper | [local](fontes/papers/self-consistency-cot-2203.11171.pdf) |
| Tree of Thoughts | Paper | [local](fontes/papers/tree-of-thoughts-2305.10601.pdf) |
| DSPy | Paper | [local](fontes/papers/dspy-2310.03714.pdf) |
| ReAct: Synergizing Reasoning and Acting | Paper | [local](fontes/papers/react-reasoning-acting-2210.03629.pdf) |
| Toolformer | Paper | [local](fontes/papers/toolformer-2302.04761.pdf) |
| Retrieval-Augmented Generation | Paper | [local](fontes/papers/rag-2005.11401.pdf) |
| Self-RAG | Paper | [local](fontes/papers/self-rag-2310.11511.pdf) |
| RAGAS: Automated Evaluation of RAG | Paper | [local](fontes/avaliacao-llm/ragas-2309.15217.pdf) |
| Knowledge Graphs — Hogan et al. | Survey | [local](fontes/papers/knowledge-graphs-hogan-2003.02320.pdf) |
| Hidden Technical Debt in ML Systems | Paper | [local](fontes/sistemas-ia-mlops/papers-nips-cc-paper-5656-hidden-technical-debt-in-machine-learning-syst.pdf) |
| The ML Test Score — Breck et al. (2017) | Paper | [local](fontes/sistemas-ia-mlops/research-google-pubs-pub46555.pdf) |
| Attention Is All You Need — Vaswani et al. (2017) | Paper | [local](fontes/papers/attention-is-all-you-need-1706.03762.pdf) |

### Padrões W3C

| Referência | Tipo | Link |
| --- | --- | --- |
| W3C PROV | Padrão | [local](fontes/conhecimento-raciocinio/w3-org-tr-prov-overview.pdf) |
| RDF 1.1 Concepts | Padrão | [local](fontes/conhecimento-raciocinio/w3-org-tr-rdf11-concepts.pdf) |
| OWL 2 Web Ontology Language | Padrão | [local](fontes/conhecimento-raciocinio/w3-org-tr-owl2-overview.pdf) |
| SHACL | Padrão | [local](fontes/conhecimento-raciocinio/w3-org-tr-shacl.pdf) |

### Repositórios e ferramentas

| Repositório | Categoria | Link |
| --- | --- | --- |
| langchain-ai/langgraph | Orquestração | [local](fontes/repositorios-referencia/github-com-langchain-ai-langgraph.pdf) |
| stanfordnlp/dspy | Orquestração | [local](fontes/repositorios-referencia/github-com-stanfordnlp-dspy.pdf) |
| run-llama/llama_index | RAG | [local](fontes/repositorios-referencia/github-com-run-llama-llama_index.pdf) |
| deepset-ai/haystack | RAG | [local](fontes/repositorios-referencia/github-com-deepset-ai-haystack.pdf) |
| microsoft/graphrag | RAG | [local](fontes/repositorios-referencia/github-com-microsoft-graphrag.pdf) |
| qdrant/qdrant | Vector DB | [local](fontes/repositorios-referencia/github-com-qdrant-qdrant.pdf) |
| weaviate/weaviate | Vector DB | [local](fontes/repositorios-referencia/github-com-weaviate-weaviate.pdf) |
| chroma-core/chroma | Vector DB | [local](fontes/repositorios-referencia/github-com-chroma-core-chroma.pdf) |
| explodinggradients/ragas | Avaliação | [local](fontes/repositorios-referencia/github-com-explodinggradients-ragas.pdf) |
| confident-ai/deepeval | Avaliação | [local](fontes/repositorios-referencia/github-com-confident-ai-deepeval.pdf) |
| truera/trulens | Avaliação | [local](fontes/repositorios-referencia/github-com-truera-trulens.pdf) |
| openai/evals | Avaliação | [local](fontes/repositorios-referencia/github-com-openai-evals.pdf) |
| open-telemetry/opentelemetry-specification | Observabilidade | [local](fontes/repositorios-referencia/github-com-open-telemetry-opentelemetry-specification.pdf) |
| prometheus/prometheus | Observabilidade | [local](fontes/repositorios-referencia/github-com-prometheus-prometheus.pdf) |
| arc42/arc42-template | Arquitetura | [local](fontes/repositorios-referencia/github-com-arc42-arc42-template.pdf) |
| awslabs/generative-ai-cdk-constructs | IaC | [local](fontes/repositorios-referencia/github-com-awslabs-generative-ai-cdk-constructs.pdf) |
| aws-samples/generative-ai-cdk-constructs-samples | IaC | [local](fontes/repositorios-referencia/github-com-aws-samples-generative-ai-cdk-constructs-samples.pdf) |
| openai/openai-cookbook | Exemplos | [local](fontes/repositorios-referencia/github-com-openai-openai-cookbook.pdf) |

### Livros

| Referência | Tipo | Link |
| --- | --- | --- |
| Software Architecture in Practice, 4th Ed. | Livro | https://www.sei.cmu.edu/library/software-architecture-in-practice-fourth-edition/ |
| Documenting Software Architectures | Livro | https://www.sei.cmu.edu/library/documenting-software-architectures-views-and-beyond-2nd-edition/ |
| Domain-Driven Design | Livro | https://www.domainlanguage.com/ddd/ |

## Regras de uso

- Prefira fontes oficiais; evite blog posts para decisões críticas sem fonte primária.
- Não cite referência que não foi usada no projeto.
- Diferencie referência conceitual de requisito obrigatório — paper não é garantia de prontidão em produção.
- Repositório Git não é padrão normativo; verifique licença, manutenção e segurança antes de reutilizar.
- Registre data de acesso para conteúdo web; revise referências regulatórias periodicamente.

## Tipos

| Tipo | Como tratar |
| --- | --- |
| Norma | Referência formal; verificar acesso e licença. |
| Lei vigente | Obrigação quando aplicável à jurisdição. |
| Projeto de lei | Referência em evolução, não obrigação vigente. |
| Framework | Guia de boas práticas. |
| Paper | Base conceitual/técnica; validar antes de produção. |
| Documentação oficial | Implementação e decisões técnicas atualizadas. |
| Repositório Git | Inspiração; verificar licença, manutenção e segurança. |
