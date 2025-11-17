# app.py
import time
import pandas as pd
import streamlit as st

from scraper_core import run_scraper  # sua função atual de scraping

# =========================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================
st.set_page_config(
    page_title="Scraper Inteligente — ICP CEMIG",
    page_icon="⚡",
    layout="wide",
)

# =========================================
# ESTILO CUSTOMIZADO (DARK FUTURISTA)
# =========================================
CUSTOM_CSS = """
<style>
    /* Fundo geral */
    .stApp {
        background: radial-gradient(circle at top, #141927 0, #05060a 55%, #020205 100%);
        color: #f5f5f5;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Inter", sans-serif;
    }

    /* Títulos principais */
    h1, h2, h3 {
        font-weight: 700 !important;
        letter-spacing: 0.03em;
    }

    /* Cards glass */
    .glass-card {
        background: rgba(15, 18, 30, 0.92);
        border-radius: 18px;
        border: 1px solid rgba(120, 220, 255, 0.08);
        box-shadow:
            0 0 0 1px rgba(255, 255, 255, 0.02),
            0 18px 45px rgba(0,0,0,0.75);
        padding: 22px 22px 18px 22px;
    }

    /* Badge */
    .chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        border-radius: 999px;
        padding: 4px 12px;
        background: linear-gradient(90deg, rgba(76, 201, 240, 0.15), rgba(111, 79, 242, 0.18));
        color: #e1f5ff;
        font-size: 12px;
        border: 1px solid rgba(148, 233, 255, 0.3);
    }

    /* Botão primário */
    .stButton>button {
        border-radius: 999px;
        border: none;
        padding: 0.75rem 1.8rem;
        font-weight: 600;
        font-size: 15px;
        background: linear-gradient(120deg, #4cc9f0, #4361ee);
        color: #020617;
        box-shadow: 0 14px 35px rgba(67, 97, 238, 0.45);
        transition: all 0.15s ease-out;
    }

    .stButton>button:hover {
        transform: translateY(-1px) scale(1.01);
        box-shadow: 0 20px 50px rgba(67, 97, 238, 0.65);
        background: linear-gradient(120deg, #4cc9f0, #4895ef);
        color: #020617;
    }

    .stButton>button:active {
        transform: translateY(0px) scale(0.99);
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.9);
    }

    /* Métricas */
    .metric-card {
        background: rgba(15, 23, 42, 0.9);
        border-radius: 16px;
        padding: 14px 16px;
        border: 1px solid rgba(148, 163, 184, 0.35);
    }
    .metric-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.13em;
        color: #94a3b8;
    }
    .metric-value {
        font-size: 22px;
        font-weight: 600;
    }
    .metric-sub {
        font-size: 12px;
        color: #64748b;
    }

    /* Text areas */
    textarea {
        background: rgba(15, 23, 42, 0.9) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(51, 65, 85, 0.9) !important;
        font-size: 13px !important;
    }

    /* Inputs */
    .stTextInput>div>div>input {
        background: rgba(15, 23, 42, 0.98);
        border-radius: 999px;
        border: 1px solid rgba(51, 65, 85, 0.9);
        font-size: 13px;
    }

    /* Slider label */
    .slider-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.13em;
        color: #9ca3af;
        margin-bottom: 4px;
    }

    /* Tabela */
    .dataframe td, .dataframe th {
        border-color: rgba(31, 41, 55, 0.9) !important;
        color: #e5e7eb !important;
        font-size: 12px !important;
    }

</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================
col_logo, col_title, col_tag = st.columns([0.8, 3, 1.4])

with col_logo:
    st.markdown("### ⚡")

with col_title:
    st.markdown(
        "<h1>Scraper Inteligente — ICP CEMIG</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='chip'>Encontre leads qualificados • Exportação em CSV • Sem depender de Google Sheets</div>",
        unsafe_allow_html=True,
    )

with col_tag:
    st.markdown(
        "<div style='text-align: right; font-size:12px; color:#9ca3af;'>Powered by <b>Pinn Growth</b></div>",
        unsafe_allow_html=True,
    )

st.markdown("")

# =========================================
# LAYOUT PRINCIPAL (CONFIG + CAMPOS DE BUSCA)
# =========================================
col_left, col_right = st.columns([1.1, 0.9])

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
    st.markdown("<div class='slider-label'>Consumo mínimo por unidade (R$)</div>", unsafe_allow_html=True)
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

    st.markdown("---")

    # Motivações esperadas
    st.caption("Motivações esperadas (palavras-chave para qualificação)")
    motivacoes_default = ["redução de custo", "economia de energia"]
    motivacoes_text = st.text_input(
        "Motivações separadas por vírgula",
        value=", ".join(motivacoes_default),
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

    st.markdown("---")

    executar = st.button("🚀 Rodar Scraper", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================
# EXECUÇÃO DO SCRAPER
# =========================================
df_resultado = None
stats = {}

if executar:
    with st.spinner("Rodando scraper e qualificando leads..."):
        # Monta o dicionário de configuração que será enviado ao scraper_core
        config = {
            "tipo_cliente": "PJ" if "Jurídica" in tipo_cliente else "PF",
            "apenas_cemig": apenas_cemig,
            "min_consumo": min_consumo,
            "motivacoes": motivacoes,
            "termos_busca": termos_busca,
            "cidades": cidades,
        }

        # Chama sua função de scraping
        leads = run_scraper(config=config)

        # Converte retorno para DataFrame, independente se veio lista ou df
        if isinstance(leads, pd.DataFrame):
            df_resultado = leads.copy()
        else:
            df_resultado = pd.DataFrame(leads)

        # Ajusta colunas vazias
        if not df_resultado.empty:
            df_resultado.columns = [str(c) for c in df_resultado.columns]

        # Exemplo de métricas básicas para o dashboard
        if not df_resultado.empty:
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

            # Se tiver coluna de capital/consumo
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
st.markdown("## 📊 Dashboard de Leads")

if df_resultado is None or df_resultado.empty:
    st.info("Rode o scraper para visualizar o dashboard com os leads qualificados.")
else:
    # ----- KPIs em cartões -----
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

    with col_kpi1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Leads qualificados</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='metric-value'>{stats.get('total_leads', 0)}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='metric-sub'>Com base nos filtros atuais</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_kpi2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Cidades</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='metric-value'>{stats.get('qtd_cidades', len(cidades))}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='metric-sub'>Área de atuação analisada</div>", unsafe_allow_html=True)
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

    # ----- GRÁFICO POR CIDADE (se tiver) -----
    col_chart, col_side = st.columns([1.8, 1])

    with col_chart:
        # tenta achar coluna de cidade
        col_municipio = None
        for c in df_resultado.columns:
            if c.lower() in ("municipio", "cidade", "cidade_uf", "cidade_estado"):
                col_municipio = c
                break

        if col_municipio:
            st.markdown("#### Distribuição de Leads por Cidade")
            top_cidades = (
                df_resultado[col_municipio]
                .value_counts()
                .reset_index()
                .rename(columns={"index": "Cidade", col_municipio: "Leads"})
            )
            st.bar_chart(
                data=top_cidades,
                x="Cidade",
                y="Leads",
            )
        else:
            st.markdown("#### Distribuição de Leads por Cidade")
            st.caption("Nenhuma coluna de cidade identificada automaticamente no retorno do scraper.")

    with col_side:
        st.markdown("#### Exportar / Filtros Rápidos")
        # Filtro simples por cidade, se existir
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

        # Botão download CSV
        csv_bytes = df_filtrado.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="⬇️ Baixar CSV dos leads",
            data=csv_bytes,
            file_name="leads_icp_cemig.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.caption(
            "O CSV inclui todas as colunas retornadas pelo scraper. "
            "Você pode importar em qualquer CRM ou planilha."
        )

    st.markdown("---")

    # ----- TABELA DETALHADA -----
    st.markdown("#### 📄 Leads detalhados")
    st.dataframe(
        df_filtrado,
        use_container_width=True,
        height=420,
    )
