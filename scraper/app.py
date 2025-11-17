import streamlit as st
import pandas as pd
from scraper_core import run_scraper

st.set_page_config(page_title="Scraper ICP CEMIG", page_icon="⚡", layout="wide")

st.title("⚡ Scraper Inteligente — ICP CEMIG")
st.markdown("Encontre leads qualificados e baixe tudo em CSV, sem dependência de Google Sheets.")

st.header("🔍 Configuração de Pesquisa")

col1, col2 = st.columns(2)

with col1:
    tipo_cliente = st.radio("Tipo de Cliente", ["Pessoa Física (PF)", "Pessoa Jurídica (PJ)"], index=1)

    if tipo_cliente == "Pessoa Física (PF)":
        consumo_minimo = st.number_input("Consumo mínimo mensal (R$)", min_value=0, value=500)
        tipo_icp = "PF"
    else:
        consumo_minimo = st.number_input("Consumo mínimo por unidade (R$)", min_value=0, value=1000)
        tipo_icp = "PJ"

with col2:
    area_cemig = st.checkbox("Apenas área de concessão CEMIG", value=True)

    motivos = st.multiselect(
        "Motivações esperadas",
        ["redução de custo", "economia de energia", "energia sustentável", "economizar sem instalação", "benefícios ESG"],
        default=["redução de custo", "economia de energia"]
    )

st.header("📍 Campos de Busca")

col3, col4 = st.columns(2)

with col3:
    termos = st.text_area("Termos de pesquisa", "empresa\ncomércio\nserviços gerais").split("\n")

with col4:
    cidades = st.text_area("Cidades", "Belo Horizonte MG\nJuiz de Fora MG").split("\n")

st.markdown("---")

if st.button("🚀 Rodar Scraper"):
    progress = st.empty()
    bar = st.progress(0)

    def callback(done, total, pct):
        progress.text(f"Processando {done}/{total} ({pct}%)…")
        bar.progress(pct)

    config = {
        "tipo_cliente": tipo_icp,
        "consumo_minimo": consumo_minimo,
        "area_cemig": area_cemig,
        "motivos": motivos,
        "termos": termos,
        "cidades": cidades
    }

    leads = run_scraper(config, progress_callback=callback)

    if not leads:
        st.error("Nenhum lead qualificado foi encontrado.")
    else:
        st.success(f"{len(leads)} leads encontrados!")

        df = pd.DataFrame(leads)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Baixar CSV", data=csv, file_name="leads_icp.csv", mime="text/csv")
