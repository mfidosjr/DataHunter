# zenodo_source.py
import os
import httpx

ZENODO_API = "https://zenodo.org/api/records"


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
            datasets.append({
                "fonte": "zenodo",
                "titulo": meta.get("title", "—"),
                "ref": str(h.get("id", "")),
                "doi": meta.get("doi", ""),
                "url": h.get("links", {}).get("html", ""),
                "descricao": (meta.get("description") or "")[:300].replace("<p>", "").replace("</p>", ""),
                "licenca": (meta.get("license") or {}).get("id", "desconhecida"),
                "downloads": h.get("stats", {}).get("downloads", 0),
                "arquivos": [
                    {
                        "nome": f.get("key", ""),
                        "url": f.get("links", {}).get("self", ""),
                        "tamanho": f.get("size", 0),
                    }
                    for f in files
                    if any(f.get("key", "").lower().endswith(ext)
                           for ext in [".csv", ".xlsx", ".json", ".zip", ".h5", ".hdf5", ".nc", ".parquet"])
                ],
            })
        return datasets

    except Exception as e:
        print(f"[zenodo_source] Erro: {e}")
        return []


def baixar_datasets_zenodo(dataset: dict, destino: str = "datasets") -> list[str]:
    """
    Downloads all supported files from a Zenodo dataset record.
    Returns list of downloaded file paths.
    """
    os.makedirs(destino, exist_ok=True)
    baixados = []

    for arq in dataset.get("arquivos", []):
        url = arq["url"]
        nome = arq["nome"]
        if not url or not nome:
            continue
        caminho = os.path.join(destino, nome)
        try:
            resp = httpx.get(url, headers=_headers(), timeout=30, follow_redirects=True)
            if resp.status_code == 200:
                with open(caminho, "wb") as f:
                    f.write(resp.content)
                baixados.append(caminho)
        except Exception as e:
            print(f"[zenodo_source] Erro ao baixar {nome}: {e}")

    return baixados
