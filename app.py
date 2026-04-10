# app.py
import streamlit as st
import os
import json
import pandas as pd
import zipfile
import plotly.express as px
import time

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from search import buscar_paginas
from validation import validar_links_de_dados, extrair_tabelas_html
from downloader import baixar_arquivo
from analyzer import analisar_dataset, ler_dataset
from api_detector import detectar_apis_na_pagina, baixar_dados_da_api
from semantic_analyzer import gerar_resumo_semantico
from kaggle_source import buscar_datasets_kaggle, baixar_dataset_kaggle
from huggingface_source import buscar_datasets_hf, baixar_dataset_hf

VERSION = "6.1"
UPDATED = "2026-04-10"

SYSTEM_PROMPT = """Você é um assistente especializado em encontrar bases de dados para projetos de analytics e pesquisa em IA.

Seu papel é entender o que o usuário precisa e, após 1 ou 2 trocas de mensagens, extrair palavras-chave de busca.

Quando tiver contexto suficiente, finalize sua resposta com um bloco JSON exatamente neste formato (sem nada depois):
KEYWORDS_JSON: ["keyword1", "keyword2", "keyword3", "keyword4"]

As keywords devem ser em inglês e português, incluindo sinônimos técnicos relevantes.
Seja objetivo e direto. Faça no máximo 2 perguntas de refinamento."""

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def _chat_groq(messages: list) -> str:
    try:
        from groq import Groq
        client = Groq(api_key=os.environ["GROQ_API_KEY"])
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=400,
            messages=messages,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"(Erro ao conectar ao assistente: {e})"


def _extrair_keywords(resposta: str) -> list[str] | None:
    """Extrai o bloco KEYWORDS_JSON da resposta do LLM, se presente."""
    if "KEYWORDS_JSON:" not in resposta:
        return None
    try:
        parte = resposta.split("KEYWORDS_JSON:")[-1].strip()
        return json.loads(parte)
    except Exception:
        return None


def _card_dataset(resumo: dict, idx: int):
    """Renderiza um card de resultado para um dataset."""
    fonte_icon = {"kaggle": "🏆", "huggingface": "🤗", "web": "🌐", "zenodo": "🔬"}.get(
        resumo.get("fonte", "web"), "📄"
    )
    q = resumo.get("qualidade", 0)
    r = resumo.get("relevancia", 0)
    estrelas_q = "★" * int(q / 20) + "☆" * (5 - int(q / 20))
    estrelas_r = "★" * int(r / 20) + "☆" * (5 - int(r / 20))

    with st.container(border=True):
        st.markdown(f"**{fonte_icon} {resumo['arquivo']}**")
        st.caption(resumo.get("descricao", "—"))
        c1, c2 = st.columns(2)
        c1.metric("Linhas", f"{resumo['linhas']:,}")
        c2.metric("Colunas", resumo["colunas"])
        st.markdown(
            f"Qualidade `{estrelas_q}` &nbsp;&nbsp; Relevância `{estrelas_r}`",
            unsafe_allow_html=True,
        )
        with open(resumo["caminho"], "rb") as f:
            st.download_button(
                "⬇️ Baixar",
                f,
                file_name=resumo["arquivo"],
                key=f"dl_{idx}",
                use_container_width=True,
            )


def _executar_busca(keywords: list, fontes: dict, formatos: list) -> list:
    """Executa o pipeline completo e retorna lista de resumos analisados."""
    query = " ".join(keywords)
    arquivos = []
    resultados_container = st.empty()

    # --- Web
    if fontes.get("web"):
        with st.status("🌐 Buscando na web...", expanded=False) as s:
            paginas = buscar_paginas(query)
            links = []
            for p in paginas:
                links.extend(validar_links_de_dados(p))
            links = list(set(links))
            s.update(label=f"🌐 Web — {len(links)} links encontrados", state="complete")
            for link in links:
                ext = link.split("?")[0].split(".")[-1].lower()
                if ext in formatos:
                    c = baixar_arquivo(link)
                    if c:
                        arquivos.append(c)
            if not links:
                for i, p in enumerate(paginas):
                    for j, t in enumerate(extrair_tabelas_html(p)):
                        os.makedirs("datasets", exist_ok=True)
                        c = f"datasets/pagina{i}_tabela{j}.csv"
                        t.to_csv(c, index=False)
                        arquivos.append(c)

    # --- Kaggle
    if fontes.get("kaggle"):
        with st.status("🏆 Buscando no Kaggle...", expanded=False) as s:
            dss = buscar_datasets_kaggle(query, max_results=5)
            s.update(label=f"🏆 Kaggle — {len(dss)} datasets encontrados", state="complete")
            for ds in dss:
                for f in baixar_dataset_kaggle(ds["ref"]):
                    arquivos.append(f)

    # --- Hugging Face
    if fontes.get("hf"):
        with st.status("🤗 Buscando no Hugging Face...", expanded=False) as s:
            dss = buscar_datasets_hf(query, max_results=5)
            s.update(label=f"🤗 Hugging Face — {len(dss)} datasets encontrados", state="complete")
            for ds in dss:
                for f in baixar_dataset_hf(ds["ref"]):
                    arquivos.append(f)

    if not arquivos:
        return []

    # --- Análise
    resumos = []
    with st.status(f"📊 Analisando {len(arquivos)} arquivos...", expanded=False) as s:
        for caminho in arquivos:
            resumo = analisar_dataset(caminho, query=query)
            if resumo:
                try:
                    df_tmp = ler_dataset(caminho)
                    resumo["descricao"] = gerar_resumo_semantico(df_tmp.columns) if df_tmp is not None else "—"
                    resumo["fonte"] = "kaggle" if "kaggle" in caminho.lower() else \
                                      "huggingface" if "hugging" in caminho.lower() else "web"
                except Exception:
                    resumo["descricao"] = "—"
                    resumo["fonte"] = "web"
                resumos.append(resumo)
        s.update(label=f"📊 {len(resumos)} datasets analisados", state="complete")

    return sorted(resumos, key=lambda x: x["relevancia"], reverse=True)


# -------------------------------------------------------------------
# Session state
# -------------------------------------------------------------------
for key, default in {
    "chat_messages": [],
    "keywords": [],
    "keywords_prontas": False,
    "resultados": [],
    "buscou": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# -------------------------------------------------------------------
# Layout
# -------------------------------------------------------------------
st.set_page_config(page_title="Data Hunter", page_icon="🔎", layout="wide")

col_title, col_ver = st.columns([6, 1])
with col_title:
    st.title("🔎 Data Hunter")
    st.caption("Vasculha a internet em busca de bases de dados para analytics e pesquisa em IA.")
with col_ver:
    st.markdown(
        f"<div style='text-align:right;padding-top:20px;color:#888;font-size:.8rem'>"
        f"<strong>v{VERSION}</strong><br>{UPDATED}</div>",
        unsafe_allow_html=True,
    )

st.divider()

# -------------------------------------------------------------------
# Seção 1 — Chat de intenção
# -------------------------------------------------------------------
st.subheader("💬 O que você precisa?")

for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        # Exibe só o texto, sem o bloco KEYWORDS_JSON
        texto = msg["content"].split("KEYWORDS_JSON:")[0].strip()
        st.markdown(texto)

if prompt := st.chat_input("Descreva os dados que você precisa..."):
    st.session_state.chat_messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    groq_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.chat_messages

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resposta = _chat_groq(groq_messages)

        texto_visivel = resposta.split("KEYWORDS_JSON:")[0].strip()
        st.markdown(texto_visivel)

    st.session_state.chat_messages.append({"role": "assistant", "content": resposta})

    keywords = _extrair_keywords(resposta)
    if keywords:
        st.session_state.keywords = keywords
        st.session_state.keywords_prontas = True

    st.rerun()

# -------------------------------------------------------------------
# Seção 2 — Configuração da busca (aparece após keywords extraídas)
# -------------------------------------------------------------------
if st.session_state.keywords_prontas:
    st.divider()
    st.subheader("⚙️ Configurar busca")

    # Keywords editáveis
    st.markdown("**Palavras-chave** — edite, adicione ou remova:")
    keywords_editadas = st.pills(
        label="keywords",
        options=st.session_state.keywords,
        selection_mode="multi",
        default=st.session_state.keywords,
        label_visibility="collapsed",
    )

    col_add, col_spacer = st.columns([2, 5])
    nova_kw = col_add.text_input("Adicionar keyword", placeholder="ex: radar spectrum", label_visibility="collapsed")
    if col_add.button("＋ Adicionar", use_container_width=True) and nova_kw.strip():
        if nova_kw.strip() not in st.session_state.keywords:
            st.session_state.keywords.append(nova_kw.strip())
        st.rerun()

    st.markdown("**Fontes de dados:**")
    fc1, fc2, fc3 = st.columns(3)
    usar_web     = fc1.checkbox("🌐 Web (DuckDuckGo)", value=True)
    usar_kaggle  = fc2.checkbox("🏆 Kaggle", value=True)
    usar_hf      = fc3.checkbox("🤗 Hugging Face", value=True)

    st.markdown("**Formatos aceitos:**")
    formatos = st.pills(
        "formatos",
        options=["csv", "xlsx", "json", "zip", "parquet"],
        selection_mode="multi",
        default=["csv", "xlsx", "json", "zip"],
        label_visibility="collapsed",
    )

    st.markdown("")
    if st.button("🔍 Buscar e Analisar", type="primary", use_container_width=True):
        fontes = {"web": usar_web, "kaggle": usar_kaggle, "hf": usar_hf}
        kws_ativas = list(keywords_editadas) if keywords_editadas else st.session_state.keywords
        with st.spinner(""):
            st.session_state.resultados = _executar_busca(kws_ativas, fontes, list(formatos))
        st.session_state.buscou = True
        st.rerun()

# -------------------------------------------------------------------
# Seção 3 — Resultados em cards
# -------------------------------------------------------------------
if st.session_state.buscou:
    st.divider()
    st.subheader("📦 Resultados")

    resumos = st.session_state.resultados

    if not resumos:
        st.warning("Nenhum dataset encontrado. Tente ajustar as keywords ou fontes.")
    else:
        st.caption(f"{len(resumos)} datasets encontrados · ordenados por relevância")

        # Gráfico comparativo
        df_res = pd.DataFrame(resumos)
        fig = px.bar(
            df_res, x="arquivo", y=["qualidade", "relevancia"],
            barmode="group",
            color_discrete_map={"qualidade": "#4C9BE8", "relevancia": "#F4845F"},
            labels={"value": "Score (0–100)", "variable": "Dimensão"},
            height=280,
        )
        fig.update_layout(margin=dict(t=20, b=20), legend=dict(orientation="h"))
        st.plotly_chart(fig, use_container_width=True)

        # Cards em grid de 3 colunas
        cols = st.columns(3)
        for i, resumo in enumerate(resumos):
            with cols[i % 3]:
                _card_dataset(resumo, i)

        # Download ZIP de todos
        st.divider()
        zip_path = "datasets_baixados.zip"
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for r in resumos:
                zipf.write(r["caminho"], arcname=r["arquivo"])
        with open(zip_path, "rb") as f:
            st.download_button(
                "📦 Baixar todos os datasets (ZIP)",
                f,
                file_name="datasets_baixados.zip",
                use_container_width=True,
            )

        # Botão para nova busca
        if st.button("🔄 Nova busca", use_container_width=True):
            for key in ["chat_messages", "keywords", "keywords_prontas", "resultados", "buscou"]:
                st.session_state[key] = [] if isinstance(st.session_state[key], list) else False
            st.rerun()
