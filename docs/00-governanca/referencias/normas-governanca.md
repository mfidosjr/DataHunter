# Normas, Regulação e Governança de IA

> Verifique jurisdição, vigência e aplicabilidade. Leis vigentes impõem obrigações; projetos de lei são sinais de direção regulatória. Normas pagas ficam como link oficial.

| Referência | Tipo | Uso | Link |
| --- | --- | --- | --- |
| ISO/IEC/IEEE 29148:2018 | Norma | Engenharia de requisitos, SRS e rastreabilidade. | https://www.iso.org/standard/72089.html |
| IEEE Std 1362-1998 | Norma histórica | Estrutura conceitual de CONOPS. | https://standards.ieee.org/ |
| ISO/IEC 42001:2023 | Norma | Sistema de gestão de IA, governança e melhoria contínua. | https://www.iso.org/standard/42001 |
| ISO/IEC 27001:2022 | Norma | Segurança da informação, controles e risco. | https://www.iso.org/standard/27001 |
| NIST AI RMF 1.0 | Framework | Gestão de riscos de IA confiável. | [local](fontes/frameworks/nist-ai-rmf-1.0.pdf) / https://www.nist.gov/itl/ai-risk-management-framework |
| NIST AI 600-1 Generative AI Profile | Framework | Riscos específicos de IA generativa. | [local](fontes/frameworks/nist-ai-600-1-generative-ai-profile.pdf) / https://doi.org/10.6028/NIST.AI.600-1 |
| OWASP Top 10 for LLM Applications 2025 | Framework | Prompt injection, data leakage, tool misuse, supply chain e agent risks. | [local](fontes/seguranca-governanca-ia/genai-owasp-org-resource-owasp-top-10-for-llm-applications-2025.pdf) / https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/ |
| Microsoft Responsible AI (Azure WAF) | Guia | Safeguards para agentes, responsible AI e operação. | [local](fontes/arquiteturas-referencia/learn-microsoft-com-en-us-azure-well-architected-ai-responsible-ai.pdf) / https://learn.microsoft.com/en-us/azure/well-architected/ai/responsible-ai |
| EU AI Act — Reg. (UE) 2024/1689 | Lei vigente (UE) | Classificação de risco, transparência, documentação e supervisão humana. | [local](fontes/normas-e-regulacao/eur-lex-europa-eu-eli-reg-2024-1689-oj.pdf) / https://eur-lex.europa.eu/eli/reg/2024/1689/oj |
| LGPD — Lei nº 13.709/2018 | Lei vigente (BR) | Privacidade, dados pessoais, finalidade, minimização e segurança. | [local](fontes/normas-e-regulacao/planalto-gov-br-ccivil_03-_ato2015-2018-2018-lei-l13709.htm.pdf) / https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/L13709.htm |
| PL 2338/2023 | Projeto de lei (BR) | Marco legal de IA no Brasil em evolução. | [local](fontes/normas-e-regulacao/congressonacional-leg-br-en-materias-materias-bicamerais---ver-pl-2338-2023.pdf) / https://www.congressonacional.leg.br/en/materias/materias-bicamerais/-/ver/pl-2338-2023 |

## Exemplo de aplicação

| Decisão / Risco | Referências | Controle |
| --- | --- | --- |
| Criar auditoria e rastreabilidade | ISO 42001, NIST AI RMF, AI Act | Logs estruturados, decisões rastreáveis |
| Bloquear resposta sem fonte confiável | NIST AI 600-1, OWASP LLM Top 10 | Guardrail com fallback explícito |
| Minimizar dados no handoff humano | LGPD, ISO 27001 | Mascaramento, menor privilégio, retenção |
| Prompt injection | OWASP LLM Top 10 | Separar instruções, validar ferramentas |
| Agência excessiva | OWASP, Microsoft Responsible AI | Allowlist, circuit breaker, human-in-the-loop |
