# huggingface_source.py
import os

def buscar_datasets_hf(query, max_results=10):
    """
    Searches Hugging Face Hub for datasets matching the query.
    Works without authentication; HF_TOKEN env var enables private datasets.
    Returns a list of dicts with metadata about each dataset.
    """
    try:
        from huggingface_hub import HfApi

        token = os.environ.get("HF_TOKEN") or None
        api = HfApi(token=token)

        resultados = api.list_datasets(search=query, limit=max_results, full=True)

        datasets = []
        for ds in resultados:
            datasets.append({
                'fonte': 'huggingface',
                'titulo': ds.id,
                'ref': ds.id,
                'url': f"https://huggingface.co/datasets/{ds.id}",
                'downloads': getattr(ds, 'downloads', 0),
                'likes': getattr(ds, 'likes', 0),
                'tags': ds.tags or [],
                'licenca': next((t.replace('license:', '') for t in (ds.tags or []) if t.startswith('license:')), 'desconhecida'),
            })

        return datasets

    except Exception as e:
        print(f"[huggingface_source] Erro: {e}")
        return []


def baixar_dataset_hf(ref, destino='datasets'):
    """
    Downloads a Hugging Face dataset as Parquet files.
    ref = 'owner/dataset-name'
    Returns list of downloaded file paths.
    """
    try:
        from huggingface_hub import snapshot_download

        token = os.environ.get("HF_TOKEN") or None
        os.makedirs(destino, exist_ok=True)

        caminho_local = snapshot_download(
            repo_id=ref,
            repo_type='dataset',
            local_dir=os.path.join(destino, ref.replace('/', '_')),
            token=token,
            ignore_patterns=["*.md", "*.txt", "*.json", ".gitattributes"],
        )

        arquivos = []
        for root, _, files in os.walk(caminho_local):
            for f in files:
                arquivos.append(os.path.join(root, f))

        return arquivos

    except Exception as e:
        print(f"[huggingface_source] Erro ao baixar {ref}: {e}")
        return []
