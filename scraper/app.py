import streamlit as st
import pandas as pd

from scraper_core import run_scraper


# ==========================================================
# ⚙️ CONFIG DA PÁGINA
# ==========================================================
st.set_page_config(
    page_title="OM MKT · Scraper de Leads",
    page_icon="📊",
    layout="wide",
)

# ==========================================================
# 🎨 CSS – PEGADA FUTURISTA / TECH
# ==========================================================
st.markdown(
    """
<style>
.stApp {
    background: radial-gradient(circle at top left, #1d4ed8 0, #020617 40%, #020617 100%);
    color: #e5e7eb;
}

.block-container {
    max-width: 1100px;
    padding-top: 2.3rem;
    padding-bottom: 3rem;
}

.hero-logo {
    text-align: center;
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
}
.hero-logo span.om {
    background: linear-gradient(120deg, #22c55e, #38bdf8);
    -webkit-background-clip: text;
    color: transparent;
    text-shadow: 0 0 18px rgba(56, 189, 248, 0.7);
}
.hero-logo span.mkt {
    background: linear-gradient(120deg, #f97316, #ef4444);
    -webkit-background-clip: text;
    color: transparent;
    text-shadow: 0 0 18px rgba(239, 68, 68, 0.7);
}

.hero-subtitle {
    text-align: center;
    font-size: 0.98rem;
    color: #9ca3af;
    margin-bottom: 0.8rem;
}

.hero-chips {
    display: flex;
    justify-content: center;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-bottom: 1.6rem;
}
.hero-chip {
    font-size: 0.8rem;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(148, 163, 184, 0.4);
}

.form-card {
    background: linear-gradient(135deg, rgba(15,23,42,0.85), rgba(15,23,42,0.95));
    border-radius: 20px;
    padding: 1.6rem 1.8rem 1.4rem 1.8rem;
    border: 1px solid rgba(148,163,184,0.35);
    box-shadow:
        0 25px 60px rgba(15, 23, 42, 0.9),
        0 0 0 1px rgba(15, 23, 42, 0.7);
    backdrop-filter: blur(18px);
}

.form-title {
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 0.4rem;
}
.form-caption {
    font-size: 0.8rem;
    color: #9ca3af;
    margin-bottom: 1.1rem;
}

.stTextInput > div > div > input,
.stTextArea textarea,
.stNumberInput input {
    background: rgba(15,23,42,0.9) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(148,163,184,0.45) !important;
    color: #e5e7eb !important;
}

.stTextInput > div > div > input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 1px rgba(56,189,248,0.55) !important;
}

.css-1kyxreq, .css-1p3ggoo, label, .stMarkdown p {
    color: #e5e7eb;
}

.stCheckbox > label {
    color: #e5e7eb !important;
    font-size: 0.85rem;
}

.stButton > button {
    background: linear-gradient(120deg, #22c55e, #38bdf8, #f97316);
    background-size: 200% 200%;
    color: #0b1120;
    border-radius: 999px;
    border: none;
    padding: 0.8rem 1.9rem;
    font-weight: 700;
    font-size: 0.98rem;
    box-shadow:
        0 15px 40px rgba(56, 189, 248, 0.45),
        0 0 18px rgba(34, 197, 94, 0.7);
    cursor: pointer;
    transition: transform 0.1s ease-out, box-shadow 0.1s ease-out, opacity 0.1s, background-position 2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow:
        0 22px 50px rgba(56, 189, 248, 0.6),
        0 0 22px rgba(34, 197, 94, 0.8);
    background-position: 100% 0;
}

.stButton > button:active {
    transform: translateY(0px);
}

.stProgress > div > div {
    background: linear-gradient(90deg, #22c55e, #38bdf8, #f97316) !important;
}

.status-text {
    color: #f97316;
    font-weight: 500;
    font-size: 0.9rem;
}

.result-card {
    background: rgba(15,23,42,0.9);
    border-radius: 18px;
    padding: 1.2rem 1.4rem;
    border: 1px solid rgba(148,163,184,0.35);
    box-shadow: 0 20px 50px rgba(15,23,42,0.85);
}

.stDownloadButton > button {
    border-radius: 999px;
    background: linear-gradient(120deg, #0ea5e9, #22c55e) !important;
    color: #0b1120 !important;
    border: none;
}

.center-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# 🧩 HELPERS
# ==========================================================
def parse_multiline(text: str):
    return [
        x.strip()
        for x in text.replace("\r", "\n").split("\n")
        if x.strip()
    ]


# ==========================================================
# 🧱 LAYOUT – HERO + FORM FUTURISTA
# ==========================================================
st.markdown('<div class="center-wrapper">', unsafe_allow_html=True)

st.markdown(
    """
<div class="hero-logo">
  <span class="om">OM</span><span class="mkt"> MKT</span>
</div>
<p class="hero-subtitle">
  Scraper de Leads com inteligência de ICP para acelerar sua prospecção B2B.
</p>
<div class="hero-chips">
  <span class="hero-chip">⚡ Prospecção automática</span>
  <span class="hero-chip">🎯 ICP dinâmico</span>
  <span class="hero-chip">📊 Leads prontos para abordagem</span>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)

col_esq, col_card, col_dir = st.columns([1, 4, 1])

with col_card:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    st.markdown('<div class="form-title">Configuração do ICP</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="form-caption">Defina o perfil ideal, clique em iniciar e deixe o motor da OM MKT trabalhar por você.</div>',
        unsafe_allow_html=True,
    )

    capital_min = st.number_input(
        "Capital social mínimo (R$)",
        value=0,
        step=50000,
        min_value=0,
        key="capital",
        help="Se não quiser filtrar por capital mínimo, deixe 0.",
    )

    termos_txt = st.text_area(
        "Termos de busca (um por linha)",
        value="",
        height=90,
        key="termos",
        placeholder="ex.: hospital particular\nclínica hospitalar\ncentro médico",
    )

    cidades_txt = st.text_area(
        "Cidades (uma por linha – ex.: Belo Horizonte MG)",
        value="",
        height=90,
        key="cidades",
        placeholder="ex.: Belo Horizonte MG\nContagem MG\nJuiz de Fora MG",
    )

    col_inc, col_exc = st.columns(2)
    with col_inc:
        include_txt = st.text_area(
            "Palavras que indicam bom lead",
            value="",
            height=80,
            key="include",
            placeholder="ex.: hospital\nclínica\ncentro médico",
            help="Se preencher, pelo menos uma dessas palavras precisa aparecer no texto da empresa.",
        )
    with col_exc:
        exclude_txt = st.text_area(
            "Palavras que excluem lead",
            value="",
            height=80,
            key="exclude",
            placeholder="ex.: farmácia\npet shop\nposto de saúde",
            help="Se aparecer, a empresa é descartada.",
        )

    enviar_sheets = st.checkbox(
        "Enviar resultados para Google Sheets",
        value=True,
        key="sheets",
    )

    start = st.button("🚀 Iniciar prospecção", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================================
# ▶️ EXECUÇÃO DO SCRAPER
# ==========================================================
if start:
    termos = parse_multiline(termos_txt)
    cidades = parse_multiline(cidades_txt)
    include_keywords = parse_multiline(include_txt)
    exclude_keywords = parse_multiline(exclude_txt)

    if not termos:
        st.error("Adicione ao menos **um termo de busca**.")
        st.stop()
    if not cidades:
        st.error("Adicione ao menos **uma cidade**.")
        st.stop()

    with col_card:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🔄 Progresso da prospecção")
        progress_bar = st.progress(0)
        status_placeholder = st.empty()

    def progress_callback(current, total, pct):
        with col_card:
            progress_bar.progress(pct)
            status_placeholder.markdown(
                f"<p class='status-text'>Processando empresas: {current}/{total} ({pct}%)</p>",
                unsafe_allow_html=True,
            )

    config = {
        "termos": termos,
        "cidades": cidades,
        "capital_minimo": int(capital_min),
        "include_keywords": include_keywords,
        "exclude_keywords": exclude_keywords,
        "enviar_sheets": enviar_sheets,
    }

    leads = run_scraper(config, progress_callback=progress_callback)

    with col_card:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown("### ✅ Resultado da prospecção")
        st.write(f"Foram encontrados **{len(leads)}** leads quentes com o filtro atual.")

        if leads:
            df = pd.DataFrame(leads)

            cols_basicas = [
                "nome", "municipio", "capital", "porte",
                "email", "telefone", "whatsapp", "lead_score"
            ]
            cols_existentes = [c for c in cols_basicas if c in df.columns]

            st.markdown("#### 📋 Leads encontrados (visão resumida)")
            st.dataframe(df[cols_existentes], use_container_width=True)

            # 🔽 Download do arquivo gerado (CSV)
            csv_bytes = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Baixar arquivo de leads (CSV)",
                data=csv_bytes,
                file_name="leads_quentes.csv",
                mime="text/csv",
            )

        else:
            st.info("Nenhum lead aprovado com o score mínimo atual.")

        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Defina o ICP no card central e clique em **🚀 Iniciar prospecção** para ver o motor da OM MKT em ação.")
