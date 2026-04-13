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

from concurrent.futures import ThreadPoolExecutor, as_completed

from search import buscar_paginas
from validation import validar_links_em_paralelo, extrair_tabelas_html
from downloader import baixar_arquivo
from analyzer import analisar_dataset
from api_detector import detectar_apis_na_pagina, baixar_dados_da_api
from kaggle_source import buscar_datasets_kaggle, baixar_dataset_kaggle
from huggingface_source import buscar_datasets_hf, baixar_dataset_hf
from zenodo_source import buscar_datasets_zenodo, baixar_datasets_zenodo
from query_expander import expandir_query
from history import save_search, list_searches, get_search, delete_search, clear_history

VERSION = "6.9"
UPDATED = "2026-04-10"

SYSTEM_PROMPT = """Você é um assistente especializado em encontrar bases de dados para projetos de analytics e pesquisa em IA.

Seu papel é entender o que o usuário precisa através de uma conversa. Siga estas regras obrigatórias:

1. Na PRIMEIRA mensagem do usuário: NUNCA extraia keywords. Faça EXATAMENTE 1 pergunta de refinamento para entender melhor o contexto (ex: finalidade, período, geografia, formato esperado).

2. Na SEGUNDA mensagem em diante: se já tiver contexto suficiente, finalize sua resposta com o bloco abaixo. Caso ainda precise de mais detalhes, faça mais 1 pergunta.

Quando estiver pronto para buscar, finalize com exatamente este formato:
KEYWORDS_JSON: ["keyword1 em inglês", "keyword2 em inglês", "termo em português", "sinônimo técnico"]

As keywords devem cobrir sinônimos técnicos em inglês e português.
Seja direto e objetivo nas perguntas."""

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


def _gerar_titulo(primeira_mensagem: str) -> str:
    """Gera um título curto (3-5 palavras) para a sessão de busca."""
    try:
        from groq import Groq
        client = Groq(api_key=os.environ["GROQ_API_KEY"])
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=20,
            messages=[{
                "role": "user",
                "content": f"Crie um título curto (3 a 5 palavras, sem aspas) para uma busca de dados sobre: {primeira_mensagem}"
            }],
        )
        return response.choices[0].message.content.strip().strip('"').strip("'")
    except Exception:
        return ""


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


def _render_metricas(m: dict, placeholders: dict):
    """Atualiza os 4 contadores de progresso ao vivo."""
    placeholders["variantes"].metric("🧠 Variantes", m["variantes"])
    placeholders["paginas"].metric("🌐 Páginas", m["paginas"])
    placeholders["arquivos"].metric("💾 Arquivos", m["arquivos"])
    placeholders["datasets"].metric("📦 Datasets", m["datasets"])


def _executar_busca(keywords: list, fontes: dict, formatos: list,
                   intencao: str = "", placeholders: dict = None) -> list:
    """Executa o pipeline completo, atualizando métricas e detalhes ao vivo."""

    metricas = {"variantes": 0, "paginas": 0, "arquivos": 0, "datasets": 0}

    def _atualizar(campo, valor):
        metricas[campo] = valor
        if placeholders:
            _render_metricas(metricas, placeholders)

    # --- Expansão de query
    with st.status("🧠 Expansão de query com IA", expanded=True) as s:
        variantes = expandir_query(keywords, intencao)
        _atualizar("variantes", len(variantes))
        for v in variantes:
            st.caption(f"• {v}")
        s.update(label=f"🧠 {len(variantes)} variantes geradas", state="complete", expanded=False)

    query_principal = variantes[0]
    arquivos = []
    meta_map: dict[str, dict] = {}

    # --- Web
    if fontes.get("web"):
        with st.status("🌐 Web (DuckDuckGo)", expanded=True) as s:
            diretos_todos: list[str] = []
            paginas_todas: list[str] = []
            for i, v in enumerate(variantes[:3], 1):
                st.caption(f"• Variante {i}/3: `{v}`")
                d, p = buscar_paginas(v, max_results=12)
                diretos_todos.extend(d)
                paginas_todas.extend(p)

            diretos_todos = list(dict.fromkeys(diretos_todos))
            paginas_todas = list(dict.fromkeys(paginas_todas))
            _atualizar("paginas", len(paginas_todas))
            st.caption(f"• {len(diretos_todos)} links diretos · {len(paginas_todas)} páginas para vasculhar")

            # Crawl paralelo — retorna (url, titulo_pagina, descricao_pagina)
            st.caption(f"• Vasculhando {len(paginas_todas)} páginas em paralelo…")
            links_crawl = validar_links_em_paralelo(paginas_todas, max_workers=10)
            # links diretos não têm contexto de página
            links_diretos_meta = [(u, "", "") for u in diretos_todos]
            links_com_meta = list({item[0]: item for item in links_diretos_meta + links_crawl}.values())
            st.caption(f"• {len(links_com_meta)} links de datasets encontrados no total")

            candidatos = [
                (url, titulo, desc) for url, titulo, desc in links_com_meta
                if url.split("?")[0].rsplit(".", 1)[-1].lower() in formatos
            ]
            st.caption(f"• Baixando {len(candidatos)} arquivos em paralelo…")

            novos = 0
            with ThreadPoolExecutor(max_workers=6) as ex:
                futs = {ex.submit(baixar_arquivo, url): (url, titulo, desc)
                        for url, titulo, desc in candidatos}
                for fut in as_completed(futs):
                    url, titulo, desc = futs[fut]
                    c = fut.result()
                    if c:
                        arquivos.append(c)
                        meta_map[c] = {"fonte": "web", "titulo": titulo, "descricao": desc}
                        novos += 1
                        _atualizar("arquivos", len(arquivos))

            if not links_com_meta:
                for i, p in enumerate(paginas_todas[:5]):
                    for j, t in enumerate(extrair_tabelas_html(p)):
                        os.makedirs("datasets", exist_ok=True)
                        c = f"datasets/pagina{i}_tabela{j}.csv"
                        t.to_csv(c, index=False)
                        arquivos.append(c)
                        meta_map[c] = {"fonte": "web", "titulo": "", "descricao": ""}
                        novos += 1
                        _atualizar("arquivos", len(arquivos))

            s.update(label=f"🌐 Web — {len(paginas_todas)} páginas · {novos} arquivos baixados",
                     state="complete", expanded=False)

    # --- Kaggle
    if fontes.get("kaggle"):
        with st.status("🏆 Kaggle", expanded=True) as s:
            dss = []
            for v in variantes[:3]:
                st.caption(f"• Query: `{v}`")
                novos_dss = buscar_datasets_kaggle(v, max_results=5)
                refs_existentes = {d["ref"] for d in dss}
                dss += [d for d in novos_dss if d["ref"] not in refs_existentes]
            st.caption(f"• {len(dss)} datasets encontrados")
            novos = 0
            for ds in dss:
                st.caption(f"  ↳ {ds.get('titulo', ds['ref'])[:60]} ({ds.get('downloads', 0):,} downloads)")
                for f in baixar_dataset_kaggle(ds["ref"]):
                    arquivos.append(f)
                    meta_map[f] = {"fonte": "kaggle", "titulo": ds.get("titulo", ""), "descricao": ""}
                    novos += 1
                    _atualizar("arquivos", len(arquivos))
            s.update(label=f"🏆 Kaggle — {len(dss)} datasets · {novos} arquivos baixados",
                     state="complete", expanded=False)

    # --- Hugging Face
    if fontes.get("hf"):
        with st.status("🤗 Hugging Face", expanded=True) as s:
            st.caption(f"• Query: `{query_principal}`")
            dss = buscar_datasets_hf(query_principal, max_results=5)
            st.caption(f"• {len(dss)} datasets encontrados")
            novos = 0
            for ds in dss:
                st.caption(f"  ↳ {ds['titulo'][:60]} ({ds.get('downloads', 0):,} downloads)")
                for f in baixar_dataset_hf(ds["ref"]):
                    arquivos.append(f)
                    meta_map[f] = {"fonte": "huggingface", "titulo": ds.get("titulo", ""), "descricao": ""}
                    novos += 1
                    _atualizar("arquivos", len(arquivos))
            s.update(label=f"🤗 Hugging Face — {len(dss)} datasets · {novos} arquivos baixados",
                     state="complete", expanded=False)

    # --- Zenodo
    if fontes.get("zenodo"):
        with st.status("🔬 Zenodo", expanded=True) as s:
            dss = []
            refs_zen: set[str] = set()
            for v in variantes[:4]:
                st.caption(f"• Query: `{v}`")
                novos_dss = buscar_datasets_zenodo(v, max_results=6)
                for d in novos_dss:
                    if d["ref"] not in refs_zen:
                        refs_zen.add(d["ref"])
                        dss.append(d)
            st.caption(f"• {len(dss)} datasets encontrados — baixando em paralelo…")

            novos = 0
            with ThreadPoolExecutor(max_workers=4) as ex:
                futs = {ex.submit(baixar_datasets_zenodo, ds): ds for ds in dss}
                for fut in as_completed(futs):
                    ds = futs[fut]
                    arqs_ds = fut.result()
                    tipos = ", ".join(set(f.split(".")[-1] for f in arqs_ds)) if arqs_ds else "nenhum"
                    st.caption(f"  ↳ {ds['titulo'][:55]} · {len(arqs_ds)} arq ({tipos})")
                    for f in arqs_ds:
                        arquivos.append(f)
                        meta_map[f] = {"fonte": "zenodo", "titulo": ds.get("titulo", ""), "descricao": ds.get("descricao", "")}
                        novos += 1
                        _atualizar("arquivos", len(arquivos))

            s.update(label=f"🔬 Zenodo — {len(dss)} datasets · {novos} arquivos baixados",
                     state="complete", expanded=False)

    if not arquivos:
        return []

    # --- Análise paralela
    resumos = []

    def _analisar_um(caminho: str) -> dict | None:
        meta = meta_map.get(caminho, {})
        resumo = analisar_dataset(
            caminho,
            query=query_principal,
            titulo=meta.get("titulo", ""),
            descricao=meta.get("descricao", ""),
        )
        if resumo:
            resumo["fonte"] = meta.get("fonte", "web")
        return resumo

    MIN_RELEVANCIA = 20  # descarta arquivos claramente fora do tema

    with st.status(f"📊 Analisando {len(arquivos)} arquivos em paralelo", expanded=True) as s:
        with ThreadPoolExecutor(max_workers=4) as ex:
            futs = {ex.submit(_analisar_um, c): c for c in arquivos}
            for fut in as_completed(futs):
                resumo = fut.result()
                if resumo:
                    score = resumo.get("relevancia_ia", resumo["relevancia"])
                    if score >= MIN_RELEVANCIA:
                        resumos.append(resumo)
                        _atualizar("datasets", len(resumos))
                        st.caption(
                            f"• {resumo['arquivo'][:45]} — "
                            f"qualidade {resumo['qualidade']} · relevância IA {score}"
                        )
                    else:
                        st.caption(f"  ↳ descartado (relevância {score} < {MIN_RELEVANCIA}): "
                                   f"{resumo['arquivo'][:40]}")
        s.update(label=f"📊 {len(resumos)} relevantes de {len(arquivos)} analisados",
                 state="complete", expanded=False)

    return sorted(resumos, key=lambda x: x.get("relevancia_ia", x["relevancia"]), reverse=True)


# -------------------------------------------------------------------
# Session state
# -------------------------------------------------------------------
for key, default in {
    "chat_messages": [],
    "keywords": [],
    "keywords_prontas": False,
    "resultados": [],
    "buscou": False,
    "session_title": "",
    "search_saved": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# -------------------------------------------------------------------
# Layout
# -------------------------------------------------------------------
st.set_page_config(page_title="Data Hunter", page_icon="🔎", layout="wide")

# -------------------------------------------------------------------
# Sidebar — Histórico de buscas
# -------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🕓 Histórico de buscas")
    historico = list_searches(limit=30)

    if not historico:
        st.caption("Nenhuma busca realizada ainda.")
    else:
        for item in historico:
            kws = json.loads(item["keywords"])
            kws_preview = ", ".join(kws[:3]) + ("…" if len(kws) > 3 else "")
            col_a, col_b = st.columns([5, 1])
            with col_a:
                st.markdown(f"**{item['title']}**")
                st.caption(f"🗓 {item['created_at']} · 📦 {item['n_results']} datasets  \n🔑 {kws_preview}")
            btn_restaurar = col_a.button(
                "↩ Restaurar",
                key=f"hist_{item['id']}",
                use_container_width=True,
            )
            if btn_restaurar:
                # Restaura a busca anterior
                st.session_state.chat_messages = json.loads(item["chat"])
                st.session_state.keywords = kws
                st.session_state.keywords_prontas = True
                st.session_state.session_title = item["title"]
                st.session_state.resultados = []
                st.session_state.buscou = False
                st.session_state.search_saved = False
                st.rerun()

            if col_b.button("🗑️", key=f"del_{item['id']}", help="Remover"):
                delete_search(item["id"])
                st.rerun()

        st.divider()
        if st.button("🗑️ Limpar todo o histórico", use_container_width=True):
            clear_history()
            st.rerun()

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
col_chat_title, col_session_title = st.columns([3, 4])
col_chat_title.subheader("💬 O que você precisa?")
if st.session_state.session_title:
    col_session_title.markdown(
        f"<div style='padding-top:10px;font-size:1rem;color:#4C9BE8;font-weight:600'>"
        f"📌 {st.session_state.session_title}</div>",
        unsafe_allow_html=True,
    )

# Histórico do chat em container com scroll
chat_container = st.container(height=340)
with chat_container:
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            texto = msg["content"].split("KEYWORDS_JSON:")[0].strip()
            st.markdown(texto)

# Input fixo abaixo do histórico
with st.form("chat_form", clear_on_submit=True):
    col_input, col_btn = st.columns([6, 1])
    prompt = col_input.text_input(
        "chat",
        placeholder="Descreva os dados que você precisa...",
        label_visibility="collapsed",
    )
    enviar = col_btn.form_submit_button("Enviar ➤", use_container_width=True)

if enviar and prompt.strip():
    st.session_state.chat_messages.append({"role": "user", "content": prompt.strip()})

    # Gera título na primeira mensagem
    if not st.session_state.session_title:
        st.session_state.session_title = _gerar_titulo(prompt.strip())

    groq_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.chat_messages
    with st.spinner("Pensando..."):
        resposta = _chat_groq(groq_messages)
    st.session_state.chat_messages.append({"role": "assistant", "content": resposta})

    msgs_usuario = sum(1 for m in st.session_state.chat_messages if m["role"] == "user")
    if msgs_usuario >= 2:
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
    keywords_editadas = st.multiselect(
        label="keywords",
        options=st.session_state.keywords,
        default=st.session_state.keywords,
        label_visibility="collapsed",
    )

    col_add, col_btn, col_spacer = st.columns([3, 1, 3])
    nova_kw = col_add.text_input("Nova keyword", placeholder="ex: radar spectrum", label_visibility="collapsed")
    if col_btn.button("＋ Adicionar", use_container_width=True) and nova_kw.strip():
        if nova_kw.strip() not in st.session_state.keywords:
            st.session_state.keywords.append(nova_kw.strip())
        st.rerun()

    st.markdown("**Fontes de dados:**")
    fc1, fc2, fc3, fc4 = st.columns(4)
    usar_web     = fc1.checkbox("🌐 Web", value=True)
    usar_kaggle  = fc2.checkbox("🏆 Kaggle", value=True)
    usar_hf      = fc3.checkbox("🤗 Hugging Face", value=False)
    usar_zenodo  = fc4.checkbox("🔬 Zenodo", value=True)

    st.markdown("**Formatos aceitos:**")
    formatos = st.multiselect(
        "formatos",
        options=["csv", "xlsx", "json", "zip", "parquet"],
        default=["csv", "xlsx", "json", "zip"],
        label_visibility="collapsed",
    )

    st.markdown("")
    if st.button("🔍 Buscar e Analisar", type="primary", use_container_width=True):
        fontes = {"web": usar_web, "kaggle": usar_kaggle, "hf": usar_hf, "zenodo": usar_zenodo}
        kws_ativas = list(keywords_editadas) if keywords_editadas else st.session_state.keywords
        intencao_usuario = " ".join(
            m["content"] for m in st.session_state.chat_messages if m["role"] == "user"
        )

        # Métricas ao vivo
        st.markdown("**Progresso da busca:**")
        mc1, mc2, mc3, mc4 = st.columns(4)
        placeholders = {
            "variantes": mc1.empty(),
            "paginas":   mc2.empty(),
            "arquivos":  mc3.empty(),
            "datasets":  mc4.empty(),
        }
        _render_metricas({"variantes": 0, "paginas": 0, "arquivos": 0, "datasets": 0}, placeholders)

        st.session_state.resultados = _executar_busca(
            kws_ativas, fontes, list(formatos), intencao_usuario, placeholders
        )
        st.session_state.buscou = True
        st.session_state.search_saved = False
        st.rerun()

# -------------------------------------------------------------------
# Seção 3 — Resultados em cards
# -------------------------------------------------------------------
if st.session_state.buscou:
    st.divider()
    st.subheader("📦 Resultados")

    resumos = st.session_state.resultados

    # Salva no histórico uma única vez por busca
    if not st.session_state.search_saved:
        save_search(
            title=st.session_state.session_title or "Busca sem título",
            keywords=st.session_state.keywords,
            fontes={},
            n_results=len(resumos),
            chat=st.session_state.chat_messages,
        )
        st.session_state.search_saved = True

    if not resumos:
        st.warning("Nenhum dataset encontrado. Tente ajustar as keywords ou fontes.")
    else:
        st.caption(f"{len(resumos)} datasets encontrados · ordenados por relevância")

        # Gráfico comparativo
        df_res = pd.DataFrame(resumos)
        fig = px.bar(
            df_res, x="arquivo", y=["qualidade", "relevancia", "relevancia_ia"],
            barmode="group",
            color_discrete_map={"qualidade": "#4C9BE8", "relevancia": "#2ECC71", "relevancia_ia": "#9B59B6"},
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
            for key in ["chat_messages", "keywords", "keywords_prontas", "resultados", "buscou", "session_title", "search_saved"]:
                val = st.session_state[key]
                st.session_state[key] = [] if isinstance(val, list) else (False if isinstance(val, bool) else "")
            st.rerun()
