# kaggle_source.py
import os

def buscar_datasets_kaggle(query, max_results=10):
    """
    Searches Kaggle for datasets matching the query.
    Requires KAGGLE_USERNAME and KAGGLE_KEY environment variables.
    Returns a list of dicts with metadata about each dataset.
    """
    try:
        import kaggle
        kaggle.api.authenticate()

        resultados = (kaggle.api.dataset_list(search=query) or [])[:max_results]

        datasets = []
        for ds in resultados:
            datasets.append({
                'fonte': 'kaggle',
                'titulo': ds.title,
                'ref': ds.ref,
                'url': f"https://www.kaggle.com/datasets/{ds.ref}",
                'tamanho_bytes': ds.total_bytes,
                'downloads': ds.download_count,
                'votos': ds.vote_count,
                'licenca': str(ds.license_name),
                'tags': [str(t) for t in ds.tags] if ds.tags else [],
            })

        return datasets

    except Exception as e:
        print(f"[kaggle_source] Erro: {e}")
        return []


def baixar_dataset_kaggle(ref, destino='datasets'):
    """
    Downloads all files of a Kaggle dataset (ref = 'owner/slug').
    Returns list of downloaded file paths.
    """
    try:
        import kaggle
        kaggle.api.authenticate()

        os.makedirs(destino, exist_ok=True)
        kaggle.api.dataset_download_files(ref, path=destino, unzip=True, quiet=False)

        arquivos = []
        for f in os.listdir(destino):
            caminho = os.path.join(destino, f)
            if os.path.isfile(caminho):
                arquivos.append(caminho)

        return arquivos

    except Exception as e:
        print(f"[kaggle_source] Erro ao baixar {ref}: {e}")
        return []
