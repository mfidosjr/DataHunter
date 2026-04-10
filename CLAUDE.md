# CLAUDE.md

This file provides guidance to Claude Code when working with the DataHunter codebase.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

**Environment**: Set `ANTHROPIC_API_KEY` in a `.env` file or as an environment variable to enable AI-powered semantic analysis. Without it, the app falls back to keyword-based analysis.

## Architecture

DataHunter is a Streamlit app that searches, downloads, and analyzes public datasets automatically.

### Request Flow

1. User types a search query → `search.py` uses DuckDuckGo to find relevant pages
2. `validation.py` crawls pages to find valid dataset links (CSV, XLSX, JSON, ZIP) and extracts HTML tables
3. `api_detector.py` detects hidden JSON APIs (XHR endpoints) as a fallback
4. `downloader.py` downloads and decompresses files into a local `datasets/` folder
5. `analyzer.py` analyzes each dataset: row/column count, null %, and a quality score
6. `semantic_analyzer.py` generates a semantic description of what the dataset is about
7. `app.py` displays the ranked results, a bar chart, and a ZIP download of all datasets

### Key Modules

- **`app.py`** — Main Streamlit UI. Orchestrates the full pipeline.
- **`search.py`** — DuckDuckGo search, filters for trusted sources (.gov, .edu, kaggle, etc).
- **`validation.py`** — Link validation and HTML table extraction via BeautifulSoup.
- **`downloader.py`** — Robust file downloader with ZIP decompression support.
- **`analyzer.py`** — Pandas-based dataset stats: rows, columns, null %, quality score.
- **`api_detector.py`** — Selenium-based XHR API detection for pages without direct file links.
- **`semantic_analyzer.py`** — Semantic analysis of column names. Uses Claude API when `ANTHROPIC_API_KEY` is set; falls back to keyword matching otherwise.

### Improvement Areas

- **Semantic analysis** (`semantic_analyzer.py`): the keyword dictionary is limited. Claude can interpret column names in context and produce richer, more accurate descriptions.
- **Dataset ranking** (`analyzer.py`): the scoring is purely structural (rows × columns - nulls). Claude could add a relevance score based on how well the dataset matches the original query.
- **Search quality** (`search.py`): Claude could re-rank or filter search results before crawling.
