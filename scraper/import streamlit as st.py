import streamlit as st
import pandas as pd

from scraper_core import run_scraper


# ==========================================================
# ⚙️ CONFIG BÁSICA DA PÁGINA
# ==========================================================
st.set_page_config(
    page_title="Scraper de Leads – ICP Configurável",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Scraper de Leads – ICP Configurável")
st.markdown(
    """
Ferramenta para **prospecção automática** baseada em ICP.

1. Configure o ICP na barra lateral.
2. Clique em **"🚀 Iniciar prospecção"**.
3. Acompanhe o progresso e baixe o CSV ao final.
"""
)


# ==========================================================
# 🧩 HELPERS
# ==========================================================
def parse_multiline(text: str):
    """Quebra texto em linhas/; e remove vazios."""
    return [
        x.strip()
        for x in text.replace("\r", "\n").split("\n")
        if x.strip()
    ]


# ==========================================================
# 🧱 SIDEBAR – CONFIGURAÇÃO DO ICP
# ==========================================================
with st.sidebar:
    st.header("⚙️ Configuração do ICP")

    capital_min = st.number_input(
        "Capital social mínimo (R$)",
        value=300000,
        step=50000,
        min_value=0,
    )

    st.markdown("**Termos de busca (um por linha)**")
    termos_txt = st.text_area(
        "",
        value="hospital particular\nclínica hospitalar\ncentro médico",
        height=110,
        key="termos",
    )

    st.markdown("**Cidades (uma por linha – ex.: Belo Horizonte MG)**")
    cidades_txt = st.text_area(
        "",
        value="Belo Horizonte MG\nContagem MG\nJuiz de Fora MG",
        height=110,
        key="cidades",
    )

    st.markdown("**Palavras que indicam bom lead**  \n"
                "_(se houver, pelo menos uma precisa aparecer no texto)_")
    include_txt = st.text_area(
        "",
        value="hospital\nclínica\ncentro médico",
        height=90,
        key="include",
    )

    st.markdown("**Palavras que excluem lead**  \n"
                "_(se aparecer, a empresa é descartada)_")
    exclude_txt = st.text_area(
        "",
        value="farmácia\npet shop\nposto de saúde",
        height=90,
        key="exclude",
    )

    enviar_sheets = st.checkbox(
        "Enviar resultados para Google Sheets",
        value=True,
    )

    start = st.button("🚀 Iniciar prospecção", type="primary")


# ==========================================================
# ▶️ EXECUÇÃO DO SCRAPER
# ==========================================================
if start:
    termos = parse_multiline(termos_txt)
    cidades = parse_multiline(cidades_txt)
    include_keywords = parse_multiline(include_txt)
    exclude_keywords = parse_multiline(exclude_txt)

    if not termos:
        st.error("Adicione ao menos **um termo de busca**.")
        st.stop()
    if not cidades:
        st.error("Adicione ao menos **uma cidade**.")
        st.stop()

    st.subheader("🔄 Progresso da prospecção")

    progress_bar = st.progress(0)
    status_text = st.empty()

    # callback chamado pelo scraper_core.run_scraper
    def progress_callback(current, total, pct):
        progress_bar.progress(pct)
        status_text.write(f"Processando empresas: **{current}/{total}** ({pct}%)")

    config = {
        "termos": termos,
        "cidades": cidades,
        "capital_minimo": int(capital_min),
        "include_keywords": include_keywords,
        "exclude_keywords": exclude_keywords,
        "enviar_sheets": enviar_sheets,
    }

    # roda o motor do scraper
    leads = run_scraper(config, progress_callback=progress_callback)

    st.markdown("---")
    st.subheader("✅ Resultado")

    st.success(f"Prospecção concluída! Foram encontrados **{len(leads)}** leads quentes.")

    if leads:
        df = pd.DataFrame(leads)

        # Tabela resumida na tela
        cols_basicas = [
            "nome", "municipio", "capital", "porte",
            "email", "telefone", "whatsapp", "lead_score"
        ]
        cols_existentes = [c for c in cols_basicas if c in df.columns]

        st.markdown("### 📋 Leads encontrados (visão resumida)")
        st.dataframe(df[cols_existentes], use_container_width=True)

        # Download CSV
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Baixar CSV completo",
            data=csv_bytes,
            file_name="leads_quentes.csv",
            mime="text/csv",
        )

        st.markdown("### 🔍 Amostra de colunas completas")
        st.dataframe(df.head(10), use_container_width=True)
    else:
        st.info("Nenhum lead aprovado com o score mínimo atual.")
else:
    st.info("Configure o ICP na barra lateral e clique em **🚀 Iniciar prospecção**.")
