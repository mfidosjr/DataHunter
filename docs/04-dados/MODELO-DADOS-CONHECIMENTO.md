# Modelo de Dados e Conhecimento

## Finalidade

Definir fontes, metadados, taxonomia, RAG, memória, chunks, embeddings, índices, eventos, logs, auditoria e lacunas.

## Como usar este documento

Use este documento para explicitar sobre quais dados e evidências o sistema de IA pode raciocinar. Ele deve ser preenchido antes do SSDD detalhado de retrieval, memória, logs e auditoria.

Premissas:

- Existem fontes de conhecimento identificadas.
- Nem toda fonte é automaticamente autorizada.
- Respostas operacionais precisam de evidência rastreável.

## Estrutura

1. Fontes.
2. Metadados.
3. Taxonomia.
4. Memória e contexto.
5. RAG.
6. Chunks.
7. Embeddings.
8. Índices.
9. Eventos.
10. Logs e auditoria.
11. Lacunas.
12. Qualidade e governança.

## 1. Fontes

### Como preencher

Liste fontes, owner, confidencialidade, domínio e status de autorização.

### Exemplo

| Fonte | Tipo | Owner | Confidencialidade | Status |
| --- | --- | --- | --- | --- |
| FAQ pública | Documento | Atendimento | Pública | Autorizada |

## 2. Metadados mínimos

### Como preencher

Defina metadados obrigatórios para retrieval e auditoria.

### Exemplo

| Campo | Descrição | Obrigatório |
| --- | --- | --- |
| `source_id` | Identificador da fonte | Sim |
| `owner` | Responsável pelo conteúdo | Sim |
| `valid_until` | Validade do conteúdo | Quando aplicável |

## 3. Taxonomia

### Como preencher

Defina domínios, categorias, intenções e motivos de handoff.

### Exemplo

| Domínio | Intenções | Handoff |
| --- | --- | --- |
| Atendimento | Status, prazo, dúvida | Reclamação, baixa confiança |

## 4. RAG e evidência

### Como preencher

Descreva chunking, embeddings, índice, filtros, reranking e validação.

### Exemplo

`O retrieval deve filtrar por domínio e confidencialidade antes de ranquear trechos por similaridade.`

## 5. Lacunas de conhecimento

### Como preencher

Defina como perguntas sem resposta viram backlog.

### Exemplo

| Lacuna | Frequência | Domínio | Owner | Ação |
| --- | --- | --- | --- | --- |
| Pergunta sem fonte sobre prazo | 12/semana | Atendimento | Operação | Criar FAQ |
