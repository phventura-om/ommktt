# app.py
import time
import pandas as pd
import streamlit as st

from scraper_core import run_scraper  # sua função de scraping


# =========================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================
st.set_page_config(
    page_title="Scraper Inteligente — ICP CEMIG",
    page_icon="⚡",
    layout="wide",
)

# =========================================
# CSS COMPLETO (FUTURISTA, OTIMIZADO e CENTRALIZADO)
# =========================================
CUSTOM_CSS = """
<style>

html, body, [class*="css"]  {
    font-family: "Inter", sans-serif;
}

/* ====== FUNDO 3D SUAVE ====== */
.stApp {
    background:
        radial-gradient(circle at 20% 0%, rgba(56, 189, 248, 0.18) 0%, transparent 45%),
        radial-gradient(circle at 80% 100%, rgba(129, 140, 248, 0.15) 0%, transparent 55%),
        linear-gradient(145deg, #05070d, #0a0f1d 55%, #070a14 100%);
    color: #e6eefc;
}

/* ========= NAVBAR COMPACTA ========= */
.navbar {
    position: sticky;
    top: 0;
    z-index: 50;
    padding: 10px 0px;
    margin: -50px -75px 15px -75px;
    backdrop-filter: blur(18px);
    background: rgba(10,12,22,0.72);
    border-bottom: 1px solid rgba(180,200,255,0.12);
}

.nav-inner {
    max-width: 1320px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.nav-left {
    display: flex;
    align-items: center;
    gap: 10px;
}

.nav-logo {
    width: 20px;
    height: 20px;
    border-radius: 999px;
    background: radial-gradient(circle at 30% 30%, #ffd43b, #ff922b);
    box-shadow: 0 0 10px rgba(255,200,60,0.6);
}

.nav-title {
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: #e5e7eb;
}

.nav-center {
    display: flex;
    gap: 16px;
    font-size: 13px;
    color: #9ca3af;
}

.nav-link {
    position: relative;
    cursor: pointer;
    padding: 4px 0;
    transition: color 0.18s ease;
}

.nav-link:hover {
    color: #e5e7eb;
}

.nav-right {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    color: #9ca3af;
}

.nav-chip {
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid rgba(148, 163, 184, 0.5);
    background: radial-gradient(circle at 0 0, rgba(76, 201, 240, 0.22), transparent);
}

/* ====== CARDS GLASS ====== */
.glass-card {
    background: rgba(15, 23, 42, 0.78);
    backdrop-filter: blur(14px);
    border-radius: 22px;
    border: 1px solid rgba(148, 163, 184, 0.35);
    padding: 24px 22px 20px 22px;
    box-shadow:
        0 0 0 1px rgba(15, 23, 42, 0.9),
        0 18px 45px rgba(0, 0, 0, 0.8),
        inset 0 0 16px rgba(15, 23, 42, 0.95);
    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
}

.glass-card:hover {
    transform: translateY(-4px);
    border-color: rgba(129, 230, 217, 0.55);
    box-shadow:
        0 30px 80px rgba(15, 23, 42, 0.95),
        0 0 35px rgba(56, 189, 248, 0.45);
}

/* ====== DIVISOR ====== */
.divider {
    height: 1px;
    margin: 15px 0;
    background: linear-gradient(
        90deg, transparent, rgba(76, 201, 240, 0.45), transparent
    );
}

/* ====== BOTÃO CENTRALIZADO ====== */
.stButton > button {
    display: block;
    margin: 0 auto;
    width: 65%;
    padding: 16px 0;
    border-radius: 999px;
    border: none;

    background: linear-gradient(120deg, #4cc9f0, #4361ee);
    color: white;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;

    box-shadow:
        0 0 0 2px rgba(56, 189, 248, 0.3),
        0 0 25px rgba(56, 189, 248, 0.6);

    transition: transform 0.2s ease, box-shadow 0.2s ease;
    animation: pulse 2s infinite;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow:
        0 0 0 2px rgba(56, 189, 248, 0.5),
        0 0 45px rgba(56, 189, 248, 0.9);
}

@keyframes pulse {
    0% { box-shadow: 0 0 12px rgba(56, 189, 248, 0.4); }
    50% { box-shadow: 0 0 28px rgba(56, 189, 248, 0.8); }
    100% { box-shadow: 0 0 12px rgba(56, 189, 248, 0.4); }
}

/* ========= INPUTS ========= */
textarea, input[type="text"], input[type="number"] {
    background: rgba(15, 23, 42, 0.88) !important;
    border-radius: 14px !important;
    color: #e5e7eb !important;
    border: 1px solid rgba(148, 163, 184, 0.35) !important;
    padding: 10px !important;
}

/* ====== MÉTRICAS ====== */
.metric-card {
    background: rgba(15, 23, 42, 0.92);
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

/* ====== JARVIS LOADING ====== */
.jarvis-overlay {
    position: fixed;
    inset: 0;
    z-index: 9999;
    background:
        radial-gradient(circle at 20% 0, rgba(56,189,248,0.22), transparent 55%),
        radial-gradient(circle at 80% 100%, rgba(129,140,248,0.22), transparent 55%),
        rgba(3,7,18,0.96);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.jarvis-core {
    width: 110px;
    height: 110px;
    border-radius: 999px;
    border: 3px solid rgba(148,163,184,0.7);
    box-shadow:
        0 0 40px rgba(56,189,248,0.8),
        0 0 120px rgba(37,99,235,0.9);
    animation: core-rotate 4s linear infinite;
    display: flex;
    align-items: center;
    justify-content: center;
}

.jarvis-core-inner {
    width: 40px;
    height: 40px;
    border-radius: 999px;
    background: radial-gradient(circle at 30% 30%, #e5e7eb, #60a5fa);
    animation: core-pulse 2s ease-in-out infinite;
}

@keyframes core-rotate {
    from { transform: rotate(0); }
    to { transform: rotate(360deg); }
}

@keyframes core-pulse {
    0%,100% { transform: scale(0.93); opacity: 0.8; }
    50% { transform: scale(1.05); opacity: 1; }
}

.jarvis-text {
    margin-top: 18px;
    font-size: 13px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #9ca3af;
}

</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# HTML overlay loading
JARVIS_HTML = """
<div class="jarvis-overlay">
  <div class="jarvis-core">
    <div class="jarvis-core-inner"></div>
  </div>
  <div class="jarvis-text">Analisando web...</div>
</div>
"""

# =========================================
# NAVBAR
# =========================================
st.markdown(
    """
<div class="navbar">
  <div class="nav-inner">
    <div class="nav-left">
      <div class="nav-logo"></div>
      <div class="nav-title">SCRAPER INTELIGENTE</div>
    </div>

    <div class="nav-center">
      <div class="nav-link">Dashboard</div>
      <div class="nav-link">ICP CEMIG</div>
      <div class="nav-link">Histórico</div>
      <div class="nav-link">Configurações</div>
    </div>

    <div class="nav-right">
      <span>Powered by</span>
      <div class="nav-chip">Pinn Growth</div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================================
# HEADER
# =========================================
st.markdown("")

col_h1, col_info = st.columns([2.8, 1.2])

with col_h1:
    st.markdown(
        "<h1>Scraper Inteligente — ICP CEMIG</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="font-size:14px;max-width:540px;color:#cbd5e1;">
        Encontre leads qualificados em minutos, filtrando consumo, região,
        motivação e exportando tudo em CSV. Tecnologia 100% autônoma.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_info:
    st.markdown(
        "<div style='text-align:right;font-size:12px;color:#94a3b8;'>Modo ativo: <b>ICP CEMIG</b><br>Última execução: —</div>",
        unsafe_allow_html=True,
    )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================================
# CAMPOS CENTRALIZADOS AGORA
# =========================================

centered_cols = st.columns([0.15, 0.35, 0.35, 0.15])
col_left = centered_cols[1]
col_right = centered_cols[2]

# -------- COLUNA ESQUERDA --------
with col_left:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("#### 🔧 Configuração de Pesquisa")

    st.caption("Tipo de Cliente")
    tipo_cliente = st.radio(
        "",
        ["Pessoa Física (PF)", "Pessoa Jurídica (PJ)"],
        index=1,
        horizontal=True,
        label_visibility="collapsed",
    )

    apenas_cemig = st.checkbox("Apenas área de concessão CEMIG", value=True)

    st.caption("Consumo mínimo por unidade (R$)")
    min_consumo = st.slider("", 500, 20000, 1000, 500)
    st.caption(f"Atual: R$ {min_consumo:,.0f}")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.caption("Motivações esperadas:")
    motivacoes = st.text_input("", "redução de custo, economia de energia")
    motivacoes = [m.strip() for m in motivacoes.split(",")]

    st.markdown("</div>", unsafe_allow_html=True)

# -------- COLUNA DIREITA --------
with col_right:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("#### 🎯 Campos de Busca")

    st.caption("Termos de busca (um por linha)")
    termos_text = st.text_area("", "empresa\ncomércio\nserviços gerais", height=110)
    termos_busca = [t.strip() for t in termos_text.splitlines()]

    st.caption("Cidades (uma por linha)")
    cidades_text = st.text_area("", "Belo Horizonte MG\nJuiz de Fora MG", height=90)
    cidades = [c.strip() for c in cidades_text.splitlines()]

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    executar = st.button("🚀 Rodar Scraper")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# EXECUÇÃO DO SCRAPER
# =========================================

df = None
stats = {}

if executar:
    overlay = st.empty()
    overlay.markdown(JARVIS_HTML, unsafe_allow_html=True)

    time.sleep(0.4)

    config = {
        "tipo_cliente": "PJ" if "Jurídica" in tipo_cliente else "PF",
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
    st.info("Rode o scraper para visualizar o dashboard com leads.")
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
        st.markdown(f"<div class='metric-value'>{df['cidade'].nunique() if 'cidade' in df else len(cidades)}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.dataframe(df, use_container_width=True, height=450)
