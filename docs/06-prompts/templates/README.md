# Templates de Prompts

Prompts devem ser versionados, testados e associados a agente, política, métrica e critério de aceite.

## Como preencher

Para cada prompt, registre:

- agente;
- objetivo;
- versão;
- entradas esperadas;
- ferramentas permitidas;
- formato de saída;
- política de segurança;
- exemplos positivos e negativos;
- testes associados.

## Exemplo

```text
Agente: Validador
Objetivo: decidir se uma resposta pode ser enviada.
Entrada: resposta candidata, fontes, confiança, política.
Saída: approved | blocked | clarify | handoff.
Regra: bloquear se não houver fonte suficiente.
```
