# app.py
import streamlit as st
import os
import pandas as pd
import zipfile
import plotly.express as px
import time

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from search import buscar_paginas
from validation import validar_links_de_dados, extrair_tabelas_html
from downloader import baixar_arquivo
from analyzer import analisar_dataset
from api_detector import detectar_apis_na_pagina, baixar_dados_da_api
from semantic_analyzer import gerar_resumo_semantico
from kaggle_source import buscar_datasets_kaggle, baixar_dataset_kaggle
from huggingface_source import buscar_datasets_hf, baixar_dataset_hf

# --- Configuração da página
st.set_page_config(
    page_title="Data Hunter",
    page_icon="🔎",
    layout="wide"
)

VERSION = "6.0"
UPDATED = "2026-04-10"

col_title, col_version = st.columns([6, 1])
with col_title:
    st.title("🔎 Data Hunter")
    st.write("Vasculha a internet em busca de bases de dados para projetos de analytics e pesquisa em IA.")
with col_version:
    st.markdown(
        f"""
        <div style='text-align:right; padding-top:18px; color:#888; font-size:0.8rem; line-height:1.6'>
            <strong>v{VERSION}</strong><br>{UPDATED}
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Entrada do usuário
consulta = st.text_input("Digite o tema da busca (ex: qualidade da água no Brasil):")

with st.expander("⚙️ Fontes de dados", expanded=True):
    col1, col2, col3 = st.columns(3)
    usar_web = col1.checkbox("🌐 Web (DuckDuckGo)", value=True)
    usar_kaggle = col2.checkbox("🏆 Kaggle", value=True)
    usar_hf = col3.checkbox("🤗 Hugging Face", value=True)

buscar = st.button("Buscar e Analisar Dados")

if buscar and consulta:
    tempo_inicio = time.time()
    arquivos_baixados = []

    # --- Fonte: Web (DuckDuckGo)
    if usar_web:
        with st.spinner('🌐 Buscando páginas relevantes na web...'):
            paginas_encontradas = buscar_paginas(consulta)
        st.success(f"✅ {len(paginas_encontradas)} páginas encontradas.")
        st.divider()

        links_web = []
        with st.spinner('🔎 Vasculhando páginas para encontrar datasets...'):
            for pagina in paginas_encontradas:
                links_validos = validar_links_de_dados(pagina)
                links_web.extend(links_validos)
        links_web = list(set(links_web))
        st.success(f"✅ {len(links_web)} links de datasets encontrados.")
        st.divider()

        if links_web:
            with st.spinner('💾 Baixando datasets da web...'):
                for link in links_web:
                    caminho = baixar_arquivo(link)
                    if caminho:
                        arquivos_baixados.append(caminho)
        else:
            st.info('ℹ️ Nenhum link direto encontrado. Tentando extrair tabelas HTML...')
            for idx_pag, pagina in enumerate(paginas_encontradas):
                tabelas = extrair_tabelas_html(pagina)
                for idx_tab, tabela in enumerate(tabelas):
                    os.makedirs('datasets', exist_ok=True)
                    caminho = f"datasets/pagina{idx_pag}_tabela{idx_tab}.csv"
                    tabela.to_csv(caminho, index=False)
                    arquivos_baixados.append(caminho)

            if not arquivos_baixados:
                st.info('ℹ️ Tentando detectar APIs JSON como fallback...')
                for pagina in paginas_encontradas:
                    apis = detectar_apis_na_pagina(pagina)
                    for idx, api_url in enumerate(apis):
                        caminho = baixar_dados_da_api(api_url, nome_base=f"api_extraida_{idx}")
                        if caminho:
                            arquivos_baixados.append(caminho)

    # --- Fonte: Kaggle
    if usar_kaggle:
        with st.spinner('🏆 Buscando datasets no Kaggle...'):
            resultados_kaggle = buscar_datasets_kaggle(consulta, max_results=5)
        if resultados_kaggle:
            st.success(f"✅ {len(resultados_kaggle)} datasets encontrados no Kaggle.")
            with st.spinner('💾 Baixando datasets do Kaggle...'):
                for ds in resultados_kaggle:
                    arquivos = baixar_dataset_kaggle(ds['ref'])
                    arquivos_baixados.extend(arquivos)
        else:
            st.info('ℹ️ Nenhum dataset encontrado no Kaggle (verifique KAGGLE_USERNAME e KAGGLE_KEY).')
        st.divider()

    # --- Fonte: Hugging Face
    if usar_hf:
        with st.spinner('🤗 Buscando datasets no Hugging Face...'):
            resultados_hf = buscar_datasets_hf(consulta, max_results=5)
        if resultados_hf:
            st.success(f"✅ {len(resultados_hf)} datasets encontrados no Hugging Face.")
            with st.spinner('💾 Baixando datasets do Hugging Face...'):
                for ds in resultados_hf:
                    arquivos = baixar_dataset_hf(ds['ref'])
                    arquivos_baixados.extend(arquivos)
        else:
            st.info('ℹ️ Nenhum dataset encontrado no Hugging Face.')
        st.divider()

    if not arquivos_baixados:
        st.error("⚠️ Nenhum dataset útil foi encontrado após todos os métodos.")
    else:
        st.success(f"✅ {len(arquivos_baixados)} datasets obtidos!")
        st.divider()

        resumos = []
        with st.spinner('📊 Analisando datasets...'):
            for caminho in arquivos_baixados:
                resumo = analisar_dataset(caminho, query=consulta)
                if resumo:
                    try:
                        from analyzer import ler_dataset
                        df_tmp = ler_dataset(caminho)
                        resumo['descricao'] = gerar_resumo_semantico(df_tmp.columns) if df_tmp is not None else '—'
                    except Exception:
                        resumo['descricao'] = '—'
                    resumos.append(resumo)

        if resumos:
            df_resultados = pd.DataFrame(resumos).sort_values(by='relevancia', ascending=False)
            st.success(f"✅ {len(resumos)} datasets analisados com sucesso!")

            st.dataframe(
                df_resultados[['arquivo', 'linhas', 'colunas', '%_nulos', 'qualidade', 'relevancia', 'descricao']],
                column_config={
                    'qualidade':  st.column_config.ProgressColumn('Qualidade',  min_value=0, max_value=100, format='%.1f'),
                    'relevancia': st.column_config.ProgressColumn('Relevância', min_value=0, max_value=100, format='%.1f'),
                },
                use_container_width=True,
            )

            fig = px.bar(
                df_resultados, x='arquivo', y=['qualidade', 'relevancia'],
                barmode='group',
                color_discrete_map={'qualidade': '#4C9BE8', 'relevancia': '#F4845F'},
                labels={'value': 'Score (0–100)', 'variable': 'Dimensão'},
            )
            st.plotly_chart(fig, use_container_width=True)

            zip_path = 'datasets_baixados.zip'
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for resumo in resumos:
                    zipf.write(resumo['caminho'], arcname=resumo['arquivo'])

            with open(zip_path, 'rb') as f:
                st.download_button("📦 Download de Todos os Datasets", f, file_name="datasets_baixados.zip")
        else:
            st.warning("⚠️ Nenhum dataset útil foi encontrado após análise.")

    tempo_fim = time.time()
    duracao = tempo_fim - tempo_inicio
    st.info(f"⏱️ Tempo total de execução: {duracao:.2f} segundos.")

else:
    st.info("Digite um tema e clique no botão para iniciar.")
