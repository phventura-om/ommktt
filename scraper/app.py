# ============================================================
# app.py — Layout 100% centralizado estilo OM MKT (VERSÃO FINAL)
# ============================================================

import streamlit as st
import pandas as pd
import time
from scraper_core import run_scraper

# =========================================
# CONFIG PÁGINA
# =========================================
st.set_page_config(
    page_title="Scraper Inteligente — ICP CEMIG",
    page_icon="⚡",
    layout="wide",
)

# =========================================
# CSS — versão OM MKT, centralizada, limpa e elegante
# =========================================
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: "Inter", sans-serif;
}

/* ===== FUNDO ===== */
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(76,150,250,0.16), transparent 60%),
        radial-gradient(circle at 90% 90%, rgba(56,189,248,0.16), transparent 60%),
        linear-gradient(145deg, #030712, #0A0F1D 55%, #05070D);
    color: #e6eefc;
}

/* ===== HEADER CENTRAL ===== */
.header {
    text-align: center;
    margin-top: 40px;
    margin-bottom: 10px;
}
.header h1 {
    font-size: 40px;
    font-weight: 800;
}
.header p {
    margin-top: -10px;
    opacity: 0.85;
}

/* ===== CARD CENTRAL ===== */
.central-card {
    max-width: 650px;
    margin: 0 auto;
    background: rgba(15, 23, 42, 0.75);
    backdrop-filter: blur(14px);
    border-radius: 20px;
    padding: 25px 25px 25px 25px;
    border: 1px solid rgba(148,163,184,0.28);

    box-shadow:
        0px 4px 25px rgba(0,0,0,0.4),
        inset 0px 0px 12px rgba(255,255,255,0.04);
}

.central-card:hover {
    border-color: rgba(129, 230, 217, 0.45);
}

/* ===== INPUTS ===== */
textarea, input[type="text"], input[type="number"] {
    background: rgba(15, 23, 42, 0.9) !important;
    border-radius: 12px !important;
    color: #e5e7eb !important;
    border: 1px solid rgba(148, 163, 184, 0.35) !important;
    padding: 10px !important;
}

/* ===== LABELS ===== */
label, .stRadio label {
    font-weight: 600 !important;
    color: #dce3f1 !important;
}

/* ===== BOTÃO CENTRAL ===== */
.stButton > button {
    display: block;
    margin: 0 auto;
    width: 90%;
    padding: 14px 0;

    border-radius: 999px;
    border: none;

    background: linear-gradient(90deg, #00E1FF, #00FFA2);
    color: black;
    font-size: 16px;
    font-weight: 700;

    transition: 0.15s ease;
}
.stButton > button:hover {
    transform: translateY(-3px);
}

/* ===== DASHBOARD ===== */
.metric-card {
    background: rgba(15, 23, 42, 0.9);
    border-radius: 16px;
    border: 1px solid rgba(148,163,184,0.35);
    padding: 16px 18px;
}

.metric-label {
    color: #9ca3af;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

.metric-value {
    font-size: 28px;
    font-weight: 700;
}

/* remover margem do topo */
.block-container {
    padding-top: 0 !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================
# HEADER SEM NADA LATERAL — 100% CENTRAL
# =========================================
st.markdown("""
<div class="header">
    <h1>Scraper Inteligente — ICP CEMIG</h1>
    <p>Ferramenta avançada para captura de leads qualificados com filtros inteligentes.</p>
</div>
""", unsafe_allow_html=True)


# =========================================
# CARD CENTRAL — estilo OM MKT
# =========================================
st.markdown('<div class="central-card">', unsafe_allow_html=True)

st.markdown("### Configuração do ICP")

tipo_cliente = st.radio("Tipo de cliente:", ["PF", "PJ"], index=1, horizontal=True)

min_consumo = st.slider("Consumo mínimo (R$):", 500, 20000, 1000, 500)

motivacoes = st.text_input("Motivações esperadas:", "redução de custo, economia de energia")
motivacoes = [m.strip() for m in motivacoes.split(",")]

st.markdown("### Termos de busca (um por linha)")
termos_txt = st.text_area("", "empresa\ncomércio\nserviços gerais", height=100)
termos_busca = [t.strip() for t in termos_txt.splitlines()]

st.markdown("### Cidades (uma por linha)")
cidades_txt = st.text_area("", "Belo Horizonte MG\nJuiz de Fora MG", height=90)
cidades = [c.strip() for c in cidades_txt.splitlines()]

executar = st.button("🚀 Rodar Scraper")

st.markdown("</div>", unsafe_allow_html=True)


# =========================================
# RUN SCRAPER
# =========================================
df = None

if executar:
    with st.spinner("Processando..."):
        config = {
            "tipo_cliente": tipo_cliente,
            "min_consumo": min_consumo,
            "motivacoes": motivacoes,
            "termos_busca": termos_busca,
            "cidades": cidades,
        }
        result = run_scraper(config)
        df = pd.DataFrame(result)


# =========================================
# DASHBOARD CENTRALIZADO
# =========================================
st.markdown("<br><h3 style='text-align:center;'>📊 Dashboard de Leads</h3>", unsafe_allow_html=True)

if df is None or df.empty:
    st.info("Rode o scraper para visualizar os resultados.")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Total de Leads</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{len(df)}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Cidades Únicas</div>", unsafe_allow_html=True)
        if "cidade" in df.columns:
            st.markdown(f"<div class='metric-value'>{df['cidade'].nunique()}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='metric-value'>—</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
