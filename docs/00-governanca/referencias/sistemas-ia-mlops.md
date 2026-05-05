# Sistemas de IA, MLOps e Observabilidade

> Use para desenhar pipelines, testes, métricas, monitoramento, seleção de modelo e operação contínua.

### MLOps e ciclo de vida

| Referência | Tipo | Uso | Link |
| --- | --- | --- | --- |
| Hidden Technical Debt in Machine Learning Systems | Paper | Riscos estruturais e dívida técnica em sistemas ML. | [local](fontes/sistemas-ia-mlops/papers-nips-cc-paper-5656-hidden-technical-debt-in-machine-learning-syst.pdf) / https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-syst |
| The ML Test Score | Paper | Rubrica de prontidão produtiva para ML. | [local](fontes/sistemas-ia-mlops/research-google-pubs-pub46555.pdf) / https://research.google/pubs/pub46555 |
| Rules of Machine Learning | Guia | Boas práticas de engenharia ML. | [local](fontes/sistemas-ia-mlops/developers-google-com-machine-learning-guides-rules-of-ml.pdf) / https://developers.google.com/machine-learning/guides/rules-of-ml |
| MLOps: Continuous delivery and automation pipelines | Arquitetura | CI/CD/CT, maturidade e automação em ML. | [local](fontes/sistemas-ia-mlops/cloud-google-com-architecture-mlops-continuous-delivery-and-automation-pipelines-in-machine-learning.pdf) / https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning |
| Practitioners Guide to MLOps | Whitepaper | Ciclo de vida, processos e capacidades de MLOps. | [local](fontes/sistemas-ia-mlops/cloud-google-com-resources-mlops-whitepaper.pdf) / https://cloud.google.com/resources/mlops-whitepaper |
| Azure Well-Architected Framework for AI | Arquitetura | Design e operação de workloads de IA. | [local](fontes/arquiteturas-referencia/learn-microsoft-com-en-us-azure-well-architected-ai.pdf) / https://learn.microsoft.com/en-us/azure/well-architected/ai/ |

### Model selection e custo

| Referência | Tipo | Uso | Link |
| --- | --- | --- | --- |
| Anthropic Models Overview | Referência | Capacidade, latência e custo por token dos modelos Claude — base para model selection. | [local](fontes/sistemas-ia-mlops/docs-anthropic-com-en-docs-about-claude-models-overview.pdf) / https://docs.anthropic.com/en/docs/about-claude/models/overview |
| OpenAI Models | Referência | Capacidade, contexto e preço dos modelos OpenAI — referência para tradeoffs de custo. | [local](fontes/sistemas-ia-mlops/platform-openai-com-docs-models.pdf) / https://platform.openai.com/docs/models |
| Anthropic Prompt Caching | Guia | Redução de custo via cache de prompt prefix — fundamental para contexto longo ou base de conhecimento fixa. | [local](fontes/sistemas-ia-mlops/docs-anthropic-com-en-docs-build-with-claude-prompt-caching.pdf) / https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching |

### Observabilidade e tracing

| Referência | Tipo | Uso | Link |
| --- | --- | --- | --- |
| OpenTelemetry Documentation | Padrão/Framework | Tracing, métricas e logs para sistemas distribuídos. | [local](fontes/observabilidade/opentelemetry-io-docs.pdf) / https://opentelemetry.io/docs/ |
| OpenTelemetry GenAI Semantic Conventions | Padrão | Convenções para spans de chamadas LLM, agentes e RAG. | [local](fontes/observabilidade/opentelemetry-io-docs-specs-semconv-gen-ai.pdf) / https://opentelemetry.io/docs/specs/semconv/gen-ai/ |
| open-telemetry/opentelemetry-specification | Repositório | Especificação OTLP, API e SDK. | [local](fontes/repositorios-referencia/github-com-open-telemetry-opentelemetry-specification.pdf) / https://github.com/open-telemetry/opentelemetry-specification |
| prometheus/prometheus | Repositório | Motor de métricas e alertas para produção. | [local](fontes/repositorios-referencia/github-com-prometheus-prometheus.pdf) / https://github.com/prometheus/prometheus |

## Exemplo de aplicação

| Decisão | Referência |
| --- | --- |
| Criar plano de avaliação desde o MVP | ML Test Score, OpenAI Evals |
| Monitorar custo, latência e qualidade | MLOps Google, Azure WAF AI |
| Evitar dependência invisível de dados | Hidden Technical Debt |
| Escolher modelo por custo vs. capacidade | Anthropic Models Overview, OpenAI Models |
| Reduzir custo em contexto longo ou RAG | Anthropic Prompt Caching |
| Rastrear chamadas LLM por agente | OTel GenAI SemConv |
| Alertar em degradação de qualidade | Prometheus Alertmanager |
