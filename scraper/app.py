import io
import streamlit as st
import pandas as pd
import time # Importado apenas para simular loading visual se precisar, pode remover se nao usar

# Se o seu arquivo se chama scraper_core.py, mantenha essa importação.
# Caso esteja testando sem o arquivo, comente a linha abaixo.
try:
    from scraper_core import run_scraper
except ImportError:
    # Mock para testar visualmente caso não tenha o scraper_core
    def run_scraper(config, progress_callback=None):
        time.sleep(2)
        return [{"nome": "Empresa Teste Futuro", "municipio": "São Paulo SP", "email": "contato@teste.com", "lead_score": 98}]

# ----------------------------------------------------------
# CONFIG DA PÁGINA
# ----------------------------------------------------------
st.set_page_config(
    page_title="OM MKT · Lead Scraper",
    layout="wide",
    page_icon="⚡"
)

# ----------------------------------------------------------
# ESTILO FUTURISTA (CSS AVANÇADO)
# ----------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Rajdhani:wght@500;600;700&display=swap');

    /* --- VARIÁVEIS GLOBAIS --- */
    :root {
        --bg-dark: #030508;
        --glass-bg: rgba(20, 25, 40, 0.6);
        --glass-border: rgba(255, 255, 255, 0.08);
        --neon-blue: #00f3ff;
        --neon-purple: #bc13fe;
        --text-main: #e0e6ed;
        --text-muted: #64748b;
    }

    /* --- FUNDO E GERAL --- */
    body {
        background-color: var(--bg-dark);
        color: var(--text-main);
        font-family: 'Rajdhani', sans-serif; /* Fonte base mais tech */
    }
    
    .stApp {
        background: 
            radial-gradient(circle at 50% 0%, #1a1d3a 0%, #030508 60%),
            linear-gradient(0deg, rgba(0,0,0,0.2) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,0,0,0.2) 1px, transparent 1px);
        background-size: 100% 100%, 40px 40px, 40px 40px;
        background-attachment: fixed;
    }

    /* Grid animado no fundo (opcional, para dar profundidade) */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 50vh;
        background: linear-gradient(180deg, rgba(0, 243, 255, 0.03) 0%, transparent 100%);
        pointer-events: none;
        z-index: 0;
    }

    .block-container {
        max-width: 1080px;
        padding-top: 2rem;
        z-index: 1;
        position: relative;
    }

    /* --- HERO SECTION --- */
    .hero-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding: 2rem;
        background: rgba(10, 12, 20, 0.4);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 30px rgba(0,0,0,0.5);
        position: relative;
        overflow: hidden;
    }
    
    /* Barra de luz decorativa no topo do hero */
    .hero-container::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--neon-blue), transparent);
        opacity: 0.7;
    }

    .logo-area h1 {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        font-size: 3rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0;
        background: linear-gradient(90deg, #fff, var(--neon-blue));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(0, 243, 255, 0.3);
    }
    
    .logo-subtitle {
        font-family: 'JetBrains Mono', monospace;
        color: var(--neon-blue);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }

    /* --- INPUTS (A MÁGICA ACONTECE AQUI) --- */
    /* Label dos inputs */
    .stTextInput label, .stTextArea label, .stNumberInput label {
        font-family: 'JetBrains Mono', monospace !important;
        text-transform: uppercase !important;
        font-size: 0.75rem !important;
        letter-spacing: 1.5px !important;
        color: var(--neon-blue) !important;
        margin-bottom: 0.5rem !important;
    }

    /* Caixas de Input */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background-color: rgba(10, 14, 23, 0.6) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #fff !important;
        border-radius: 4px !important; /* Bordas mais retas = mais tech */
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
    }

    /* Foco no Input (Glow) */
    .stTextInput > div > div > input:focus, 
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--neon-blue) !important;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.2), inset 0 0 10px rgba(0, 243, 255, 0.05) !important;
        background-color: rgba(10, 14, 23, 0.9) !important;
    }

    /* Placeholder styling */
    ::placeholder {
        color: rgba(255,255,255,0.2) !important;
        font-style: italic;
    }

    /* --- CARD PRINCIPAL --- */
    .glass-card {
        background: rgba(13, 17, 28, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        margin-bottom: 2rem;
    }

    /* --- BOTÃO DE AÇÃO --- */
    .stButton > button {
        width: 100%;
        border: none !important;
        background: linear-gradient(90deg, var(--neon-blue), #2d6cdf) !important;
        color: #000 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        padding: 0.8rem 0 !important;
        border-radius: 4px !important;
        transition: all 0.3s ease !important;
        position: relative;
        z-index: 1;
        clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px); /* Corte futurista nos cantos */
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px var(--neon-blue);
        filter: brightness(1.2);
    }

    /* --- PROGRESS BAR --- */
    .stProgress > div > div > div > div {
        background-color: var(--neon-blue) !important;
        box-shadow: 0 0 10px var(--neon-blue);
    }
    
    /* --- HELPER TEXT --- */
    .help-text {
        font-size: 0.7rem;
        color: var(--text-muted);
        font-family: 'JetBrains Mono', monospace;
        margin-top: -10px;
        margin-bottom: 10px;
        display: block;
    }

    /* Hide Streamlit footer/menu for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------
# LAYOUT VISUAL
# ----------------------------------------------------------

# HERO SECTION (HTML PURO DENTRO DO MARKDOWN PARA CONTROLE TOTAL)
st.markdown("""
<div class="hero-container">
    <div class="logo-area">
        <div class="logo-subtitle">DATA ENGINE v.2.0</div>
        <h1>OM MKT <span style="color:#fff; opacity:0.3; font-weight:300;">|</span> LEAD SCRAPER</h1>
        <p style="color: #8892b0; margin-top: 10px; font-size: 0.9rem; max-width: 600px;">
            Sistema proprietário de inteligência comercial. Defina os parâmetros táticos abaixo para iniciar a extração de dados em tempo real.
        </p>
    </div>
    <div style="text-align: right; border-left: 1px solid rgba(255,255,255,0.1); padding-left: 2rem;">
         <div style="font-family: 'JetBrains Mono'; font-size: 0.7rem; color: #00f3ff; margin-bottom: 5px;">SYSTEM STATUS</div>
         <div style="font-weight: bold; color: #fff;">ONLINE</div>
         <div style="margin-top: 15px; font-family: 'JetBrains Mono'; font-size: 0.7rem; color: #bc13fe; margin-bottom: 5px;">TARGET</div>
         <div style="font-weight: bold; color: #fff;">B2B / DECISORES</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ----------------------------------------------------------
# FORMULÁRIO (Dentro de um container estilizado)
# ----------------------------------------------------------

# Usamos colunas para centralizar o formulário e dar "respiro" nas laterais
col_padding_left, col_main, col_padding_right = st.columns([1, 6, 1])

with col_main:
    # Início do Card de Vidro (Container Visual)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Termos de Busca
    termos_raw = st.text_area(
        "TERMOS DE BUSCA (TARGET)",
        placeholder="ex: hospital particular\nclínica premium\nsupermercado atacado",
        height=120,
        help="Digite um setor por linha."
    )
    st.markdown('<span class="help-text">// Um termo por linha. O sistema fará a combinação matricial com as cidades.</span>', unsafe_allow_html=True)
    
    # Cidades
    cidades_raw = st.text_area(
        "CIDADES / MERCADOS (GEO)",
        placeholder="ex: Belo Horizonte MG\nJuiz de Fora MG\nRio de Janeiro RJ",
        height=120,
        help="Digite cidade e UF."
    )
    st.markdown('<span class="help-text">// Formato: Cidade UF (ex: São Paulo SP).</span>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Filtros Avançados em 3 Colunas
    c1, c2, c3 = st.columns(3)
    
    with c1:
        capital_minimo = st.number_input(
            "CAPITAL SOCIAL MÍNIMO (R$)",
            min_value=0,
            value=0,
            step=50000,
            format="%d"
        )
    
    with c2:
        include_raw = st.text_input(
            "PALAVRAS OBRIGATÓRIAS",
            placeholder="ex: ltda, s.a."
        )
    
    with c3:
        exclude_raw = st.text_input(
            "PALAVRAS EXCLUÍDAS",
            placeholder="ex: me, mei"
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Botão Principal
    start_button = st.button("INICIAR PROSPECÇÃO SYSTEM")
    
    st.markdown('</div>', unsafe_allow_html=True) # Fim do Glass Card


# ----------------------------------------------------------
# RESULTADOS E LÓGICA (Mantida do seu original)
# ----------------------------------------------------------

# Container para resultados
res_container = st.container()

with res_container:
    if start_button:
        # Espaçamento visual
        st.markdown("<br>", unsafe_allow_html=True)
        
        status_placeholder = st.empty()
        progress_bar = st.progress(0)
        
        termos = [t.strip() for t in termos_raw.splitlines() if t.strip()]
        cidades = [c.strip() for c in cidades_raw.splitlines() if c.strip()]
        include_keywords = [k.strip() for k in include_raw.split(",") if k.strip()]
        exclude_keywords = [k.strip() for k in exclude_raw.split(",") if k.strip()]

        if not termos:
            status_placeholder.error("ERRO: INPUT DE TERMOS VAZIO.")
        elif not cidades:
            status_placeholder.error("ERRO: INPUT DE CIDADES VAZIO.")
        else:
            config = {
                "termos": termos,
                "cidades": cidades,
                "capital_minimo": capital_minimo,
                "include_keywords": include_keywords,
                "exclude_keywords": exclude_keywords,
            }

            status_placeholder.markdown(
                "<div style='text-align:center; color: #00f3ff; font-family: JetBrains Mono;'>[SYSTEM] INICIALIZANDO PROTOCOLO DE EXTRAÇÃO...</div>",
                unsafe_allow_html=True,
            )

            def progress_callback(current, total, percent):
                try:
                    progress_bar.progress(percent)
                    status_placeholder.markdown(
                        f"<div style='text-align:center; color: #fff; font-family: JetBrains Mono;'>PROCESSANDO NODE: {current}/{total} ({percent}%)</div>",
                        unsafe_allow_html=True,
                    )
                except Exception:
                    pass

            try:
                leads = run_scraper(config, progress_callback=progress_callback)
            except Exception as e:
                status_placeholder.error(f"FALHA CRÍTICA: {e}")
                leads = []

            if not leads:
                progress_bar.progress(100)
                status_placeholder.warning("NENHUM DADO ENCONTRADO COM OS PARÂMETROS ATUAIS.")
            else:
                progress_bar.progress(100)
                status_placeholder.success("OPERAÇÃO CONCLUÍDA COM SUCESSO.")

                df = pd.DataFrame(leads)

                # Exibição dos Resultados Estilizada
                st.markdown(f"""
                <div style="background: rgba(0, 243, 255, 0.05); border: 1px solid #00f3ff; padding: 15px; border-radius: 8px; margin: 20px 0; text-align: center;">
                    <span style="font-size: 2rem; font-weight: bold; color: #fff;">{len(df)}</span>
                    <br>
                    <span style="font-family: 'JetBrains Mono'; color: #00f3ff; font-size: 0.8rem;">LEADS QUALIFICADOS ENCONTRADOS</span>
                </div>
                """, unsafe_allow_html=True)

                cols_show = [c for c in ["nome", "municipio", "email", "telefone", "whatsapp", "lead_score", "url"] if c in df.columns]
                st.dataframe(df[cols_show], use_container_width=True)

                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False, sep=";")
                csv_data = csv_buffer.getvalue()

                # Centralizar botão de download
                c_dl_1, c_dl_2, c_dl_3 = st.columns([1,1,1])
                with c_dl_2:
                    st.download_button(
                        label="📥 EXPORTAR DADOS (CSV)",
                        data=csv_data,
                        file_name="leads_ommkt_extracted.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
