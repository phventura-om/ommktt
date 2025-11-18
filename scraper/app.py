import io
import streamlit as st
import pandas as pd

from scraper_core import run_scraper

# ----------------------------------------------------------
# CONFIG DA PÁGINA
# ----------------------------------------------------------
st.set_page_config(
    page_title="OM MKT · Lead Scraper",
    layout="wide",
)

# ----------------------------------------------------------
# ESTILO FUTURISTA
# ----------------------------------------------------------
st.markdown(
    """
    <style>
    /* Fundo com vibe de painel holográfico */
    body {
        background: radial-gradient(circle at 5% 0%, #1f2937 0, #020617 45%, #000 100%);
        color: #e5e7eb;
        font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .main {
        background: transparent;
    }
    .block-container {
        max-width: 1120px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    /* Hero wrapper */
    .hero-shell {
        position: relative;
        overflow: hidden;
        border-radius: 24px;
        padding: 1.6rem 2rem;
        margin-bottom: 1.8rem;
        background:
            radial-gradient(circle at -10% -10%, rgba(96,165,250,0.25), transparent 55%),
            radial-gradient(circle at 110% 0%, rgba(236,72,153,0.25), transparent 55%),
            linear-gradient(135deg, rgba(15,23,42,0.98), rgba(15,23,42,0.94));
        border: 1px solid rgba(148,163,253,0.35);
        box-shadow:
            0 0 0 1px rgba(15,23,42,0.95),
            0 28px 70px rgba(0,0,0,0.9);
    }
    .hero-orbit {
        position: absolute;
        inset: -40%;
        background:
            radial-gradient(circle at 0% 0%, rgba(59,130,246,0.18), transparent 55%),
            radial-gradient(circle at 100% 100%, rgba(34,211,238,0.18), transparent 60%);
        opacity: 0.8;
        filter: blur(2px);
        pointer-events: none;
    }
    .hero-content {
        position: relative;
        z-index: 1;
        display: grid;
        grid-template-columns: minmax(0, 3fr) minmax(0, 2.4fr);
        gap: 1.8rem;
        align-items: center;
    }

    /* Logo / título à esquerda */
    .om-logo-stack {
        display: flex;
        flex-direction: column;
        gap: 0.9rem;
    }
    .om-logo-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.42rem 0.9rem;
        border-radius: 999px;
        border: 1px solid rgba(96,165,250,0.6);
        background: radial-gradient(circle at 0 0, rgba(59,130,246,0.8), rgba(15,23,42,0.85));
        box-shadow:
            0 0 0 1px rgba(15,23,42,0.9),
            0 0 22px rgba(56,189,248,0.7);
    }
    .om-logo-mark {
        width: 26px;
        height: 26px;
        border-radius: 10px;
        background: conic-gradient(from 210deg, #22d3ee, #4f46e5, #ec4899, #22d3ee);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 16px rgba(59,130,246,0.85);
    }
    .om-logo-mark span {
        font-size: 0.78rem;
        font-weight: 800;
        color: #020617;
    }
    .om-logo-text {
        font-size: 0.86rem;
        font-weight: 600;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: #e5e7eb;
    }
    .om-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        background: linear-gradient(120deg, #38bdf8, #a855f7, #f97316);
        -webkit-background-clip: text;
        color: transparent;
    }
    .om-subtitle {
        font-size: 0.9rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.18em;
    }
    .hero-copy {
        margin-top: 0.75rem;
        font-size: 0.92rem;
        color: #cbd5f5;
        max-width: 30rem;
        line-height: 1.6;
    }

    /* Chips de benefícios */
    .hero-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        margin-top: 0.7rem;
    }
    .hero-chip {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        padding: 0.32rem 0.7rem;
        border-radius: 999px;
        border: 1px solid rgba(148,163,253,0.6);
        background: radial-gradient(circle at 0 0, rgba(129,140,248,0.32), rgba(15,23,42,0.9));
        color: #e5e7eb;
    }

    /* Lado direito do hero com “painel holográfico” */
    .hero-panel {
        border-radius: 22px;
        padding: 1.2rem 1.4rem;
        background:
            radial-gradient(circle at 0 0, rgba(59,130,246,0.25), transparent 55%),
            radial-gradient(circle at 120% 0, rgba(236,72,153,0.22), transparent 55%),
            linear-gradient(to bottom right, rgba(15,23,42,0.95), rgba(15,23,42,0.9));
        border: 1px solid rgba(148,163,253,0.5);
        box-shadow: 0 18px 40px rgba(15,23,42,0.9);
    }
    .hero-panel-title {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        color: #9ca3af;
        margin-bottom: 0.6rem;
    }
    .hero-metric-row {
        display: flex;
        gap: 1.2rem;
        margin-bottom: 0.7rem;
    }
    .hero-metric {
        flex: 1;
    }
    .hero-metric-label {
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        color: #6b7280;
        margin-bottom: 0.2rem;
    }
    .hero-metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #e5e7eb;
    }
    .hero-metric-badge {
        font-size: 0.72rem;
        padding: 0.2rem 0.5rem;
        border-radius: 999px;
        border: 1px solid rgba(74,222,128,0.6);
        background: radial-gradient(circle at 0 0, rgba(34,197,94,0.25), transparent 55%);
        color: #bbf7d0;
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        margin-top: 0.25rem;
    }
    .hero-metric-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #4ade80;
        box-shadow: 0 0 10px rgba(74,222,128,0.95);
    }
    .hero-panel-footer {
        margin-top: 0.75rem;
        font-size: 0.78rem;
        color: #94a3b8;
    }

    /* Card principal (config) */
    .om-card {
        background: linear-gradient(145deg, rgba(15,23,42,0.98), rgba(15,23,42,0.92));
        border-radius: 22px;
        padding: 1.6rem 1.8rem 1.5rem 1.8rem;
        border: 1px solid rgba(30,64,175,0.7);
        box-shadow:
            0 0 0 1px rgba(15,23,42,0.95),
            0 22px 58px rgba(0,0,0,0.9);
        margin-bottom: 1.1rem;
    }

    .om-label {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: #9ca3af;
        margin-bottom: 0.25rem;
    }
    .om-help {
        font-size: 0.74rem;
        color: #6b7280;
        margin-top: 0.15rem;
    }

    .om-metric {
        font-size: 2.1rem;
        font-weight: 700;
        color: #e5e7eb;
    }
    .om-metric-label {
        font-size: 0.8rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.18em;
    }

    /* Inputs */
    textarea, .stTextInput>div>div>input, .stNumberInput input {
        background-color: rgba(15,23,42,0.96) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(55,65,81,0.95) !important;
        color: #e5e7eb !important;
        font-size: 0.9rem !important;
    }
    textarea:focus, .stTextInput>div>div>input:focus, .stNumberInput input:focus {
        border-color: rgba(96,165,250,0.95) !important;
        box-shadow: 0 0 0 1px rgba(37,99,235,0.85) !important;
        outline: none !important;
    }

    /* Botão principal */
    .stButton>button {
        border-radius: 999px !important;
        padding: 0.7rem 0 !important;
        font-weight: 600 !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        border: 1px solid rgba(56,189,248,0.9) !important;
        background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
        box-shadow:
            0 0 0 1px rgba(15,23,42,0.95),
            0 18px 40px rgba(37,99,235,0.85) !important;
        color: #f9fafb !important;
    }
    .stButton>button:hover {
        filter: brightness(1.08);
        box-shadow:
            0 0 0 1px rgba(15,23,42,0.95),
            0 22px 48px rgba(59,130,246,0.95) !important;
    }

    /* Botão de download */
    .stDownloadButton>button {
        border-radius: 999px !important;
        border: 1px solid rgba(148,163,253,0.95) !important;
        background: linear-gradient(135deg, rgba(79,70,229,0.96), rgba(59,130,246,0.98)) !important;
        color: #e5e7eb !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        padding: 0.55rem 0 !important;
        box-shadow:
            0 0 0 1px rgba(15,23,42,1),
            0 18px 46px rgba(30,64,175,0.98) !important;
    }
    .stDownloadButton>button:hover {
        filter: brightness(1.06);
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #22c55e, #22d3ee) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------
# HERO
# ----------------------------------------------------------
st.markdown(
    """
    <div class="hero-shell">
        <div class="hero-orbit"></div>
        <div class="hero-content">
            <div class="om-logo-stack">
                <div class="om-logo-pill">
                    <div class="om-logo-mark"><span>OM</span></div>
                    <div class="om-logo-text">MKT · DATA ENGINE</div>
                </div>
                <div class="om-title">Lead Scraper</div>
                <div class="om-subtitle">
                    prospecção inteligente · icp dinâmico · leads em tempo real
                </div>
                <p class="hero-copy">
                    Um painel de prospecção que parece software enterprise — mas roda direto no seu navegador.
                    Desenhe o ICP, clique em iniciar e deixe a OM MKT coletar os próximos leads quentes da sua operação B2B.
                </p>
                <div class="hero-chips">
                    <div class="hero-chip">scraper proprietário</div>
                    <div class="hero-chip">filtro por icp & capital</div>
                    <div class="hero-chip">dados prontos para abordagem</div>
                </div>
            </div>
            <div class="hero-panel">
                <div class="hero-panel-title">Painel de operação</div>
                <div class="hero-metric-row">
                    <div class="hero-metric">
                        <div class="hero-metric-label">batch típico</div>
                        <div class="hero-metric-value">120–300</div>
                        <div class="hero-metric-badge">
                            <span class="hero-metric-dot"></span>
                            leads qualificados por rodada
                        </div>
                    </div>
                    <div class="hero-metric">
                        <div class="hero-metric-label">foco</div>
                        <div class="hero-metric-value">B2B</div>
                        <div class="hero-metric-badge">
                            <span class="hero-metric-dot"></span>
                            decisores & alto tíquete
                        </div>
                    </div>
                </div>
                <div class="hero-panel-footer">
                    Conecte o ICP do cliente, baixe o CSV e pluga direto no CRM, fluxo de SDR ou n8n.
                    O motor de coleta, enriquecimento e filtro roda por baixo da interface.
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------
# CARD CENTRAL – CONFIG + RESULTADO
# ----------------------------------------------------------
_, center_col, _ = st.columns([0.08, 0.84, 0.08])

with center_col:
    # ---------------- CONFIG ----------------
    st.markdown('<div class="om-card">', unsafe_allow_html=True)

    st.markdown('<div class="om-label">Termos de busca</div>', unsafe_allow_html=True)
    termos_raw = st.text_area(
        "",
        value="",
        placeholder="ex: hospital particular\nclínica premium\nsupermercado atacado\n...",
        height=110,
    )
    st.markdown(
        '<div class="om-help">Um termo por linha. Cada termo será combinado com cada cidade.</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown('<div class="om-label">Cidades / mercados</div>', unsafe_allow_html=True)
    cidades_raw = st.text_area(
        "",
        value="",
        placeholder="ex: Belo Horizonte MG\nJuiz de Fora MG\nRio de Janeiro RJ\n...",
        height=110,
    )
    st.markdown(
        '<div class="om-help">Também um por linha, sempre com UF no final.</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    col_capital, col_include, col_exclude = st.columns([0.7, 1.1, 1.1])

    with col_capital:
        st.markdown('<div class="om-label">Capital social mínimo</div>', unsafe_allow_html=True)
        capital_minimo = st.number_input(
            "",
            min_value=0,
            value=0,
            step=50000,
            help="0 = sem filtro por capital. Ajuste para mirar empresas maiores.",
        )

    with col_include:
        st.markdown('<div class="om-label">Palavras obrigatórias</div>', unsafe_allow_html=True)
        include_raw = st.text_input(
            "",
            value="",
            placeholder="ex: hospital, centro médico, laboratório",
            help="Opcional. Separe por vírgulas. Pelo menos uma deve aparecer no texto.",
        )

    with col_exclude:
        st.markdown('<div class="om-label">Palavras para excluir</div>', unsafe_allow_html=True)
        exclude_raw = st.text_input(
            "",
            value="",
            placeholder="ex: farmácia, drogaria, pet shop",
            help="Opcional. Se aparecer, o lead é descartado.",
        )

    st.write("")
    start_button = st.button("⚡ Iniciar prospecção", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)  # fecha card de config

    # ---------------- RESULTADOS ----------------
    st.markdown('<div class="om-card">', unsafe_allow_html=True)

    status_placeholder = st.empty()
    progress_bar = st.progress(0)
    resumo_placeholder = st.empty()
    tabela_placeholder = st.empty()
    download_placeholder = st.empty()

    st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------------------------------------
# LÓGICA DO BOTÃO
# ----------------------------------------------------------
if start_button:
    status_placeholder.empty()
    resumo_placeholder.empty()
    tabela_placeholder.empty()
    download_placeholder.empty()
    progress_bar.progress(0)

    termos = [t.strip() for t in termos_raw.splitlines() if t.strip()]
    cidades = [c.strip() for c in cidades_raw.splitlines() if c.strip()]
    include_keywords = [k.strip() for k in include_raw.split(",") if k.strip()]
    exclude_keywords = [k.strip() for k in exclude_raw.split(",") if k.strip()]

    if not termos:
        status_placeholder.error("Preencha pelo menos um termo de busca.")
    elif not cidades:
        status_placeholder.error("Preencha pelo menos uma cidade/mercado.")
    else:
        config = {
            "termos": termos,
            "cidades": cidades,
            "capital_minimo": capital_minimo,
            "include_keywords": include_keywords,
            "exclude_keywords": exclude_keywords,
        }

        status_placeholder.markdown(
            "<span style='color:#9ca3af; font-size:0.85rem;'>Prospecção em andamento...</span>",
            unsafe_allow_html=True,
        )

        def progress_callback(current, total, percent):
            try:
                progress_bar.progress(percent)
                status_placeholder.markdown(
                    f"<span style='color:#9ca3af; font-size:0.85rem;'>Processando {current}/{total} itens ({percent}%).</span>",
                    unsafe_allow_html=True,
                )
            except Exception:
                pass

        try:
            leads = run_scraper(config, progress_callback=progress_callback)
        except Exception as e:
            status_placeholder.error(f"Erro ao rodar o scraper: {e}")
            leads = []

        if not leads:
            progress_bar.progress(100)
            status_placeholder.markdown(
                "<span style='color:#f97373; font-size:0.85rem;'>Nenhum lead qualificado encontrado com esses filtros.</span>",
                unsafe_allow_html=True,
            )
        else:
            progress_bar.progress(100)
            status_placeholder.markdown(
                "<span style='color:#4ade80; font-size:0.9rem;'>Prospecção concluída com sucesso.</span>",
                unsafe_allow_html=True,
            )

            df = pd.DataFrame(leads)

            resumo_placeholder.markdown(
                f"""
                <div style="margin-top:1rem; margin-bottom:0.75rem;">
                    <span class="om-metric">{len(df)}</span><br/>
                    <span class="om-metric-label">leads qualificados encontrados</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            cols_show = [
                c for c in
                ["nome", "municipio", "email", "telefone", "whatsapp", "lead_score", "url"]
                if c in df.columns
            ]
            tabela_placeholder.dataframe(df[cols_show], use_container_width=True)

            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, sep=";")
            csv_data = csv_buffer.getvalue()

            download_placeholder.download_button(
                label="📥 Baixar leads em CSV",
                data=csv_data,
                file_name="leads_ommkt.csv",
                mime="text/csv",
                use_container_width=True,
            )
