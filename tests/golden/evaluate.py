#!/usr/bin/env python3
"""
Golden dataset evaluator for DataHunter.

Measures:
  - Query expansion quality  : are domain-specific terms present in the generated variants?
  - Source recall@K          : did expected sources appear in the top-K search results?
  - Link recall              : were known dataset URLs (or their domains) found?

Usage:
    python tests/golden/evaluate.py                        # all queries
    python tests/golden/evaluate.py --id eme_01            # single query
    python tests/golden/evaluate.py --k 20 --no-download   # adjust K, skip downloads
"""
import sys
import os
import json
import argparse
from urllib.parse import urlparse

# Make project root importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from query_expander import expandir_query
from search import buscar_paginas


GOLDEN_FILE = os.path.join(os.path.dirname(__file__), "queries.json")


# ── helpers ──────────────────────────────────────────────────────────────────

def _domain(url: str) -> str:
    try:
        return urlparse(url).netloc.lstrip("www.")
    except Exception:
        return url


def _urls_to_domains(urls: list[str]) -> set[str]:
    return {_domain(u) for u in urls if u}


def _color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

OK   = lambda t: _color(t, "32")   # green
WARN = lambda t: _color(t, "33")   # yellow
FAIL = lambda t: _color(t, "31")   # red
BOLD = lambda t: _color(t, "1")


# ── per-query evaluation ──────────────────────────────────────────────────────

def avaliar_expansao(query: dict, variantes: list[str]) -> dict:
    """Checks whether domain-specific keywords appear in the generated variants."""
    esperadas = [kw.lower() for kw in query.get("keywords_esperadas_na_expansao", [])]
    if not esperadas:
        return {"score": None, "achadas": [], "faltando": []}

    variantes_lower = " ".join(variantes).lower()
    achadas  = [kw for kw in esperadas if kw in variantes_lower]
    faltando = [kw for kw in esperadas if kw not in variantes_lower]
    score = round(len(achadas) / len(esperadas) * 100) if esperadas else 100
    return {"score": score, "achadas": achadas, "faltando": faltando}


def avaliar_recall_fontes(query: dict, urls_encontradas: list[str], k: int) -> dict:
    """Measures what fraction of expected sources appeared in the top-K URLs."""
    fontes_esperadas = query.get("fontes_esperadas", [])
    if not fontes_esperadas:
        return {"recall": None, "achadas": [], "faltando": []}

    dominios_encontrados = _urls_to_domains(urls_encontradas[:k])
    achadas  = [f for f in fontes_esperadas if any(f in d for d in dominios_encontrados)]
    faltando = [f for f in fontes_esperadas if f not in achadas]
    recall = round(len(achadas) / len(fontes_esperadas) * 100) if fontes_esperadas else 100
    return {"recall": recall, "achadas": achadas, "faltando": faltando}


def avaliar_datasets_conhecidos(query: dict, urls_encontradas: list[str]) -> dict:
    """Checks whether known dataset URLs (or their domains) were found."""
    conhecidos = query.get("datasets_conhecidos", [])
    if not conhecidos:
        return {"found": [], "missed": []}

    dominios_encontrados = _urls_to_domains(urls_encontradas)
    found, missed = [], []
    for ds in conhecidos:
        dom = _domain(ds["url"])
        if any(dom in d or d in dom for d in dominios_encontrados):
            found.append(ds["titulo"])
        else:
            missed.append(ds["titulo"])
    return {"found": found, "missed": missed}


# ── main evaluation loop ──────────────────────────────────────────────────────

def avaliar_query(query: dict, k: int = 15) -> dict:
    print(f"\n{'─'*60}")
    print(BOLD(f"[{query['id']}] {query['intent']}"))
    print(f"Keywords: {query['keywords']}")

    # 1. Expand query
    variantes = expandir_query(query["keywords"], query.get("intent", ""))
    print(f"\n{BOLD('Variantes geradas')} ({len(variantes)}):")
    for v in variantes:
        print(f"  • {v}")

    exp = avaliar_expansao(query, variantes)
    if exp["score"] is not None:
        cor = OK if exp["score"] >= 60 else (WARN if exp["score"] >= 30 else FAIL)
        print(f"  Cobertura vocabulário: {cor(str(exp['score']) + '%')} "
              f"({len(exp['achadas'])}/{len(exp['achadas'])+len(exp['faltando'])})")
        if exp["faltando"]:
            print(f"  {WARN('Faltando')}: {', '.join(exp['faltando'])}")

    # 2. Search (first 2 variants to stay fast)
    print(f"\n{BOLD('Busca web')} (top-{k} por variante):")
    urls_diretas, urls_paginas = [], []
    for v in variantes[:2]:
        d, p = buscar_paginas(v, max_results=k)
        urls_diretas.extend(d)
        urls_paginas.extend(p)
        print(f"  • '{v}' → {len(d)} diretos + {len(p)} páginas")

    todas_urls = list(dict.fromkeys(urls_diretas + urls_paginas))

    # 3. Source recall
    rec = avaliar_recall_fontes(query, todas_urls, k=len(todas_urls))
    if rec["recall"] is not None:
        cor = OK if rec["recall"] >= 60 else (WARN if rec["recall"] >= 30 else FAIL)
        print(f"\n{BOLD('Recall de fontes')}: {cor(str(rec['recall']) + '%')}")
        if rec["achadas"]:
            print(f"  {OK('Encontradas')}: {', '.join(rec['achadas'])}")
        if rec["faltando"]:
            print(f"  {FAIL('Não encontradas')}: {', '.join(rec['faltando'])}")

    # 4. Known datasets
    ds_check = avaliar_datasets_conhecidos(query, todas_urls)
    if ds_check["found"] or ds_check["missed"]:
        print(f"\n{BOLD('Datasets conhecidos')}:")
        for t in ds_check["found"]:
            print(f"  {OK('✓')} {t}")
        for t in ds_check["missed"]:
            print(f"  {FAIL('✗')} {t}")

    return {
        "id": query["id"],
        "expansao_score": exp.get("score"),
        "recall_fontes": rec.get("recall"),
        "datasets_found": len(ds_check["found"]),
        "datasets_total": len(ds_check["found"]) + len(ds_check["missed"]),
        "urls_total": len(todas_urls),
    }


def resumo_final(resultados: list[dict]):
    print(f"\n{'═'*60}")
    print(BOLD("RESUMO GERAL"))
    print(f"{'═'*60}")

    exp_scores  = [r["expansao_score"] for r in resultados if r["expansao_score"] is not None]
    rec_scores  = [r["recall_fontes"]  for r in resultados if r["recall_fontes"]  is not None]
    ds_found    = sum(r["datasets_found"] for r in resultados)
    ds_total    = sum(r["datasets_total"] for r in resultados)

    def media(lst):
        return round(sum(lst) / len(lst)) if lst else "—"

    print(f"  Expansão de vocabulário (média): {media(exp_scores)}%")
    print(f"  Recall de fontes        (média): {media(rec_scores)}%")
    print(f"  Datasets conhecidos encontrados: {ds_found}/{ds_total}")

    if rec_scores and (sum(rec_scores) / len(rec_scores)) < 40:
        print(f"\n{WARN('⚠ Recall baixo — considere:')}")
        print("  • Adicionar as fontes faltantes em FONTES_PREFERIDAS (search.py)")
        print("  • Melhorar o DOMAIN_HINTS em query_expander.py")
        print("  • Adicionar connectors diretos (ex: FCC API, ANATEL API)")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Avalia o DataHunter contra o golden dataset.")
    parser.add_argument("--id",          help="Rodar apenas a query com este id")
    parser.add_argument("--k",  type=int, default=15, help="Top-K para cálculo de recall (default: 15)")
    args = parser.parse_args()

    with open(GOLDEN_FILE) as f:
        queries = json.load(f)

    if args.id:
        queries = [q for q in queries if q["id"] == args.id]
        if not queries:
            print(FAIL(f"Query '{args.id}' não encontrada."))
            sys.exit(1)

    resultados = []
    for q in queries:
        try:
            resultado = avaliar_query(q, k=args.k)
            resultados.append(resultado)
        except Exception as e:
            print(FAIL(f"Erro em [{q['id']}]: {e}"))

    if len(resultados) > 1:
        resumo_final(resultados)


if __name__ == "__main__":
    main()
