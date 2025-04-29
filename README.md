<p align="center">
  <img src="logo.png" alt="Data Hunter Logo" width="400">
</p>

<h1 align="center">🔎 Data Hunter 5.2 Alpha</h1>
<p align="center">
Busca Inteligente e Análise Automatizada de Datasets Públicos.<br>
</p>

<p align="center">
  <a href="https://streamlit.io/">
    <img alt="Streamlit" src="https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?logo=streamlit">
  </a>
  <a href="https://www.python.org/">
    <img alt="Python Version" src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python">
  </a>
</p>

---

# 📦 Funcionalidades

- 🔍 Busca fontes confiáveis (.gov, .edu, Kaggle, entre outros)
- 🛡️ Validação avançada de links, botões e tabelas HTML
- 🧠 Detecção de APIs JSON ocultas (XHR)
- 💾 Download robusto e descompactação de arquivos ZIP
- 📊 Análise automática de datasets (linhas, colunas, tipos, nulos)
- 🧩 Análise semântica baseada em nomes de colunas
- 📈 Ranking interativo dos datasets obtidos
- 📥 Download zipado de todos os datasets encontrados

---

# 🚀 Como Rodar Localmente

```bash
# Instale as dependências
pip install -r requirements.txt

# Rode o aplicativo
streamlit run app.py

# 🌎 Deploy Online

O Data Hunter foi desenvolvido para fácil deploy no Streamlit Community Cloud.

Para implantar:
	1.	Faça fork/clonagem deste repositório.
	2.	No Streamlit Cloud, crie um novo app apontando para o arquivo app.py.
	3.	Certifique-se que o requirements.txt está correto e atualizado.

---

# 📚 Tecnologias

	•	Python 3.10+
	•	Streamlit
	•	DuckDuckGo Search API
	•	BeautifulSoup4
	•	Selenium + WebDriver Manager
	•	Requests
	•	Pandas
	•	Plotly
