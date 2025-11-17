# app.py — versão atualizada com ICP CEMIG PF/PJ e SEM cred_path
import streamlit as st
import pandas as pd
from scraper_core import run_scraper

st.set_page_config(
    page_title="Scraper Inteligente - ICP CEMIG",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Scraper Inteligente - ICP CEMIG")

st.markdown("""
Este sistema coleta leads qualificados com base no **perfil ideal de cliente (ICP)** da CEMIG,
incluindo filtros PF/PJ, consumo mínimo, área de concessão e motivação para economia de energia.
""")

# ==========================================================
# FORMULÁRIO DE CONFIGURAÇÃO
# ==========================================================

st.header("🔎 Configuração de Pesquisa")

col1, col2 = st.columns(2)

with col1:
    tipo_cliente = st.radio(
        "Tipo de Cliente",
        ["Pessoa Física (PF)", "Pessoa Jurídica (PJ)"],
        index=1
    )

    if tipo_cliente == "Pessoa Física (PF)":
        consumo_minimo = st.number_input(
            "Consumo mínimo (R$ / mês)",
            min_value=0,
            value=500,
            help="PF deve gastar pelo menos R$ 500/mês"
        )
        tipo_icp = "PF"
    else:
        consumo_minimo = st.number_input(
            "Consumo mínimo por unidade consumidora (R$ / mês)",
            min_value=0,
            value=1000,
            help="PJ ideal ≥ R$ 1.000/mês por unidade"
        )
        tipo_icp = "PJ"

with col2:
    area_cemig = st.checkbox(
        "Apenas leads da área de concessão CEMIG",
        value=True
    )

    motivos = st.multiselect(
        "Motivações esperadas",
        [
            "redução de custo",
            "economia de energia",
            "energia sustentável",
            "economizar sem instalação",
            "benefícios ESG"
        ],
        default=["redução de custo", "economia de energia"]
    )

# ==========================================================
# CAMPOS DE BUSCA
# ==========================================================

st.header("📍 Campos de Busca")

c1, c2 = st.columns(2)

with c1:
    termos = st.text_area(
        "Termos de pesquisa",
        "empresa\ncomércio\nserviços gerais",
        help="Um termo por linha"
    ).split("\n")

with c2:
    cidades = st.text_area(
        "Cidades (ex: Belo Horizonte MG)",
        "Belo Horizonte MG\nJuiz de Fora MG",
        help="Uma cidade por linha"
    ).split("\n")

spreadsheet_name = st.text_input(
    "Nome da planilha no Google Sheets",
    value="Leads ICP"
)

# ==========================================================
# BOTÃO PRINCIPAL
# ==========================================================

st.markdown("---")

executar = st.button("🚀 Rodar Scraper")

progress_text = st.empty()
progress_bar = st.progress(0)

def progress_callback(done, total, pct):
    progress_text.text(f"Processando {done}/{total} ({pct}%) …")
    progress_bar.progress(pct)

# ==========================================================
# EXECUÇÃO
# ==========================================================

if executar:
    st.subheader("⏳ Rodando prospecção…")

    config = {
        "tipo_cliente": tipo_icp,
        "consumo_minimo": consumo_minimo,
        "area_cemig": area_cemig,
        "motivos": motivos,
        "termos": termos,
        "cidades": cidades,
        "spreadsheet_name": spreadsheet_name,
        "aba_resumo": "resumo_icp",
        "aba_leads": "leads_organizados"
    }

    leads = run_scraper(config, progress_callback=progress_callback)

    st.markdown("---")

    if not leads:
        st.error("Nenhum lead qualificado encontrado com esses filtros.")
    else:
        st.success(f"🎉 {len(leads)} leads qualificados encontrados!")

        df = pd.DataFrame(leads)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Baixar CSV",
            data=csv,
            file_name="leads_icp.csv",
            mime="text/csv"
        )
