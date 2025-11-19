import io
import time
import streamlit as st
import pandas as pd

# ----------------------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA
# ----------------------------------------------------------
st.set_page_config(
    page_title="OM MKT · Data Engine",
    layout="wide",
    page_icon="💠",
    initial_sidebar_state="collapsed"
)

# ----------------------------------------------------------
# 2. ESTILO PREMIUM (CSS)
# ----------------------------------------------------------
st.markdown(
    """
    <style>
    /* Importando fontes Premium */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --primary-glow: #00f3ff;   /* Ciano Neon */
        --secondary-glow: #7000ff; /* Roxo Profundo */
        --bg-dark: #050505;        /* Quase Preto */
        --card-bg: #0e1116;        /* Cinza Chumbo */
        --border-color: #1f2937;   /* Borda sutil */
    }

    /* Reset Geral */
    .stApp {
        background-color: var(--bg-dark);
        background-image: 
            radial-gradient(at 50% 0%, rgba(0, 243, 255, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(112, 0, 255, 0.1) 0px, transparent 50%);
        background-attachment: fixed;
        color: #e0e0e0;
    }

    /* Ocultar elementos nativos do Streamlit que poluem a tela */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 900px; /* Limita a largura para ficar mais elegante */
    }

    /* --- CONTAINER PRINCIPAL (O CHASSI) --- */
    .main-frame {
        background: rgba(14, 17, 22, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 0;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
        overflow: hidden;
        margin-bottom: 2rem;
    }

    /* --- HEADER DO CONTAINER --- */
    .frame-header {
        background: linear-gradient(180deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0) 100%);
        padding: 2.5rem 3rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }

    .brand-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 2rem;
        letter-spacing: -0.02em;
        color: #fff;
        margin: 0;
        background: linear-gradient(90deg, #fff, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .brand-tagline {
        font-family: 'Inter', sans-serif;
        color: #94a3b8;
        font-size: 0.95rem;
        margin-top: 0.5rem;
        max-width: 400px;
        line-height: 1.5;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        background: rgba(0, 243, 255, 0.1);
        border: 1px solid rgba(0, 243, 255, 0.2);
        border-radius: 999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: var(--primary-glow);
        box-shadow: 0 0 10px rgba(0, 243, 255, 0.1);
    }
    
    .status-dot {
        width: 6px;
        height: 6px;
        background-color: var(--primary-glow);
        border-radius: 50%;
        margin-right: 8px;
        box-shadow: 0 0 8px var(--primary-glow);
    }

    /* --- CORPO DO FORMULÁRIO --- */
    .form-body {
        padding: 3rem;
    }

    /* Labels Estilizados */
    .stTextArea label, .stTextInput label, .stNumberInput label {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        color: #94a3b8 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 0.5rem !important;
    }

    /* Inputs Estilizados */
    .stTextArea textarea, .stTextInput input, .stNumberInput input {
        background-color: #0a0c10 !important; /* Fundo bem escuro */
        border: 1px solid #2d3748 !important;
        border-radius: 8px !important;
        color: #f8fafc !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.9rem !important;
        padding: 1rem !important;
        transition: all 0.2s ease;
    }

    /* Efeito de Foco nos Inputs (Onde acontece a mágica) */
    .stTextArea textarea:focus, .stTextInput input:focus, .stNumberInput input:focus {
        border-color: var(--primary-glow) !important;
        box-shadow: 0 0 0 4px rgba(0, 243, 255, 0.1) !important;
        background-color: #0f1218 !important;
    }

    /* Placeholder Text */
    ::placeholder {
        color: #475569 !important;
        opacity: 1;
    }
    
    /* Remove a borda vermelha de erro padrão do Streamlit se houver */
    .stTextArea div[data-baseweb="textarea"], .stTextInput div[data-baseweb="input"] {
        border: none !important;
    }

    /* --- BOTÃO "INICIAR" --- */
    div[data-testid="stButton"] > button {
        width: 100%;
        background: linear-gradient(92.88deg, #455EB5 9.16%, #5643CC 43.89%, #673FD7 64.72%) !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.85rem 1.5rem !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 4px 14px 0 rgba(110, 88, 255, 0.39) !important;
        transition: all 0.2s ease-in-out !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-top: 1rem;
    }

    div[data-testid="stButton"] > button:hover {
        box-shadow: 0 6px 20px rgba(110, 88, 255, 0.23) !important;
        transform: scale(1.01) !important;
        filter: brightness(1.1);
    }

    div[data-testid="stButton"] > button:active {
        transform: scale(0.98) !important;
    }

    /* Ajuste fino para alinhamento das colunas de inputs pequenos */
    div[data-testid="column"] {
        padding: 0 5px;
    }
    
    /* Help text (tooltips) styling adjustments */
    .stTooltipIcon {
        color: #64748b !important;
    }
    
    /* Metrics Result Card styling */
    .result-metric-card {
        background: rgba(0, 243, 255, 0.05);
        border: 1px solid rgba(0, 243, 255, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------
# 3. INTERFACE (HTML WIDGETS + STREAMLIT INPUTS)
# ----------------------------------------------------------

# Início do Container Visual (HTML puro para o "Frame")
st.markdown("""
<div class="main-frame">
    <div class="frame-header">
        <div>
            <h1 class="brand-title">OM MKT · Data Engine</h1>
            <p class="brand-tagline">
                Inteligência comercial proprietária. Configure os vetores de busca para iniciar a extração em tempo real.
            </p>
        </div>
        <div style="text-align: right;">
            <div class="status-pill">
                <span class="status-dot"></span> SYSTEM ONLINE
            </div>
            <div style="margin-top:8px; font-family:'JetBrains Mono'; font-size:0.7rem; color:#64748b; text-transform:uppercase;">
                v.2.2.0 Stable
            </div>
        </div>
    </div>
    <div class="form-body">
""", unsafe_allow_html=True)

# --- INPUTS (Agora dentro do "form-body") ---

# Termos de Busca
termos_raw = st.text_area(
    "Termos de Busca (Target)",
    placeholder="Ex: Indústria Metalúrgica\nClínica de Estética\nEmpresa de Logística",
    height=140,
    help="Um termo por linha. O sistema fará a varredura combinada."
)

# Cidades
cidades_raw = st.text_area(
    "Cidades / Mercados (Geo)",
    placeholder="Ex: São Paulo SP\nCampinas SP\nBelo Horizonte MG",
    height=140,
    help="Cidade e UF obrigatórios."
)

# 🔹 NOVO: Consultas livres (cada linha é uma busca feita exatamente como está)
consultas_raw = st.text_area(
    "Consultas Livres (Opcional)",
    placeholder="Ex:\nclínica de estética São Paulo telefone\nhospital particular Belo Horizonte contato",
    height=120,
    help="Use quando quiser escrever a busca exatamente como será enviada. Uma consulta por linha."
)

st.write("")  # Espaçamento sutil

# Filtros Avançados (3 Colunas)
c1, c2, c3 = st.columns(3)

with c1:
    capital_minimo = st.number_input(
        "Capital Social Mín (R$)",
        min_value=0,
        value=0,
        step=10000,
        help="Filtra empresas pequenas."
    )

with c2:
    include_raw = st.text_input(
        "Termos Obrigatórios",
        placeholder="Ex: Ltda, S.A.",
        help="Se preenchido, o lead DEVE conter isso."
    )

with c3:
    exclude_raw = st.text_input(
        "Termos Excluídos",
        placeholder="Ex: MEI, Drogaria",
        help="Remove leads indesejados."
    )

# 🔹 NOVO: Segunda linha de filtros avançados
c4, c5, c6 = st.columns(3)

with c4:
    resultados_por_consulta = st.number_input(
        "Resultados por Consulta",
        min_value=5,
        max_value=100,
        value=25,
        step=5,
        help="Quantos resultados o motor deve puxar por consulta de busca."
    )

with c5:
    score_minimo = st.number_input(
        "Score Mínimo do Lead",
        min_value=0,
        max_value=20,
        value=0,
        step=1,
        help="Corte mínimo do lead_score. 0 = sem corte por score."
    )

with c6:
    filtrar_me_epp = st.checkbox(
        "Excluir ME / EPP",
        value=False,
        help="Quando marcado, remove micro e pequenas empresas (ME / EPP) da base."
    )

# 🔹 NOVO: Controle enviar para Sheets
enviar_sheets = st.checkbox(
    "Enviar automaticamente para Google Sheets",
    value=False,
    help="Quando integrado ao backend, ativa o envio automático dos leads para a planilha."
)

st.write("") # Espaçamento antes do botão
st.write("")

# Botão de Ação
start_button = st.button("⚡ Iniciar Varredura e Extração")

# Fechamento das tags HTML do Container
st.markdown("</div></div>", unsafe_allow_html=True)


# ----------------------------------------------------------
# 4. LÓGICA E RESULTADOS (Simulado)
# ----------------------------------------------------------

if start_button:
    # Validação simples (mantida)
    if not termos_raw or not cidades_raw:
        st.error("⚠️ Erro de Input: Defina pelo menos um Termo e uma Cidade.")
    else:
        # 🔹 Aqui você já tem todas as variáveis prontas para montar o config do scraper:
        # termos = [t.strip() for t in termos_raw.splitlines() if t.strip()]
        # cidades = [c.strip() for c in cidades_raw.splitlines() if c.strip()]
        # consultas = [q.strip() for q in consultas_raw.splitlines() if q.strip()]
        # include_keywords = [w.strip() for w in include_raw.split(",") if w.strip()]
        # exclude_keywords = [w.strip() for w in exclude_raw.split(",") if w.strip()]
        #
        # config = {
        #     "termos": termos,
        #     "cidades": cidades,
        #     "consultas": consultas,
        #     "resultados_por_consulta": int(resultados_por_consulta),
        #     "capital_minimo": int(capital_minimo),
        #     "include_keywords": include_keywords,
        #     "exclude_keywords": exclude_keywords,
        #     "filtrar_me_epp": filtrar_me_epp,
        #     "score_minimo": int(score_minimo),
        #     "enviar_sheets": enviar_sheets,
        # }
        #
        # leads = run_scraper(config)

        # Placeholder para loading
        with st.status("Processando extração de dados...", expanded=True) as status:
            st.write("Conectando aos servidores de busca...")
            time.sleep(1)
            st.write("Filtrando por Capital Social e Keywords...")
            time.sleep(1.5)
            st.write("Enriquecendo contatos...")
            time.sleep(0.5)
            status.update(label="Processo Concluído!", state="complete", expanded=False)

        # Mock de dados (Substitua pela sua chamada 'run_scraper')
        data = {
            "Empresa": ["Indústria Alpha Ltda", "Beta Tech S.A.", "Gamma Solutions"],
            "Cidade": ["São Paulo SP", "São Paulo SP", "Belo Horizonte MG"],
            "Telefone": ["(11) 99999-9999", "(11) 3030-3030", "(31) 98888-8888"],
            "Score": [98, 95, 82]
        }
        df = pd.DataFrame(data)

        # Exibição dos Resultados (Card "Caro")
        st.markdown(f"""
        <div class="result-metric-card">
            <div style="font-family: 'Inter'; font-size: 0.9rem; color: #94a3b8; text-transform: uppercase;">Leads Encontrados</div>
            <div style="font-family: 'Inter'; font-size: 3rem; font-weight: 800; color: #fff; line-height: 1.2;">{len(df)}</div>
            <div style="font-family: 'Inter'; font-size: 0.8rem; color: #00f3ff;">Prontos para exportação</div>
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(df, use_container_width=True)

        # Botão Download (Centralizado via colunas)
        c_dl_1, c_dl_2, c_dl_3 = st.columns([1, 2, 1])
        with c_dl_2:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Baixar CSV Completo",
                data=csv,
                file_name="leads_export.csv",
                mime="text/csv",
                use_container_width=True
            )
