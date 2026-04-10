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

# --- Configuração da página
st.set_page_config(
    page_title="Data Hunter 5.2 Alpha",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Data Hunter 5.2 Alpha")
st.write("Busca inteligente e análise automática de datasets públicos!")

# --- Entrada do usuário
consulta = st.text_input("Digite o tema da busca (ex: qualidade da água no Brasil):")
buscar = st.button("Buscar e Analisar Dados")

if buscar and consulta:
    tempo_inicio = time.time()

    with st.spinner('🔍 Buscando páginas relevantes...'):
        paginas_encontradas = buscar_paginas(consulta)

    st.success(f"✅ {len(paginas_encontradas)} páginas encontradas.")
    st.divider()

    datasets_encontrados = []
    with st.spinner('🔎 Vasculhando páginas para encontrar datasets...'):
        for pagina in paginas_encontradas:
            links_validos = validar_links_de_dados(pagina)
            datasets_encontrados.extend(links_validos)

    datasets_encontrados = list(set(datasets_encontrados))
    st.success(f"✅ {len(datasets_encontrados)} links de datasets encontrados.")
    st.divider()

    arquivos_baixados = []

    if datasets_encontrados:
        with st.spinner('💾 Baixando datasets encontrados...'):
            for link in datasets_encontrados:
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

    if not arquivos_baixados:
        st.error("⚠️ Nenhum dataset útil foi encontrado após todos os métodos.")
    else:
        st.success(f"✅ {len(arquivos_baixados)} datasets obtidos!")
        st.divider()

        resumos = []
        with st.spinner('📊 Analisando datasets...'):
            for caminho in arquivos_baixados:
                resumo = analisar_dataset(caminho)
                if resumo:
                    # Análise semântica adicional
                    try:
                        df = pd.read_csv(caminho, encoding='utf-8', low_memory=False)
                        resumo['analise_semantica'] = gerar_resumo_semantico(df.columns)
                    except Exception as e:
                        resumo['analise_semantica'] = "Erro na leitura para análise semântica"
                    resumos.append(resumo)

        if resumos:
            df_resultados = pd.DataFrame(resumos).sort_values(by='pontuacao', ascending=False)
            st.success(f"✅ {len(resumos)} datasets analisados com sucesso!")

            st.dataframe(df_resultados[['arquivo', 'linhas', 'colunas', '%_nulos', 'pontuacao', 'analise_semantica']])

            fig = px.bar(df_resultados, x='arquivo', y='pontuacao', color='pontuacao', color_continuous_scale=['red', 'orange', 'green'])
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
