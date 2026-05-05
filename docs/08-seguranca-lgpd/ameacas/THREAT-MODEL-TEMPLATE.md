# Template de Threat Model

## Finalidade

Inventário de ameaças e controles mitigatórios para sistemas de IA com LLMs, RAG e agentes. Atualize a cada mudança arquitetural relevante ou nova integração.

## Referências

- OWASP Top 10 for LLM Applications 2025: [local](../../../00-governanca/referencias/fontes/seguranca-governanca-ia/genai-owasp-org-resource-owasp-top-10-for-llm-applications-2025.pdf)
- NIST AI RMF 1.0: [local](../../../00-governanca/referencias/fontes/frameworks/nist-ai-rmf-1.0.pdf)
- Microsoft Responsible AI (Azure WAF): [local](../../../00-governanca/referencias/fontes/arquiteturas-referencia/learn-microsoft-com-en-us-azure-well-architected-ai-responsible-ai.pdf)

---

## 1. Escopo do modelo de ameaças

| Campo | Valor |
| --- | --- |
| **Sistema** | {{PROJECT_NAME}} |
| **Versão** | v0.1 — MVP |
| **Data de revisão** | YYYY-MM-DD |
| **Responsável** | {{equipe de segurança}} |
| **Componentes em escopo** | API de entrada, agentes, pipeline RAG, integrações externas, base de conhecimento |
| **Fora de escopo** | Infraestrutura de nuvem gerenciada (responsabilidade do provedor) |

---

## 2. Diagrama de fluxo de dados (DFD)

> Inserir diagrama ou descrever os fluxos principais:
>
> `Usuário → API → Agente Orquestrador → [LLM / RAG / Ferramentas] → Resposta`
>
> Identifique os trust boundaries: onde dados passam de zona não confiável para confiável e vice-versa.

---

## 3. Inventário de ameaças (STRIDE × LLM)

### LLM01 — Prompt Injection

| Campo | Descrição |
| --- | --- |
| **Descrição** | Entrada do usuário manipula instruções do sistema, bypassa políticas ou extrai dados protegidos. |
| **Superfícies de ataque** | Campo de texto livre, parâmetros de API, conteúdo de documentos indexados no RAG. |
| **Impacto** | Exfiltração de dados, execução de ações não autorizadas, bypass de políticas. |
| **Probabilidade** | Alta — qualquer sistema com input de texto é suscetível. |
| **Controles mitigatórios** | Separar instruções de sistema de entrada do usuário; validar e sanitizar inputs; detectar padrões de injection; logar e alertar tentativas suspeitas. |
| **Referência OWASP** | LLM01:2025 |

### LLM02 — Vazamento de Dados (Insecure Output Handling)

| Campo | Descrição |
| --- | --- |
| **Descrição** | Respostas do modelo expõem dados de treinamento, PII, segredos ou informações de outros usuários. |
| **Superfícies de ataque** | Resposta gerada pelo LLM, logs de debug, contexto do RAG repassado sem filtragem. |
| **Impacto** | Violação de LGPD/GDPR, exposição de segredos, dano reputacional. |
| **Probabilidade** | Média. |
| **Controles mitigatórios** | Mascarar PII antes de indexar na base de conhecimento; validar output antes de retornar ao usuário; não logar payloads completos; aplicar menor privilégio no acesso a fontes. |
| **Referência OWASP** | LLM02:2025, LLM06:2025 |

### LLM06 — Agência Excessiva (Excessive Agency)

| Campo | Descrição |
| --- | --- |
| **Descrição** | Agente executa ações com escopo, permissões ou autonomia além do necessário. |
| **Superfícies de ataque** | Ferramentas com permissões amplas, ausência de confirmação humana, loop de agentes sem circuit breaker. |
| **Impacto** | Modificação/deleção de dados, execução de chamadas externas não autorizadas, side effects irreversíveis. |
| **Probabilidade** | Média-alta em sistemas agenticos. |
| **Controles mitigatórios** | Allowlist de ferramentas e operações por agente; operações de escrita requerem aprovação explícita; circuit breaker para loops; human-in-the-loop em ações de alto impacto. |
| **Referência OWASP** | LLM06:2025 |

### LLM03 — Envenenamento da Base de Conhecimento (Training/RAG Data Poisoning)

| Campo | Descrição |
| --- | --- |
| **Descrição** | Documentos maliciosos injetados na base de conhecimento alteram comportamento do sistema ou exfiltram dados. |
| **Superfícies de ataque** | Pipeline de ingestão de documentos, fontes externas sem validação, atualizações automáticas. |
| **Impacto** | Respostas incorretas, bypass de políticas, prompt injection indireto via documento. |
| **Probabilidade** | Média — depende da abertura do pipeline de ingestão. |
| **Controles mitigatórios** | Validar e sanitizar documentos antes de indexar; controle de acesso à base de conhecimento; auditoria de mudanças; evitar ingestão automática sem revisão. |
| **Referência OWASP** | LLM03:2025 |

### LLM08 — Fraquezas do Modelo (Model Weaknesses)

| Campo | Descrição |
| --- | --- |
| **Descrição** | Alucinações, viés, inconsistências e respostas inadequadas do modelo base. |
| **Superfícies de ataque** | Perguntas fora do domínio, edge cases não cobertos por avaliação, prompts adversariais. |
| **Impacto** | Informação incorreta entregue ao usuário, dano por confiança excessiva na resposta. |
| **Probabilidade** | Alta em qualquer sistema com LLM. |
| **Controles mitigatórios** | Suíte de evals com RAGAS/DeepEval; disclaimer de limitações; human-in-the-loop para decisões de alto impacto; monitorar taxa de alucinação em produção. |
| **Referência OWASP** | LLM08:2025 |

### LLM09 — Dependência Excessiva (Overreliance)

| Campo | Descrição |
| --- | --- |
| **Descrição** | Usuários ou sistemas downstream confiam cegamente nas respostas sem verificação. |
| **Superfícies de ataque** | UX sem indicadores de confiança, ausência de fontes/evidências na resposta. |
| **Impacto** | Decisões erradas baseadas em respostas incorretas. |
| **Probabilidade** | Alta — problema de design e comunicação. |
| **Controles mitigatórios** | Exibir fontes e scores de confiança; mensagens de limitação claras; escalonamento humano para casos de incerteza alta. |
| **Referência OWASP** | LLM09:2025 |

---

## 4. Análise STRIDE por componente

| Componente | Spoofing | Tampering | Repudiation | Info Disclosure | DoS | Elevation of Privilege |
| --- | --- | --- | --- | --- | --- | --- |
| API de entrada | Autenticação JWT/OAuth | Validação de schema | Logs de auditoria | Rate limiting + TLS | Rate limit + timeout | RBAC |
| Agente orquestrador | — | Allowlist de ferramentas | Trace de decisões | Menor privilégio | Circuit breaker | Contratos de agente |
| Pipeline RAG | — | Validação de documentos | Logs de ingestão | Mascaramento de PII | Timeout de retrieval | ACL por fonte |
| LLM externo | — | Prompt system assinado | — | Não enviar PII | Retry com backoff | — |
| Integrações externas | Auth por serviço | Validação de resposta | Log de chamadas | TLS + mascaramento | Timeout + retry | Menor privilégio |

---

## 5. Fluxos de dados sensíveis

| Dado sensível | Origem | Destino | Controle |
| --- | --- | --- | --- |
| PII do usuário | Input de usuário | LLM / logs | Mascarar antes de enviar ao LLM; não logar em claro |
| Credenciais de integração | Secrets manager | Agente/ferramenta | Nunca no código; rotação automática |
| Conteúdo da base de conhecimento | Fontes internas | RAG index | ACL por categoria de documento |
| Contexto de conversa | Sessão do usuário | LLM | TTL curto; não persistir dados sensíveis além da sessão |

---

## 6. Riscos residuais aceitos

| Risco | Justificativa | Revisão |
| --- | --- | --- |
| Alucinação do modelo base | Mitigado por evals e fontes rastreáveis; risco residual aceito para MVP | Trimestral |
| Prompt injection sofisticada | Controles básicos implementados; ataque avançado requer esforço significativo | Semestral |

---

## 7. Histórico de revisões

| Versão | Data | Mudança |
| --- | --- | --- |
| 0.1 | YYYY-MM-DD | Versão inicial — escopo MVP |
