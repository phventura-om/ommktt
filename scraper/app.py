# app.py — Versão Premium UI 🧪⚡

import streamlit as st
import pandas as pd
from scraper_core import run_scraper

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================
st.set_page_config(
    page_title="Scraper ICP CEMIG",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================
# ESTILO PERSONALIZADO (CSS)
# ==============================
st.markdown("""
<style>
/* Remove espaço superior padrão */
#root > div:nth-child(1) { padding-top: 1rem !important; }

/* Card padrão */
.card {
    background-color: #111827;
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid #1f2937;
    margin-bottom: 1.5rem;
}

/* Seção título */
.section-title {
    font-size: 1.7rem;
    font-weight: 600;
    color: #38bdf8;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Badge PF/PJ */
.badge {
    display: inline-block;
    padding: 0.25rem 0.7rem;
    border-radius: 6px;
    background-color: #1e3a8a;
    color: white;
    margin-left: 8px;
    font-size: 0.8rem;
}

hr {
    border: none;
    border-top: 1px solid #1f2937;
}
</style>
""", unsafe_allow_html=True)


# ==============================
# HERO HEADER
# ==============================
st.markdown("""
<div style="padding: 1rem 0 2rem 0">
    <h1 style="font-size: 2.4rem; font-weight: 700; color: #fff;">
        ⚡ Scraper Inteligente — ICP CEMIG
    </h1>
    <p style="font-size: 1.1rem; color: #9ca3af; max-width: 800px;">
        Encontre automaticamente leads qualificados com base no perfil ideal de cliente (ICP) 
        da CEMIG. Personalize filtros PF/PJ, consumo mínimo, área de concessão e motivações de compra.
    </p>
</div>
""", unsafe_allow_html=True)


# ==============================
# SEÇÃO 1 — CONFIGURAÇÃO
# ==============================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🔍 Configuração de Pesquisa</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    tipo_cliente = st.radio(
        "**Tipo de Cliente**",
        ["Pessoa Física (PF)", "Pessoa Jurídica (PJ)"],
        index=1
    )

    if tipo_cliente == "Pessoa Física (PF)":
        consumo_minimo = st.number_input(
            "Consumo mínimo mensal (R$)",
            min_value=0,
            value=500,
            help="PF deve gastar pelo menos R$ 500/mês"
        )
        tipo_icp = "PF"
    else:
        consumo_minimo = st.number_input(
            "Consumo mínimo por unidade consumidora (R$)",
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

st.markdown("</div>", unsafe_allow_html=True)


# ==============================
# SEÇÃO 2 — CAMPOS DE BUSCA
# ==============================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📍 Campos de Busca</div>", unsafe_allow_html=True)

cb1, cb2 = st.columns([1, 1])

with cb1:
    termos = st.text_area(
        "Termos de pesquisa",
        "empresa\ncomércio\nserviços gerais",
        help="Um termo por linha"
    ).split("\n")

with cb2:
    cidades = st.text_area(
        "Cidades (ex: Belo Horizonte MG)",
        "Belo Horizonte MG\nJuiz de Fora MG",
        help="Uma cidade por linha"
    ).split("\n")

spreadsheet_name = st.text_input(
    "Nome da planilha no Google Sheets",
    value="Leads ICP"
)

st.markdown("</div>", unsafe_allow_html=True)


# ==============================
# BOTÃO DE EXECUÇÃO
# ==============================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🚀 Execução</div>", unsafe_allow_html=True)

executar = st.button("🔎 Rodar Scraper", use_container_width=True)

progress = st.empty()
bar = st.progress(0)

def progress_callback(done, total, pct):
    progress.text(f"Processando {done}/{total} ({pct}%)…")
    bar.progress(pct)

st.markdown("</div>", unsafe_allow_html=True)


# ==============================
# EXECUÇÃO DO SCRAPER
# ==============================
if executar:

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📡 Coleta de Dados</div>", unsafe_allow_html=True)

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

    if not leads:
        st.error("Nenhum lead qualificado encontrado.")
    else:
        st.success(f"🎉 {len(leads)} leads encontrados!")

        df = pd.DataFrame(leads)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Baixar CSV",
            data=csv,
            file_name="leads_icp.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)
