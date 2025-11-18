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
# ESTILO FUTURISTA / PRODUTO CARO
# ----------------------------------------------------------
st.markdown(
    """
    <style>
    /* Fundo geral */
    body {
        background: radial-gradient(circle at 10% 0%, #141629 0, #050612 55%, #020308 100%);
        color: #f9fafb;
        font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .main {
        background: transparent;
    }
    /* Centralizar conteúdo principal */
    .block-container {
        max-width: 1100px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    /* Header / Logo */
    .om-header {
        text-align: center;
        margin-bottom: 2.2rem;
    }
    .om-logo-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.45rem 0.9rem;
        border-radius: 999px;
        border: 1px solid rgba(96, 165, 250, 0.45);
        background: radial-gradient(circle at 0% 0%, rgba(59, 130, 246, 0.75), rgba(15, 23, 42, 0.45));
        box-shadow:
            0 0 0 1px rgba(15, 23, 42, 0.9),
            0 0 22px rgba(59, 130, 246, 0.55);
        margin-bottom: 1rem;
    }
    .om-logo-mark {
        width: 26px;
        height: 26px;
        border-radius: 11px;
        background: conic-gradient(from 210deg, #22d3ee, #4f46e5, #ec4899, #22d3ee);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 18px rgba(59, 130, 246, 0.7);
    }
    .om-logo-mark span {
        font-size: 0.9rem;
        font-weight: 800;
        color: #020617;
    }
    .om-logo-text {
        font-size: 0.9rem;
        font-weight: 600;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #e5e7eb;
    }
    .om-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        background: linear-gradient(120deg, #38bdf8, #a855f7, #f97316);
        -webkit-background-clip: text;
        color: transparent;
        margin-bottom: 0.4rem;
    }
    .om-subtitle {
        font-size: 0.95rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.18em;
    }

    /* Card principal (form) */
    .om-card {
        background: radial-gradient(circle at 0 0, rgba(148, 163, 253, 0.12), rgba(15, 23, 42, 0.96));
        border-radius: 24px;
        padding: 1.8rem 2rem 1.6rem 2rem;
        border: 1px solid rgba(148, 163, 253, 0.35);
        box-shadow:
            0 0 0 1px rgba(15, 23, 42, 0.9),
            0 26px 60px rgba(0, 0, 0, 0.85);
    }

    /* Card de resultados */
    .om-card-secondary {
        background: radial-gradient(circle at 100% 0, rgba(96, 165, 250, 0.12), rgba(15, 23, 42, 0.98));
        border-radius: 22px;
        padding: 1.4rem 1.6rem 1.4rem 1.6rem;
        border: 1px solid rgba(55, 65, 81, 0.9);
        box-shadow:
            0 0 0 1px rgba(15, 23, 42, 0.85),
            0 18px 42px rgba(0, 0, 0, 0.75);
    }

    .om-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.35rem 0.9rem;
        border-radius: 999px;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        background: radial-gradient(circle at 0 0, rgba(52, 211, 153, 0.2), rgba(30, 64, 175, 0.8));
        color: #d1fae5;
        border: 1px solid rgba(52, 211, 153, 0.6);
    }
    .om-pill-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #4ade80;
        box-shadow: 0 0 10px rgba(74, 222, 128, 0.95);
    }

    .om-card-title {
        margin-top: 1rem;
        font-size: 1.25rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .om-card-text {
        font-size: 0.9rem;
        color: #9ca3af;
        margin-top: 0.4rem;
        line-height: 1.5;
    }

    .om-label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: #9ca3af;
        margin-bottom: 0.25rem;
    }
    .om-help {
        font-size: 0.75rem;
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

    /* Botão principal */
    .stButton>button {
        border-radius: 999px !important;
        padding: 0.65rem 0 !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        border: 1px solid rgba(56, 189, 248, 0.8) !important;
        background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
        box-shadow:
            0 0 0 1px rgba(15, 23, 42, 0.9),
            0 14px 30px rgba(37, 99, 235, 0.65) !important;
        color: #f9fafb !important;
    }
    .stButton>button:hover {
        filter: brightness(1.08);
        box-shadow:
            0 0 0 1px rgba(15, 23, 42, 0.9),
            0 18px 36px rgba(59, 130, 246, 0.85) !important;
    }

    /* Download button */
    .stDownloadButton>button {
        border-radius: 999px !important;
        border: 1px solid rgba(148, 163, 253, 0.85) !important;
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.92), rgba(59, 130, 246, 0.95)) !important;
        color: #e5e7eb !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        padding: 0.55rem 0 !important;
        box-shadow:
            0 0 0 1px rgba(17, 24, 39, 0.9),
            0 16px 34px rgba(30, 64, 175, 0.85) !important;
    }
    .stDownloadButton>button:hover {
        filter: brightness(1.06);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------
# HEADER / LOGO
# ----------------------------------------------------------
st.markdown(
    """
    <div class="om-header">
        <div class="om-logo-pill">
            <div class="om-logo-mark"><span>OM</span></div>
            <div class="om-logo-text">MKT · DATA ENGINE</div>
        </div>
        <div class="om-title">Lead Scraper</div>
        <div class="om-subtitle">prospecção inteligente • dados em escala • operação plug & play</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------
# CARD CENTRAL (FORM)
# ----------------------------------------------------------
spacer_left, center_col, spacer_right = st.columns([0.1, 0.8, 0.1])

with center_col:
    st.markdown('<div class="om-card">', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="om-badge">
            <span class="om-pill-dot"></span>
            configuração de icp & mercado alvo
        </div>
        <div class="om-card-title">Desenhe o alvo, o motor faz o resto</div>
        <p class="om-card-text">
            Defina como você quer atacar o mercado: segmentos, cidades e filtros.
            O OM MKT Scraper transforma isso em uma operação de prospecção ativa com cara de produto enterprise.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    # Termos
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

    # Cidades
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

    # Linha de filtros
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

    st.markdown("</div>", unsafe_allow_html=True)  # fecha om-card

st.write("")  # espaçamento

# ----------------------------------------------------------
# CARD DE RESULTADOS / STATUS
# ----------------------------------------------------------
st.markdown('<div class="om-card-secondary">', unsafe_allow_html=True)

status_placeholder = st.empty()
progress_bar = st.progress(0)
resumo_placeholder = st.empty()
tabela_placeholder = st.empty()
download_placeholder = st.empty()

st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------
# LÓGICA AO CLICAR NO BOTÃO
# ----------------------------------------------------------
if start_button:
    # Limpa saída antiga
    status_placeholder.empty()
    resumo_placeholder.empty()
    tabela_placeholder.empty()
    download_placeholder.empty()
    progress_bar.progress(0)

    # Normaliza entradas
    termos = [t.strip() for t in termos_raw.splitlines() if t.strip()]
    cidades = [c.strip() for c in cidades_raw.splitlines() if c.strip()]
    include_keywords = [k.strip() for k in include_raw.split(",") if k.strip()]
    exclude_keywords = [k.strip() for k in exclude_raw.split(",") if k.strip()]

    # Validação
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

        # Callback de progresso
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

            # Tabela resumida
            cols_show = [c for c in ["nome", "municipio", "email", "telefone", "whatsapp", "lead_score", "url"] if c in df.columns]
            tabela_placeholder.dataframe(df[cols_show], use_container_width=True)

            # CSV para download
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
