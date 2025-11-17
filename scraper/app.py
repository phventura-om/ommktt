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
# ESTILO CUSTOMIZADO (DARK FUTURISTA + ANIMAÇÕES)
# =========================================
CUSTOM_CSS = """
<style>
/* ====== BACKGROUND 3D FUTURISTA ====== */
.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(76, 201, 240, 0.32) 0, transparent 45%),
        radial-gradient(circle at 90% 0%, rgba(67, 97, 238, 0.32) 0, transparent 50%),
        radial-gradient(circle at 10% 100%, rgba(244, 114, 182, 0.24) 0, transparent 45%),
        linear-gradient(140deg, #020617 0%, #020715 45%, #020617 100%);
    color: #e6eefc;
    font-family: "Inter", system-ui, sans-serif;
}

/* ====== NAVBAR SUPERIOR ====== */
.navbar {
    position: sticky;
    top: 0;
    z-index: 50;
    padding: 12px 32px 6px 32px;
    margin: -30px -80px 18px -80px;
    backdrop-filter: blur(20px);
    background: linear-gradient(
        120deg,
        rgba(15, 23, 42, 0.85),
        rgba(15, 23, 42, 0.65),
        rgba(15, 23, 42, 0.85)
    );
    border-bottom: 1px solid rgba(148, 163, 184, 0.35);
    box-shadow:
        0 12px 30px rgba(0, 0, 0, 0.75),
        0 0 0 1px rgba(15, 23, 42, 0.9);
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
    width: 24px;
    height: 24px;
    border-radius: 999px;
    background: radial-gradient(circle at 30% 30%, #facc15, #f97316, #f97316);
    box-shadow: 0 0 16px rgba(250, 204, 21, 0.75);
}

.nav-title {
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #e5e7eb;
}

.nav-center {
    display: flex;
    gap: 18px;
    font-size: 13px;
    color: #9ca3af;
}

.nav-link {
    position: relative;
    cursor: pointer;
    padding: 4px 0;
    transition: color 0.18s ease;
}

.nav-link::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: -3px;
    width: 0%;
    height: 2px;
    border-radius: 999px;
    background: linear-gradient(90deg, #4cc9f0, #4361ee);
    transition: width 0.24s ease;
}

.nav-link:hover {
    color: #e5e7eb;
}

.nav-link:hover::after {
    width: 100%;
}

.nav-right {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 11px;
    color: #9ca3af;
}

.nav-chip {
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid rgba(148, 163, 184, 0.5);
    background: radial-gradient(circle at 0 0, rgba(76, 201, 240, 0.22), transparent);
}

/* ====== DIVISOR GRADIENTE ====== */
.divider {
    height: 1px;
    margin: 18px 0;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(76, 201, 240, 0.4),
        rgba(129, 140, 248, 0.4),
        transparent
    );
}

/* ====== CARDS GLASS ANIMADOS ====== */
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
    transform: translateY(-4px) translateZ(0);
    border-color: rgba(129, 230, 217, 0.55);
    box-shadow:
        0 30px 80px rgba(15, 23, 42, 0.95),
        0 0 35px rgba(56, 189, 248, 0.45);
}

/* ====== BOTÃO ANIMADO (HOVER + CLICK + PULSE) ====== */
.stButton > button {
    display: block;
    margin: 0 auto;
    width: 60%;
    padding: 14px 0;
    border-radius: 999px;
    border: none;

    background: radial-gradient(circle at 0 0, #4cc9f0, transparent 55%),
                linear-gradient(120deg, #4cc9f0, #4361ee);
    color: #f9fafb;
    font-size: 16px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;

    box-shadow:
        0 0 0 1px rgba(15, 23, 42, 0.9),
        0 16px 38px rgba(37, 99, 235, 0.7),
        0 0 26px rgba(56, 189, 248, 0.7);

    cursor: pointer;
    transition: transform 0.18s ease, box-shadow 0.18s ease, opacity 0.18s ease;
    animation: btn-pulse 2.2s infinite;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow:
        0 0 0 1px rgba(59, 130, 246, 0.9),
        0 20px 55px rgba(37, 99, 235, 0.9),
        0 0 40px rgba(56, 189, 248, 0.85);
}

.stButton > button:active {
    transform: translateY(0px) scale(0.97);
    box-shadow:
        0 0 0 1px rgba(15, 23, 42, 0.95),
        0 8px 24px rgba(15, 23, 42, 0.9);
    opacity: 0.9;
}

/* PULSO DO BOTÃO */
@keyframes btn-pulse {
    0% { box-shadow:
            0 0 0 1px rgba(15, 23, 42, 0.9),
            0 16px 38px rgba(37, 99, 235, 0.7),
            0 0 18px rgba(56, 189, 248, 0.55); }
    50% { box-shadow:
            0 0 0 1px rgba(56, 189, 248, 0.8),
            0 20px 55px rgba(37, 99, 235, 0.9),
            0 0 40px rgba(56, 189, 248, 0.95); }
    100% { box-shadow:
            0 0 0 1px rgba(15, 23, 42, 0.9),
            0 16px 38px rgba(37, 99, 235, 0.7),
            0 0 18px rgba(56, 189, 248, 0.55); }
}

/* ====== INPUTS / TEXTAREAS ====== */
textarea, input[type="text"], input[type="number"] {
    background: radial-gradient(circle at 0 0, rgba(56, 189, 248, 0.12), transparent 60%),
                rgba(15, 23, 42, 0.92) !important;
    color: #e5e7eb !important;
    border-radius: 14px !important;
    border: 1px solid rgba(148, 163, 184, 0.6) !important;
    font-size: 13px !important;
    box-shadow:
        0 0 0 1px rgba(15, 23, 42, 0.9),
        inset 0 0 12px rgba(15, 23, 42, 0.9);
    transition: box-shadow 0.2s ease, border-color 0.2s ease, background 0.2s ease;
}

textarea:focus, input[type="text"]:focus, input[type="number"]:focus {
    border-color: rgba(56, 189, 248, 0.9) !important;
    box-shadow:
        0 0 0 1px rgba(56, 189, 248, 0.9),
        0 0 26px rgba(56, 189, 248, 0.5),
        inset 0 0 14px rgba(15, 23, 42, 0.95);
}

/* ====== MÉTRICAS ====== */
.metric-card {
    background: radial-gradient(circle at 0 0, rgba(56, 189, 248, 0.12), transparent 60%),
                rgba(15, 23, 42, 0.92);
    border-radius: 18px;
    padding: 16px 18px;
    border: 1px solid rgba(148, 163, 184, 0.55);
    box-shadow:
        0 0 0 1px rgba(15, 23, 42, 1),
        0 12px 30px rgba(15, 23, 42, 0.9);
}

.metric-label {
    color: #94a3b8;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.16em;
}

.metric-value {
    font-size: 24px;
    font-weight: 700;
    margin-top: 4px;
}

.metric-sub {
    font-size: 11px;
    color: #64748b;
}

/* ====== TABELA ====== */
.dataframe td, .dataframe th {
    background: rgba(15, 23, 42, 0.96) !important;
    border-color: rgba(31, 41, 55, 0.9) !important;
    color: #e5e7eb !important;
    font-size: 12px !important;
}

/* ====== OVERLAY JARVIS LOADING ====== */
.jarvis-overlay {
    position: fixed;
    inset: 0;
    z-index: 9999;
    background:
        radial-gradient(circle at 20% 0, rgba(56, 189, 248, 0.22), transparent 55%),
        radial-gradient(circle at 80% 100%, rgba(129, 140, 248, 0.22), transparent 55%),
        rgba(3, 7, 18, 0.96);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.jarvis-core {
    width: 110px;
    height: 110px;
    border-radius: 999px;
    border: 3px solid rgba(148, 163, 184, 0.7);
    box-shadow:
        0 0 40px rgba(56, 189, 248, 0.8),
        0 0 120px rgba(37, 99, 235, 0.9);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: core-rotate 4s linear infinite;
}

.jarvis-core-inner {
    width: 40px;
    height: 40px;
    border-radius: 999px;
    background: radial-gradient(circle at 30% 30%, #e5e7eb, #60a5fa);
    box-shadow: 0 0 35px rgba(96, 165, 250, 1);
    animation: core-pulse 2s ease-in-out infinite;
}

.jarvis-ring {
    position: absolute;
    inset: -18px;
    border-radius: 999px;
    border: 1px dashed rgba(148, 163, 184, 0.45);
    animation: ring-rotate 10s linear infinite;
}

.jarvis-scan-line {
    width: 60%;
    height: 2px;
    margin-top: 40px;
    border-radius: 999px;
    background: linear-gradient(90deg, transparent, #38bdf8, transparent);
    animation: scan-move 1.6s ease-in-out infinite;
}

.jarvis-text {
    margin-top: 18px;
    font-size: 13px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #9ca3af;
}

/* ANIMAÇÕES JARVIS */
@keyframes core-rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@keyframes core-pulse {
    0%, 100% { transform: scale(0.94); opacity: 0.9; }
    50% { transform: scale(1.05); opacity: 1; }
}

@keyframes ring-rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(-360deg); }
}

@keyframes scan-move {
    0% { transform: translateX(-40%); opacity: 0; }
    30% { opacity: 1; }
    70% { opacity: 1; }
    100% { transform: translateX(40%); opacity: 0; }
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# HTML do overlay JARVIS (usado só quando rodar o scraper)
JARVIS_HTML = """
<div class="jarvis-overlay">
  <div class="jarvis-core">
    <div class="jarvis-ring"></div>
    <div class="jarvis-core-inner"></div>
  </div>
  <div class="jarvis-scan-line"></div>
  <div class="jarvis-text">
    Analisando web • Qualificando ICP • Preparando leads...
  </div>
</div>
"""

# =========================================
# NAVBAR SUPERIOR
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
# HEADER PRINCIPAL
# =========================================
st.markdown("")

col_header_left, col_header_right = st.columns([2.8, 1.2])

with col_header_left:
    st.markdown(
        "<h1>Scraper Inteligente — ICP CEMIG</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="font-size:13px;color:#cbd5f5;max-width:520px;">
        Encontre leads qualificados em minutos, com filtros avançados de consumo, motivação e região,
        exportando tudo em CSV sem depender de planilhas conectadas.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_header_right:
    st.markdown(
        """
        <div style="text-align:right;font-size:11px;color:#94a3b8;">
          Modo ativo: <span style="color:#a5b4fc;">ICP CEMIG</span><br/>
          Última execução: <span style="color:#e5e7eb;">—</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# =========================================
# LAYOUT PRINCIPAL (CONFIG + CAMPOS DE BUSCA)
# =========================================
col_left, col_right = st.columns([1.05, 0.95])

# ---------- COLUNA ESQUERDA: CONFIG ---------
with col_left:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    st.markdown("#### 🔧 Configuração de Pesquisa")

    # Tipo de cliente
    st.caption("Tipo de Cliente")
    tipo_cliente = st.radio(
        "Selecione o tipo de cliente",
        ["Pessoa Física (PF)", "Pessoa Jurídica (PJ)"],
        index=1,
        horizontal=True,
        label_visibility="collapsed",
    )

    # Apenas área CEMIG
    apenas_cemig = st.checkbox("Apenas área de concessão CEMIG", value=True)

    # Consumo mínimo
    st.caption("Consumo mínimo por unidade (R$)")
    min_consumo = st.slider(
        "Consumo mínimo por unidade",
        min_value=500,
        max_value=20000,
        step=500,
        value=1000,
        label_visibility="collapsed",
    )
    st.markdown(
        f"<span style='font-size:13px;color:#e5e7eb;'>Atual: <b>R$ {min_consumo:,.0f}</b> por unidade</span>",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Motivações esperadas
    st.caption("Motivações esperadas (palavras-chave para qualificação)")
    motivacoes_default = "redução de custo, economia de energia"
    motivacoes_text = st.text_input(
        "Motivações separadas por vírgula",
        value=motivacoes_default,
        label_visibility="collapsed",
    )
    motivacoes = [m.strip() for m in motivacoes_text.split(",") if m.strip()]

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- COLUNA DIREITA: CAMPOS DE BUSCA ---------
with col_right:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    st.markdown("#### 🎯 Campos de Busca")

    st.caption("Termos de pesquisa (um por linha)")
    termos_default = "empresa\ncomércio\nserviços gerais"
    termos_text = st.text_area(
        "Termos de pesquisa",
        value=termos_default,
        height=110,
        label_visibility="collapsed",
    )
    termos_busca = [t.strip() for t in termos_text.splitlines() if t.strip()]

    st.caption("Cidades (uma por linha)")
    cidades_default = "Belo Horizonte MG\nJuiz de Fora MG"
    cidades_text = st.text_area(
        "Cidades",
        value=cidades_default,
        height=90,
        label_visibility="collapsed",
    )
    cidades = [c.strip() for c in cidades_text.splitlines() if c.strip()]

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Botão centralizado
    st.markdown("<div style='display:flex;justify-content:center;width:100%;'>", unsafe_allow_html=True)
    executar = st.button("🚀 Rodar Scraper", use_container_width=False)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# EXECUÇÃO DO SCRAPER
# =========================================
df_resultado = None
stats = {}
df_filtrado = None

if executar:
    # Overlay estilo Jarvis
    overlay = st.empty()
    overlay.markdown(JARVIS_HTML, unsafe_allow_html=True)

    # Pequeno delay visual (opcional)
    time.sleep(0.4)

    # Monta config
    config = {
        "tipo_cliente": "PJ" if "Jurídica" in tipo_cliente else "PF",
        "apenas_cemig": apenas_cemig,
        "min_consumo": min_consumo,
        "motivacoes": motivacoes,
        "termos_busca": termos_busca,
        "cidades": cidades,
    }

    # Execução do scraper
    leads = run_scraper(config=config)

    # Some overlay
    overlay.empty()

    # Trata retorno
    if isinstance(leads, pd.DataFrame):
        df_resultado = leads.copy()
    else:
        df_resultado = pd.DataFrame(leads)

    if not df_resultado.empty:
        df_resultado.columns = [str(c) for c in df_resultado.columns]

        stats["total_leads"] = len(df_resultado)

        col_municipio = None
        for c in df_resultado.columns:
            if c.lower() in ("municipio", "cidade", "cidade_uf", "cidade_estado"):
                col_municipio = c
                break
        if col_municipio:
            stats["qtd_cidades"] = df_resultado[col_municipio].nunique()
        else:
            stats["qtd_cidades"] = len(cidades)

        col_consumo = None
        for c in df_resultado.columns:
            if "consumo" in c.lower() or "fatura" in c.lower():
                col_consumo = c
                break
        if col_consumo:
            try:
                stats["media_consumo"] = float(
                    pd.to_numeric(df_resultado[col_consumo], errors="coerce").mean()
                )
            except Exception:
                stats["media_consumo"] = None
        else:
            stats["media_consumo"] = None

    st.success("Scraper finalizado com sucesso ✅")

# =========================================
# DASHBOARD / RESULTADOS
# =========================================
st.markdown("")
st.markdown("### 📊 Dashboard de Leads")

if df_resultado is None or df_resultado.empty:
    st.info("Rode o scraper para visualizar o dashboard com os leads qualificados.")
else:
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

    with col_kpi1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Leads qualificados</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='metric-value'>{stats.get('total_leads', 0)}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='metric-sub'>Base atual filtrada</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_kpi2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Cidades</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='metric-value'>{stats.get('qtd_cidades', len(cidades))}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='metric-sub'>Área de atuação</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_kpi3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Consumo mínimo</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='metric-value'>R$ {min_consumo:,.0f}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='metric-sub'>Por unidade consumidora</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_kpi4:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Motivações</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='metric-value'>{len(motivacoes)}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='metric-sub'>Palavras-chave ativas</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")

    # Gráfico por cidade (se houver coluna)
    col_chart, col_side = st.columns([1.8, 1])

    col_municipio = None
    for c in df_resultado.columns:
        if c.lower() in ("municipio", "cidade", "cidade_uf", "cidade_estado"):
            col_municipio = c
            break

    with col_chart:
        st.markdown("#### Distribuição de leads por cidade")
        if col_municipio:
            top_cidades = (
                df_resultado[col_municipio]
                .value_counts()
                .reset_index()
                .rename(columns={"index": "Cidade", col_municipio: "Leads"})
            )
            st.bar_chart(top_cidades, x="Cidade", y="Leads")
        else:
            st.caption("Nenhuma coluna de cidade identificada automaticamente no retorno do scraper.")

    with col_side:
        st.markdown("#### Exportar / filtros rápidos")

        if col_municipio:
            cidades_unicas = sorted(df_resultado[col_municipio].dropna().unique())
            cidade_filtro = st.selectbox(
                "Filtrar por cidade",
                options=["Todas"] + list(cidades_unicas),
            )
            if cidade_filtro != "Todas":
                df_filtrado = df_resultado[df_resultado[col_municipio] == cidade_filtro]
            else:
                df_filtrado = df_resultado
        else:
            df_filtrado = df_resultado

        csv_bytes = df_filtrado.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="⬇️ Baixar CSV dos leads",
            data=csv_bytes,
            file_name="leads_icp_cemig.csv",
            mime="text/csv",
            use_container_width=True,
        )
        st.caption("Use este CSV em qualquer CRM, Google Sheets ou painel interno.")

    st.markdown("---")
    st.markdown("#### 📄 Leads detalhados")
    st.dataframe(df_filtrado, use_container_width=True, height=420)
