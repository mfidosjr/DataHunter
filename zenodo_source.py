# zenodo_source.py
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx

ZENODO_API = "https://zenodo.org/api/records"
MAX_TAMANHO_MB = 80          # ignora arquivos maiores que isso
MAX_ARQS_POR_DATASET = 3     # no máximo 3 arquivos por registro


def _headers():
    token = os.environ.get("ZENODO_TOKEN", "").strip()
    return {"Authorization": f"Bearer {token}"} if token else {}


def buscar_datasets_zenodo(query: str, max_results: int = 10) -> list[dict]:
    """
    Searches Zenodo for datasets matching the query.
    No authentication required for public records.
    ZENODO_TOKEN env var enables higher rate limits.
    """
    try:
        resp = httpx.get(
            ZENODO_API,
            params={"q": query, "type": "dataset", "size": max_results, "sort": "mostrecent"},
            headers=_headers(),
            timeout=15,
        )
        resp.raise_for_status()
        hits = resp.json().get("hits", {}).get("hits", [])

        datasets = []
        for h in hits:
            meta = h.get("metadata", {})
            files = h.get("files", [])
            max_bytes = MAX_TAMANHO_MB * 1024 * 1024

            arqs_suportados = [
                {
                    "nome": f.get("key", ""),
                    "url": f.get("links", {}).get("self", ""),
                    "tamanho": f.get("size", 0),
                }
                for f in files
                if any(f.get("key", "").lower().endswith(ext)
                       for ext in [".csv", ".xlsx", ".json", ".zip", ".h5", ".hdf5", ".nc", ".parquet"])
                and f.get("size", 0) <= max_bytes
            ]

            # Ordena pelo menor tamanho e limita a MAX_ARQS_POR_DATASET
            arqs_suportados.sort(key=lambda x: x["tamanho"])
            datasets.append({
                "fonte": "zenodo",
                "titulo": meta.get("title", "—"),
                "ref": str(h.get("id", "")),
                "doi": meta.get("doi", ""),
                "url": h.get("links", {}).get("html", ""),
                "descricao": (meta.get("description") or "")[:300].replace("<p>", "").replace("</p>", ""),
                "licenca": (meta.get("license") or {}).get("id", "desconhecida"),
                "downloads": h.get("stats", {}).get("downloads", 0),
                "arquivos": arqs_suportados[:MAX_ARQS_POR_DATASET],
            })
        return datasets

    except Exception as e:
        print(f"[zenodo_source] Erro na busca: {e}")
        return []


def _baixar_arquivo_zenodo(arq: dict, destino: str) -> str | None:
    """Baixa um único arquivo Zenodo com streaming. Retorna o caminho ou None."""
    url = arq.get("url", "")
    nome = arq.get("nome", "")
    if not url or not nome:
        return None
    caminho = os.path.join(destino, nome)
    try:
        with httpx.stream("GET", url, headers=_headers(), timeout=20,
                          follow_redirects=True) as resp:
            if resp.status_code != 200:
                return None
            with open(caminho, "wb") as f:
                for chunk in resp.iter_bytes(chunk_size=65536):
                    f.write(chunk)
        return caminho
    except Exception as e:
        print(f"[zenodo_source] Erro ao baixar {nome}: {e}")
        return None


def baixar_datasets_zenodo(dataset: dict, destino: str = "datasets") -> list[str]:
    """
    Downloads all supported files from a Zenodo dataset record in parallel.
    Skips files larger than MAX_TAMANHO_MB. Returns list of downloaded file paths.
    """
    os.makedirs(destino, exist_ok=True)
    arqs = dataset.get("arquivos", [])
    if not arqs:
        return []

    baixados = []
    with ThreadPoolExecutor(max_workers=min(len(arqs), MAX_ARQS_POR_DATASET)) as ex:
        futs = {ex.submit(_baixar_arquivo_zenodo, arq, destino): arq for arq in arqs}
        for fut in as_completed(futs):
            resultado = fut.result()
            if resultado:
                baixados.append(resultado)
    return baixados
