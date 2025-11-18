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
    body {
        background: radial-gradient(circle at top left, #101020, #02030a 60%);
        color: #f5f5f5;
        font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .main {
        background: transparent;
    }
    .om-header {
        text-align: center;
        padding: 2rem 0 0.5rem 0;
    }
    .om-title {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        background: linear-gradient(120deg, #32e7ff, #9b68ff, #ff4b8a);
        -webkit-background-clip: text;
        color: transparent;
        margin-bottom: 0.2rem;
    }
    .om-subtitle {
        font-size: 0.95rem;
        color: #b5bfd9;
        text-transform: uppercase;
        letter-spacing: 0.16em;
    }
    .om-card {
        background: rgba(8, 12, 32, 0.92);
        border-radius: 20px;
        padding: 1.5rem 1.75rem;
        border: 1px solid rgba(99, 179, 237, 0.25);
        box-shadow:
            0 0 0 1px rgba(10, 132, 255, 0.08),
            0 22px 45px rgba(0, 0, 0, 0.55);
    }
    .om-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.3rem 0.75rem;
        border-radius: 999px;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        background: linear-gradient(120deg, rgba(50,231,255,0.16), rgba(155,104,255,0.08));
        color: #c7d2fe;
        border: 1px solid rgba(129, 140, 248, 0.5);
    }
    .om-pill-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #34d399;
        box-shadow: 0 0 10px rgba(52, 211, 153, 0.9);
    }
    .om-label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #9ca3af;
        margin-bottom: 0.25rem;
    }
    .om-help {
        font-size: 0.75rem;
        color: #6b7280;
        margin-top: 0.15rem;
    }
    .om-metric {
        font-size: 2rem;
        font-weight: 700;
        color: #e5e7eb;
    }
    .om-metric-label {
        font-size: 0.8rem;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.14em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------
# HEADER
# ----------------------------------------------------------
st.markdown(
    """
    <div class="om-header">
        <div class="om-title">OM MKT SCRAPER</div>
        <div class="om-subtitle">prospecção inteligente • dados em escala • operação pronta pra rodar</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")  # espaçamento pequeno

# ----------------------------------------------------------
# LAYOUT PRINCIPAL
# ----------------------------------------------------------
col_left, col_right = st.columns([1.1, 1.3])

with col_left:
    st.markdown(
        """
        <div class="om-card">
            <div class="om-badge">
                <span class="om-pill-dot"></span>
                engine de prospecção ativa
            </div>
            <h2 style="margin-top: 1rem; font-size: 1.3rem; font-weight: 700;">
                Defina o alvo da sua operação
            </h2>
            <p style="font-size: 0.9rem; color: #9ca3af; margin-bottom: 1.2rem;">
                Configure o ICP, escolha os segmentos e mercados que deseja atacar e deixe o motor da OM MKT
                varrer a web em busca dos melhores leads para o seu time.
            </p>
        """
        ,
        unsafe_allow_html=True,
    )

    # Campos de termos
    st.markdown('<div class="om-label">Termos de busca</div>', unsafe_allow_html=True)
    termos_raw = st.text_area(
        "",
        value="",
        placeholder="ex: hospital particular\nclínica premium\nsupermercado atacado\n...",
        height=120,
    )
    st.markdown(
        '<div class="om-help">Um termo por linha. O scraper combina cada termo com cada cidade.</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    # Cidades
    st.markdown('<div class="om-label">Cidades / Mercados</div>', unsafe_allow_html=True)
    cidades_raw = st.text_area(
        "",
        value="",
        placeholder="ex: Belo Horizonte MG\nJuiz de Fora MG\nRio de Janeiro RJ\n...",
        height=120,
    )
    st.markdown(
        '<div class="om-help">Também um por linha, sempre com UF no final.</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    # Capital mínimo
    st.markdown('<div class="om-label">Capital social mínimo (opcional)</div>', unsafe_allow_html=True)
    capital_minimo = st.number_input(
        "",
        min_value=0,
        value=0,
        step=10000,
        help="0 = sem filtro por capital social. Se quiser filtrar empresas maiores, ajuste aqui.",
    )

    st.write("")

    # Palavras de inclusão
    st.markdown('<div class="om-label">Palavras que DEVEM aparecer (opcional)</div>', unsafe_allow_html=True)
    include_raw = st.text_input(
        "",
        value="",
        placeholder="ex: hospital, centro médico, supermercado",
        help="Opcional. Separe por vírgulas. Pelo menos uma dessas palavras deve aparecer no texto.",
    )

    # Palavras de exclusão
    st.markdown('<div class="om-label" style="margin-top: 0.75rem;">Palavras para EXCLUIR (opcional)</div>',
                unsafe_allow_html=True)
    exclude_raw = st.text_input(
        "",
        value="",
        placeholder="ex: farmácia, drogaria, pet shop",
        help="Opcional. Se alguma dessas palavras aparecer, o lead é descartado.",
    )

    st.write("")

    # Botão de ação
    start_button = st.button("⚡ Iniciar prospecção", use_container_width=True, type="primary")

    st.markdown("</div>", unsafe_allow_html=True)  # fecha om-card

with col_right:
    st.markdown(
        """
        <div class="om-card">
            <div class="om-label">status da sessão</div>
        """,
        unsafe_allow_html=True,
    )

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

    # Validação básica
    if not termos:
        st.error("Preencha pelo menos um termo de busca.")
    elif not cidades:
        st.error("Preencha pelo menos uma cidade/mercado.")
    else:
        # Monta config para o core
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

        # Callback para atualizar barra de progresso
        def progress_callback(current, total, percent):
            try:
                progress_bar.progress(percent)
                status_placeholder.markdown(
                    f"<span style='color:#9ca3af; font-size:0.85rem;'>Processando {current}/{total} itens "
                    f"({percent}%).</span>",
                    unsafe_allow_html=True,
                )
            except Exception:
                # Streamlit às vezes reclama se a sessão for resetada; ignoramos aqui
                pass

        try:
            leads = run_scraper(config, progress_callback=progress_callback)
        except Exception as e:
            st.error(f"Erro ao rodar o scraper: {e}")
            leads = []

        if not leads:
            progress_bar.progress(100)
            status_placeholder.markdown(
                "<span style='color:#f97373; font-size:0.85rem;'>Nenhum lead qualificado encontrado "
                "com esses filtros.</span>",
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

            tabela_placeholder.dataframe(
                df[["nome", "municipio", "email", "telefone", "whatsapp", "lead_score", "url"]],
                use_container_width=True,
            )

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
