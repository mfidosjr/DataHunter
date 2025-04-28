# app.py
import streamlit as st
import os
import pandas as pd
import zipfile

from search import buscar_paginas
from validation import validar_links_de_dados, extrair_tabelas_html
from downloader import baixar_arquivo
from analyzer import analisar_dataset

# --- Configuração da página
st.set_page_config(
    page_title="Data Hunter 5.0 Alpha",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Data Hunter 5.0 Alpha")
st.write("Busca inteligente e análise automática de datasets públicos!")

# --- Entrada do usuário
consulta = st.text_input("Digite o tema da busca (ex: qualidade da água no Brasil):")
buscar = st.button("Buscar e Analisar Dados")

# --- Processamento
if buscar and consulta:
    with st.spinner('🔍 Buscando páginas relevantes...'):
        paginas_encontradas = buscar_paginas(consulta)

    st.success(f"{len(paginas_encontradas)} páginas encontradas.")
    st.divider()

    # 🔵 Nova validação aprimorada
    datasets_encontrados = []
    with st.spinner('🔎 Vasculhando páginas para encontrar datasets...'):
        for pagina in paginas_encontradas:
            links_validos = validar_links_de_dados(pagina)
            datasets_encontrados.extend(links_validos)

    datasets_encontrados = list(set(datasets_encontrados))  # Remove duplicados
    st.success(f"{len(datasets_encontrados)} links de datasets encontrados!")
    st.divider()

    arquivos_baixados = []

    if datasets_encontrados:
        with st.spinner('💾 Baixando datasets encontrados...'):
            for link in datasets_encontrados:
                caminho = baixar_arquivo(link)
                if caminho:
                    arquivos_baixados.append(caminho)
        st.success(f"{len(arquivos_baixados)} arquivos baixados!")
    else:
        st.warning('Nenhum link de download encontrado! Tentando extrair tabelas HTML como fallback...')
        with st.spinner('🗂️ Extraindo tabelas HTML...'):
            for pagina in paginas_encontradas:
                tabelas = extrair_tabelas_html(pagina)
                for idx, tabela in enumerate(tabelas):
                    os.makedirs('datasets', exist_ok=True)
                    caminho = f"datasets/tabela_extraida_{idx}.csv"
                    tabela.to_csv(caminho, index=False)
                    arquivos_baixados.append(caminho)
        st.success(f"{len(arquivos_baixados)} tabelas extraídas e salvas!")

    st.divider()

    # 🔵 Analisar arquivos
    resumos = []
    with st.spinner('📊 Analisando datasets...'):
        for caminho in arquivos_baixados:
            resumo = analisar_dataset(caminho)
            if resumo:
                resumos.append(resumo)

    if resumos:
        df_resultados = pd.DataFrame(resumos).sort_values(by='pontuacao', ascending=False)
        st.success(f"{len(resumos)} datasets analisados com sucesso!")

        st.dataframe(df_resultados[['arquivo', 'linhas', 'colunas', '%_nulos', 'pontuacao']])

        # Gráfico
        import plotly.express as px
        fig = px.bar(df_resultados, x='arquivo', y='pontuacao', color='pontuacao', color_continuous_scale=['red', 'orange', 'green'])
        st.plotly_chart(fig, use_container_width=True)

        # Botão de download zipado
        zip_path = 'datasets_baixados.zip'
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for resumo in resumos:
                zipf.write(resumo['caminho'], arcname=resumo['arquivo'])
        
        with open(zip_path, 'rb') as f:
            st.download_button("📦 Download de Todos os Datasets", f, file_name="datasets_baixados.zip")
    else:
        st.warning("⚠️ Nenhum dataset útil foi encontrado após download ou extração.")

else:
    st.info("Digite um tema e clique no botão para iniciar.")
