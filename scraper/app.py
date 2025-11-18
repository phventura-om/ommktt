# app.py — versão final sem Pinn, centralizado e refinado
import time
import pandas as pd
import streamlit as st
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
# CSS FINAL REVISADO – SEM PINN E SEM FALHAS
# =========================================
CUSTOM_CSS = """
<style>

html, body, [class*="css"]  {
    font-family: "Inter", sans-serif;
}

/* ===== FUNDO EFEITO 3D SUAVE ===== */
.stApp {
    background:
        radial-gradient(circle at 25% 10%, rgba(76,150,250,0.18), transparent 55%),
        radial-gradient(circle at 75% 90%, rgba(56,189,248,0.18), transparent 55%),
        linear-gradient(145deg, #05070d, #0a0f1d 55%, #070a14 100%);
    color: #e6eefc;
}


/* ===== NAVBAR COMPACTA, SEM MARCA ===== */
.navbar {
    position: sticky;
    top: 0;
    z-index: 50;

    padding: 10px 0px;
    margin: -50px -75px 25px -75px;

    backdrop-filter: blur(18px);
    background: rgba(10,12,22,0.8);
    border-bottom: 1px solid rgba(180,200,255,0.12);
}

.nav-inner {
    max-width: 1180px;
    margin: 0 auto;
    display: flex;
    justify-content: center;
    align-items: center;
}

.nav-title {
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #e5e7eb;
}


/* ===== CARDS GLASS ===== */
.glass-card {
    background: rgba(15, 23, 42, 0.78);
    backdrop-filter: blur(14px);
    border-radius: 20px;
    border: 1px solid rgba(148, 163, 184, 0.35);
    padding: 24px;
    box-shadow:
        0 0 0 1px rgba(15, 23, 42, 0.9),
        0 18px 45px rgba(0, 0, 0, 0.8);
    transition: 0.2s ease;
}

.glass-card:hover {
    transform: translateY(-3px);
    border-color: rgba(129, 230, 217, 0.45);
}


/* ===== DIVISOR ===== */
.divider {
    height: 1px;
    margin: 20px 0;
    background: linear-gradient(
        90deg, transparent, rgba(76, 201, 240, 0.35), transparent
    );
}

/* ===== BOTÃO ===== */
.stButton > button {
    display: block;
    margin: 0 auto;
    width: 65%;
    padding: 14px 0;

    border-radius: 999px;
    border: none;

    background: linear-gradient(120deg, #4cc9f0, #4361ee);
    color: white;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;

    box-shadow:
        0 0 12px rgba(56, 189, 248, 0.45),
        0 0 25px rgba(56, 189, 248, 0.25);

    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow:
        0 0 18px rgba(56, 189, 248, 0.6),
        0 0 30px rgba(56, 189, 248, 0.45);
}


/* ===== INPUTS e TEXTAREAS ===== */
textarea, input[type="text"], input[type="number"] {
    background: rgba(15, 23, 42, 0.9) !important;
    border-radius: 14px !important;
    color: #e5e7eb !important;
    border: 1px solid rgba(148, 163, 184, 0.35) !important;
    padding: 10px !important;
}


/* ===== MÉTRICAS ===== */
.metric-card {
    background: rgba(15, 23, 42, 0.9);
    border-radius: 18px;
    padding: 16px 18px;
    border: 1px solid rgba(148, 163, 184, 0.35);
}

.metric-label {
    color: #9ca3af;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.16em;
}

.metric-value {
    font-size: 26px;
    font-weight: 700;
}

.metric-sub {
    font-size: 11px;
    color: #64748b;
}


/* ===== JARVIS LOADING ===== */
.jarvis-overlay {
    position: fixed;
    inset: 0;
    z-index: 9999;
    background:
        radial-gradient(circle at 20% 0, rgba(56,189,248,0.05), transparent 55%),
        radial-gradient(circle at 80% 100%, rgba(129,140,248,0.05), transparent 55%),
        rgba(3,7,18,0.97);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.jarvis-core {
    width: 90px;
    height: 90px;
    border-radius: 999px;
    border: 3px solid rgba(148,163,184,0.35);
    animation: rotate 3.2s linear infinite;
}

@keyframes rotate {
   from { transform: rotate(0); }
   to { transform: rotate(360deg); }
}

.jarvis-text {
    margin-top: 18px;
    font-size: 12px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #9ca3af;
}

</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# LOADING HTML
JARVIS_HTML = """
<div class="jarvis-overlay">
  <div class="jarvis-core"></div>
  <div class="jarvis-text">Processando scraper...</div>
</div>
"""


# =========================================
# NAVBAR (CENTRALIZADA E LIMPA)
# =========================================
st.markdown(
    """
<div class="navbar">
  <div class="nav-inner">
    <div class="nav-title">SCRAPER INTELIGENTE</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================
# HEADER CENTRALIZADO
# =========================================
st.markdown("")

st.markdown(
    """
<div style='text-align:center; margin-top:20px;'>
  <h1 style='font-weight:700;'>Scraper Inteligente — ICP CEMIG</h1>
  <p style='max-width:700px;margin:auto;font-size:14px;color:#cbd5e1;'>
     Ferramenta avançada para captura de leads qualificados com filtros inteligentes,
     análise ICP e exportação em CSV.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# =========================================
# CAMPOS CENTRALIZADOS DEFINITIVAMENTE
# =========================================
cols = st.columns([0.15, 0.35, 0.35, 0.15])
col_left = cols[1]
col_right = cols[2]


# ========== COLUNA ESQUERDA ==========
with col_left:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 🔧 Configuração de Pesquisa")

    tipo_cliente = st.radio("", ["PF", "PJ"], index=1, horizontal=True)
    apenas_cemig = st.checkbox("Apenas área CEMIG", True)
    min_consumo = st.slider("Consumo mínimo (R$)", 500, 20000, 1000, 500)

    motivacoes = st.text_input("Motivações esperadas", "redução de custo, economia de energia")
    motivacoes = [m.strip() for m in motivacoes.split(",")]

    st.markdown("</div>", unsafe_allow_html=True)


# ========== COLUNA DIREITA ==========
with col_right:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 🎯 Campos de Busca")

    termos_txt = st.text_area("Termos de busca", "empresa\ncomércio\nserviços gerais")
    termos_busca = [t.strip() for t in termos_txt.splitlines()]

    cidades_txt = st.text_area("Cidades", "Belo Horizonte MG\nJuiz de Fora MG")
    cidades = [c.strip() for c in cidades_txt.splitlines()]

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    executar = st.button("🚀 Rodar Scraper")

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================
# EXECUTAR SCRAPER
# =========================================
df = None

if executar:

    overlay = st.empty()
    overlay.markdown(JARVIS_HTML, unsafe_allow_html=True)

    time.sleep(0.4)

    config = {
        "tipo_cliente": tipo_cliente,
        "apenas_cemig": apenas_cemig,
        "min_consumo": min_consumo,
        "motivacoes": motivacoes,
        "termos_busca": termos_busca,
        "cidades": cidades,
    }

    result = run_scraper(config)
    overlay.empty()

    df = pd.DataFrame(result)


# =========================================
# DASHBOARD
# =========================================
st.markdown("### 📊 Dashboard de Leads")

if df is None or df.empty:
    st.info("Rode o scraper para visualizar os resultados.")
else:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Leads</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-value'>{len(df)}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Cidades</div>", unsafe_allow_html=True)
        if "cidade" in df:
            st.markdown(f"<div class='metric-value'>{df['cidade'].nunique()}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='metric-value'>{len(cidades)}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.dataframe(df, use_container_width=True, height=450)
