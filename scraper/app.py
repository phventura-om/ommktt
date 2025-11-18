# ============================================================
# app.py — Layout OM MKT + Animações Premium (Versão Final)
# ============================================================

import streamlit as st
import pandas as pd
import time
from scraper_core import run_scraper

st.set_page_config(
    page_title="Scraper Inteligente — ICP CEMIG",
    page_icon="⚡",
    layout="wide",
)

# ============================================================
# CSS COMPLETO — animações, centralização, OM MKT e refinamento
# ============================================================
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: "Inter", sans-serif;
}

/* ====== ANIMAÇÕES GLOBAIS ====== */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInSlow {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ====== FUNDO OM MKT ====== */
.stApp {
    animation: fadeIn 1.2s ease-out;
    background:
        radial-gradient(circle at 5% 10%, rgba(0,180,255,0.15), transparent 60%),
        radial-gradient(circle at 95% 90%, rgba(0,255,180,0.12), transparent 60%),
        linear-gradient(145deg, #020814, #07101F 55%, #02050A 100%);
    color: #e6eefc;
}

/* ====== HEADER ====== */
.header {
    text-align: center;
    margin-top: 45px;
    animation: fadeInSlow 1.6s ease-out;
}
.header h1 {
    font-size: 40px;
    font-weight: 800;
}
.header p {
    margin-top: -10px;
    font-size: 14px;
    opacity: 0.82;
}

/* ====== CARD CENTRAL ====== */
.central-card {
    animation: fadeInSlow 1.4s ease-out;
    max-width: 650px;
    margin: 30px auto;
    background: rgba(15,23,42,0.75);
    backdrop-filter: blur(16px);
    border-radius: 20px;
    padding: 28px;
    border: 1px solid rgba(148,163,184,0.25);
    transition: 0.25s ease;
}
.central-card:hover {
    transform: translateY(-4px);
    border-color: rgba(0,255,200,0.45);
    box-shadow: 0 0 35px rgba(0,255,200,0.14);
}

/* ====== LABELS ====== */
label, .stRadio label {
    font-weight: 600 !important;
    color: #dce3f1 !important;
}

/* ====== INPUTS ====== */
textarea, input[type="text"], input[type="number"] {
    background: rgba(15,23,42,0.9) !important;
    border-radius: 12px !important;
    color: #e5e7eb !important;
    border: 1px solid rgba(148,163,184,0.35) !important;
    padding: 10px !important;
    transition: 0.15s ease;
}
textarea:focus, input:focus {
    border-color: rgba(0,255,200,0.4) !important;
    box-shadow: 0 0 18px rgba(0,255,200,0.25) !important;
}

/* ====== BOTÃO ====== */
.stButton > button {
    animation: fadeIn 1.2s ease-out;
    display: block;
    margin: 15px auto 0 auto;
    width: 90%;
    padding: 15px 0;

    border-radius: 999px;
    border: none;

    background: linear-gradient(90deg, #00E1FF, #00FFA2);
    color: black;
    font-size: 16px;
    font-weight: 700;

    transition: 0.25s ease;
    box-shadow: 0 0 18px rgba(0,255,200,0.3);
}
.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 30px rgba(0,255,200,0.45);
}

/* ====== MÉTRICAS ====== */
.metric-card {
    animation: fadeInSlow 1.4s ease-out;
    background: rgba(15,23,42,0.9);
    border-radius: 16px;
    padding: 18px;
    border: 1px solid rgba(148,163,184,0.35);
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

/* removendo padding padrão */
.block-container {
    padding-top: 0 !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER — CENTRALIZADO
# ============================================================
st.markdown("""
<div class="header">
    <h1>Scraper Inteligente — ICP CEMIG</h1>
    <p>Ferramenta avançada para captura de leads qualificados com filtros inteligentes.</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CARD PRINCIPAL — ESTILO OM MKT
# ============================================================
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

# ============================================================
# EXECUTAR SCRAPER
# ============================================================
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

# ============================================================
# DASHBOARD
# ============================================================
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
