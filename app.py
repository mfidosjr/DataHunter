# 📚 Data Hunter 4.1: Streamlit App com Logo, Sidebar, Download ZIP e Gráficos Coloridos
# ⚙️ Interface Web Avançada - Visual Profissional

# ---
# 📌 Instalação necessária
# pip install streamlit duckduckgo-search pandas openpyxl lxml beautifulsoup4 requests tqdm plotly

# ---
# 📌 Código do aplicativo (salve como app.py)

import streamlit as st
import pandas as pd
import requests
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import os
import zipfile
import shutil
import plotly.express as px

# ---
# 📌 Funções auxiliares

@st.cache_data

def buscar_links(query):
    links = []
    with DDGS() as ddgs:
        results = ddgs.text(f"{query} filetype:csv OR filetype:xlsx OR filetype:json OR filetype:zip", max_results=20)
        page_links = [r.get('href', '') for r in results if r.get('href', '')]
    
    for page_url in page_links:
        try:
            page = requests.get(page_url, timeout=10)
            soup = BeautifulSoup(page.content, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if any(href.lower().endswith(ext) for ext in ['.csv', '.xlsx', '.json', '.zip']):
                    if href.startswith('/'):
                        href = page_url + href
                    links.append(href)
        except:
            pass
    return links


def baixar_arquivos(links, max_files=5, max_size_mb=50):
    arquivos = []
    os.makedirs('datasets', exist_ok=True)
    for url in links:
        if len(arquivos) >= max_files:
            break
        try:
            head = requests.head(url, timeout=10, allow_redirects=True)
            content_type = head.headers.get('Content-Type', '').lower()
            size = int(head.headers.get('Content-Length', 0)) / (1024 * 1024)
            if any(valid in content_type for valid in ['csv', 'excel', 'json', 'zip']) and size <= max_size_mb:
                r = requests.get(url, stream=True, timeout=15)
                filename = url.split("/")[-1].split("?")[0]
                filepath = os.path.join('datasets', filename)
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                if filename.endswith('.zip'):
                    with zipfile.ZipFile(filepath, 'r') as zip_ref:
                        zip_ref.extractall('datasets')
                    for fzip in zip_ref.namelist():
                        if fzip.endswith(('.csv', '.xlsx', '.json')):
                            arquivos.append(os.path.join('datasets', fzip))
                else:
                    arquivos.append(filepath)
        except:
            continue
    return arquivos


def analisar_arquivo(filepath):
    try:
        if filepath.endswith(".csv"):
            df = pd.read_csv(filepath, encoding='utf-8')
        elif filepath.endswith(".xlsx"):
            df = pd.read_excel(filepath)
        elif filepath.endswith(".json"):
            df = pd.read_json(filepath)
        else:
            return None
        if df.shape[0] < 10:
            return None
        percentual_nulos = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
        score = (df.shape[0] * 0.3) + (df.shape[1] * 0.5) - (percentual_nulos * 0.2)
        resumo = {
            'Arquivo': os.path.basename(filepath),
            'Linhas': df.shape[0],
            'Colunas': df.shape[1],
            '% Nulos': percentual_nulos,
            'Pontuação': score,
            'Caminho': filepath
        }
        return resumo
    except:
        return None


def zipar_datasets(datasets_dir='datasets'):
    zip_path = 'datasets_compactados.zip'
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for foldername, subfolders, filenames in os.walk(datasets_dir):
            for filename in filenames:
                if filename.endswith(('.csv', '.xlsx', '.json')):
                    filepath = os.path.join(foldername, filename)
                    zipf.write(filepath, os.path.relpath(filepath, datasets_dir))
    return zip_path

# ---
# 📌 Interface Streamlit

st.set_page_config(page_title="Data Hunter 4.1", layout="wide")

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Magnifying_glass_icon.svg/512px-Magnifying_glass_icon.svg.png", width=80)
    st.title("🔎 Data Hunter 4.1")
    consulta = st.text_input("Digite o tema da busca:")
    buscar = st.button("Buscar Dados")

st.divider()

if buscar and consulta:
    with st.spinner('Buscando e analisando dados, aguarde...'):
        links_encontrados = buscar_links(consulta)
        arquivos_baixados = baixar_arquivos(links_encontrados)
        resultados = []
        for arquivo in arquivos_baixados:
            resumo = analisar_arquivo(arquivo)
            if resumo:
                resultados.append(resumo)

    st.divider()

    if resultados:
        df_resultados = pd.DataFrame(resultados)
        df_resultados = df_resultados.sort_values(by='Pontuação', ascending=False)

        st.success(f"Encontrados {len(resultados)} datasets válidos!")
        st.dataframe(df_resultados[['Arquivo', 'Linhas', 'Colunas', '% Nulos', 'Pontuação']])

        # Gráfico colorido
        fig = px.bar(df_resultados, x='Arquivo', y='Pontuação', color='Pontuação', color_continuous_scale=['red', 'orange', 'green'])
        st.plotly_chart(fig, use_container_width=True)

        # Botão de download zipado
        zip_path = zipar_datasets()
        with open(zip_path, 'rb') as fzip:
            st.download_button("📦 Download de Todos os Datasets", fzip, file_name="datasets_compactados.zip")

        st.subheader("📥 Downloads individuais")
        for idx, row in df_resultados.iterrows():
            with open(row['Caminho'], 'rb') as f:
                st.download_button(f"Download {row['Arquivo']}", f, file_name=row['Arquivo'])

    else:
        st.warning("Nenhum dataset válido foi encontrado.")

# ---
# ✅ Fim do app
