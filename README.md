<p align="center">
  <img src="logo.png" alt="Data Hunter Logo" width="340"/>
</p>

<h1 align="center">Data Hunter</h1>

<p align="center">
  <strong>Vasculha a internet em busca de bases de dados para projetos de analytics e pesquisa em IA.</strong><br/>
  Busca automática · Download · Análise de qualidade · Ranking por relevância
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white"/>
  <img alt="Kaggle" src="https://img.shields.io/badge/Kaggle-20BEFF?style=flat-square&logo=kaggle&logoColor=white"/>
  <img alt="Hugging Face" src="https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black"/>
  <img alt="Groq" src="https://img.shields.io/badge/Groq%20AI-F55036?style=flat-square&logo=groq&logoColor=white"/>
  <img alt="License" src="https://img.shields.io/badge/license-MIT-22C55E?style=flat-square"/>
  <img alt="CI" src="https://github.com/mfidosjr/DataHunter/actions/workflows/ci.yml/badge.svg"/>
</p>

---

## O que é

Data Hunter é uma aplicação Streamlit que **automatiza o processo de descoberta de datasets públicos**. Em vez de garimpar manualmente dezenas de portais, você descreve o tema que precisa e o app:

1. Busca em múltiplas fontes (Web, Kaggle, Hugging Face)
2. Faz download automático dos arquivos encontrados
3. Analisa cada dataset e gera dois scores: **qualidade técnica** e **relevância** para a sua query
4. Entrega um ranking interativo e um ZIP com todos os dados prontos para uso

Ideal para analistas de dados, cientistas e pesquisadores de IA que precisam de dados rapidamente.

---

## Fontes suportadas

| Fonte | O que busca | Autenticação |
|---|---|---|
| 🌐 **Web (DuckDuckGo)** | Portais .gov, .edu, Kaggle, dados abertos | Não necessária |
| 🏆 **Kaggle** | Datasets públicos com metadata rica (downloads, votos, licença) | `KAGGLE_USERNAME` + `KAGGLE_KEY` |
| 🤗 **Hugging Face** | Datasets da comunidade de ML/IA | Opcional (`HF_TOKEN`) |

---

## Funcionalidades

- **Busca multi-fonte** com priorização de fontes confiáveis
- **Download robusto** com retry automático e backoff exponencial
- **Detecção de APIs JSON ocultas** (XHR) como fallback
- **Extração de tabelas HTML** via BeautifulSoup e Selenium
- **Score de qualidade** — avalia completude, tamanho e densidade de dados
- **Score de relevância** — mede sobreposição semântica com a query
- **Análise semântica com IA** via Groq (fallback por keywords)
- **Ranking interativo** com gráfico comparativo das duas dimensões
- **Download em ZIP** de todos os datasets encontrados

---

## Como rodar

### 1. Clone o repositório

```bash
git clone https://github.com/mfidosjr/DataHunter.git
cd DataHunter
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Groq — análise semântica com IA (grátis em https://console.groq.com)
GROQ_API_KEY="sua_chave_groq"

# Kaggle — obtenha em kaggle.com > Settings > API > Create New Token
KAGGLE_USERNAME="seu_usuario"
KAGGLE_KEY="sua_chave_kaggle"

# Hugging Face — opcional, só para datasets privados
HF_TOKEN="seu_token_hf"
```

> Sem as chaves, o app funciona normalmente: busca via web permanece ativa e a análise semântica cai para o modo por keywords.

### 4. Rode

```bash
streamlit run app.py
```

Acesse em **http://localhost:8501**

---

## Deploy no Streamlit Cloud

1. Faça fork deste repositório
2. No [Streamlit Community Cloud](https://streamlit.io/cloud), crie um novo app apontando para `app.py`
3. Em **Settings > Secrets**, adicione as variáveis do `.env`
4. Deploy!

---

## Arquitetura

```
app.py                  # UI Streamlit — orquestra o pipeline completo
├── search.py           # Busca via DuckDuckGo com variantes de query
├── kaggle_source.py    # Conector Kaggle (busca + download)
├── huggingface_source.py  # Conector Hugging Face (busca + download)
├── validation.py       # Crawling de páginas, extração de links e tabelas HTML
├── downloader.py       # Download com retry automático (tenacity + httpx)
├── api_detector.py     # Detecção de APIs JSON ocultas via Selenium
├── analyzer.py         # Score de qualidade e relevância por dataset
└── semantic_analyzer.py   # Descrição semântica das colunas (Groq ou keywords)
```

---

## Tecnologias

- [Python 3.10+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Kaggle API](https://github.com/Kaggle/kaggle-api)
- [Hugging Face Hub](https://huggingface.co/docs/huggingface_hub)
- [DuckDuckGo Search](https://github.com/deedy5/duckduckgo_search)
- [Groq](https://groq.com/) · [httpx](https://www.python-httpx.org/) · [tenacity](https://tenacity.readthedocs.io/)
- [BeautifulSoup4](https://beautiful-soup-4.readthedocs.io/) · [Selenium](https://selenium-python.readthedocs.io/)
- [Pandas](https://pandas.pydata.org/) · [Plotly](https://plotly.com/python/)

---

<p align="center">
  Feito com 🔎 para quem vive de dados
</p>
