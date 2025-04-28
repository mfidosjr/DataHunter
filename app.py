# app.py
import streamlit as st
import os
import pandas as pd
import zipfile

from search import buscar_paginas
from validation import validar_links_de_dados
from downloader import baixar_arquivo
from analyzer import analisar_dataset

# --- Configuração da página
st.set_page_config(
    page_title="Data Hunter 5.0 Alpha",
    page_icon="🔎",  # Agora com emoji de lupa como favicon!
    layout="wide"
)

st.title("🔎 Data Hunter 5.0 Alpha")
st.write("Busca inteligente e análise automática de datasets públicos!")

consulta = st.text_input("Digite o tema da busca (ex: qualidade da água no Brasil):")
buscar = st.button("Buscar e Analisar Dados")

if buscar and consulta:
    with st.spinner('🔍 Buscando páginas relevantes...'):
        paginas_encontradas = buscar_paginas(consulta)
    st.success(f"{len(paginas_encontradas)} páginas encontradas.")
    st.divider()

    datasets_encontrados = []
    with st.spinner('🔎 Vasculhando páginas para encontrar datasets...'):
        for pagina in paginas_encontradas:
            links_validos = validar_links_de_dados(pagina)
            datasets_encontrados.extend(links_validos)
    st.success(f"{len(datasets_encontrados)} links de datasets encontrados!")
    st.divider()

    arquivos_baixados = []
    with st.spinner('💾 Baixando datasets...'):
        for link in datasets_encontrados:
            caminho = baixar_arquivo(link)
            if caminho:
                arquivos_baixados.append(caminho)
    st.success(f"{len(arquivos_baixados)} arquivos baixados!")
    st.divider()

    resumos = []
    with st.spinner('📊 Analisando qualidade dos dados...'):
        for caminho in arquivos_baixados:
            resumo = analisar_dataset(caminho)
            if resumo:
                resumos.append(resumo)

    if resumos:
        df_resultados = pd.DataFrame(resumos).sort_values(by='pontuacao', ascending=False)
        st.success(f"{len(resumos)} datasets analisados com sucesso!")
        st.dataframe(df_resultados[['arquivo', 'linhas', 'colunas', '%_nulos', 'pontuacao']])
        import plotly.express as px
        fig = px.bar(df_resultados, x='arquivo', y='pontuacao', color='pontuacao', color_continuous_scale=['red', 'orange', 'green'])
        st.plotly_chart(fig, use_container_width=True)

        zip_path = 'datasets_baixados.zip'
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for resumo in resumos:
                zipf.write(resumo['caminho'], arcname=resumo['arquivo'])

        with open(zip_path, 'rb') as f:
            st.download_button("📦 Download de Todos os Datasets", f, file_name="datasets_baixados.zip")
    else:
        st.warning("⚠️ Nenhum dataset útil foi encontrado.")
else:
    st.info("Digite um tema e clique no botão para começar.")
