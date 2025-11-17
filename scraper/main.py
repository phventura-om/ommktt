import csv
import time
import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from bs4 import BeautifulSoup
from ddgs import DDGS
import urllib3

import tkinter as tk
from tkinter import ttk, messagebox

from cnpj_detector import extrair_cnpj_site, extrair_cnpj_texto, buscar_cnpj_google_serper
from receita_scraper import consultar_receita
from organizador_sheets import atualizar_planilha_completa

# Desativa avisos SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================================
# ⚙️ CONFIGURAÇÕES (VALORES PADRÃO)
# ==========================================================
MAX_REQ_PER_SEC = 3

# mínimo de capital social (regula o "porte" mínimo que você quer)
MIN_CAPITAL = 300000  # ajuste se ficar muito/ pouco restrito

# 🔹 Termos de busca (usados na DuckDuckGo)
#    – você configura na tela, mas aqui ficam os defaults
TERMOS_BASE = [
    "hospital particular",
    "hospital privado",
    "hospital geral particular",
    "hospital de luxo",
    "hospital premium",
    "clínica hospitalar",
    "centro médico",
    "centro medico",
    "hospital e maternidade particular",
]

# 🔹 Cidades de atuação
CIDADES_BUSCA = [
    # Minas Gerais
    "Belo Horizonte MG",
    "Contagem MG",
    "Betim MG",
    "Nova Lima MG",
    "Ribeirão das Neves MG",
    "Santa Luzia MG",
    "Vespasiano MG",
    "Sabará MG",
    "Ibirité MG",
    "Juiz de Fora MG",

    # Rio de Janeiro
    "Rio de Janeiro RJ",
    "Volta Redonda RJ",
    "Barra Mansa RJ",
]

# 🔹 Validação pela Receita (por município)
CIDADES_PERMITIDAS = [
    "BELO HORIZONTE", "CONTAGEM", "BETIM", "NOVA LIMA",
    "RIBEIRÃO DAS NEVES", "SANTA LUZIA", "VESPASIANO",
    "SABARÁ", "IBIRITÉ", "JUIZ DE FORA",
    "RIO DE JANEIRO", "VOLTA REDONDA", "BARRA MANSA",
]

DOMINIOS_BANIDOS = [
    "guiapj.com", "cuiket.com", "descubraonline.com", "acheempresa.com",
    "telelistas.net", "solutudo.com.br", "cnpj.biz", "br.biz", "guiamais.com",
    "dnb.com", "yelp.com", "facebook.com", "linkedin.com"
]

# ==========================================================
# 🧠 CACHES
# ==========================================================
cache_cnpj = {}
cache_dominios = {}
cache_nome_cnpj = {}
cache_redes_sociais = {}
cache_contatos = {}
empresas_processadas = set()

# ==========================================================
# 🔧 FILTRO DE CONTEÚDO (GENÉRICO)
# ==========================================================
# Palavras que reforçam que é bom lead (defaults focados em hospital/clinica)
INCLUDE_KEYWORDS = [
    "hospital",
    "clínica",
    "clinica",
    "centro médico",
    "centro medico",
    "instituto",
    "day hospital",
]

# Palavras que excluem lead (defaults para saúde que NÃO queremos)
EXCLUDE_KEYWORDS = [
    "farmácia", "farmacia", "drogaria", "drugstore",
    "laboratório farmacêutico", "laboratorio farmaceutico",
    "análises clínicas", "analises clinicas",
    "veterinário", "veterinaria", "pet shop", "petshop",
    "clínica veterinária", "clinica veterinaria",
    "posto de saúde", "posto de saude",
    "ubs ", "upa ", "sus ",
    "unidade básica de saúde", "unidade basica de saude",
]

# Se você quiser ignorar completamente os defaults e usar só o que
# colocar na tela, é só limpar esses campos na interface.
# (não precisa mexer aqui no código)


# ==========================================================
# 🔍 DUCKDUCKGO SEARCH
# ==========================================================
def buscar_duckduckgo(termo, num_results=25):
    """Busca gratuita via DuckDuckGo."""
    time.sleep(1 / MAX_REQ_PER_SEC)
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(termo, max_results=num_results))
            return [
                {"titulo": r.get("title", ""), "link": r.get("href", ""), "descricao": r.get("body", "")}
                for r in results
            ]
    except Exception as e:
        print(f"⚠ Erro DuckDuckGo: {e}")
        return []

def filtrar_resultados(resultados):
    """Remove sites genéricos e duplicados."""
    vistos = set()
    filtrados = []
    for r in resultados:
        link = r.get("link", "")
        if not link:
            continue
        dominio = link.split("/")[2]
        if any(d in dominio for d in DOMINIOS_BANIDOS):
            continue
        if dominio in vistos:
            continue
        vistos.add(dominio)
        filtrados.append(r)
    return filtrados

# ==========================================================
# 📞 EXTRAÇÃO DE CONTATOS
# ==========================================================
EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
PHONE_REGEX = r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}"
WHATS_REGEX = r"(?:(?:\+55\s?)?\(?\d{2}\)?\s?)?(?:9\d{4}|[2-9]\d{3})-?\d{4}"

def extrair_contatos_site(url):
    """Busca e-mail, telefone e WhatsApp em várias páginas do site."""
    contatos = {"email": "", "telefone": "", "whatsapp": ""}
    if not url:
        return contatos

    try:
        dominio = url.split("/")[2]
        if dominio in cache_contatos:
            return cache_contatos[dominio]
    except Exception:
        dominio = ""

    caminhos_contato = ["", "/contato", "/fale-conosco", "/sobre", "/quem-somos"]
    for caminho in caminhos_contato:
        link = url.rstrip("/") + caminho
        try:
            resp = requests.get(link, timeout=10, verify=False, headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code != 200:
                continue
            text = BeautifulSoup(resp.text, "html.parser").get_text(" ")

            if not contatos["email"]:
                emails = re.findall(EMAIL_REGEX, text)
                if emails:
                    contatos["email"] = emails[0]
            if not contatos["telefone"]:
                tels = re.findall(PHONE_REGEX, text)
                if tels:
                    contatos["telefone"] = tels[0]
            if not contatos["whatsapp"]:
                whats = re.findall(WHATS_REGEX, text)
                if whats:
                    contatos["whatsapp"] = whats[0]

            if any(contatos.values()):
                break
        except Exception:
            continue

    cache_contatos[dominio] = contatos
    return contatos

# ==========================================================
# 🌐 REDES SOCIAIS
# ==========================================================
def buscar_redes_sociais(nome):
    if nome in cache_redes_sociais:
        return cache_redes_sociais[nome]

    termo = f"{nome} instagram facebook linkedin"
    resultados = buscar_duckduckgo(termo)
    redes = {"instagram": "", "facebook": "", "linkedin": ""}

    for r in resultados:
        link = r.get("link", "")
        if "instagram.com" in link and not redes["instagram"]:
            redes["instagram"] = link
        elif "facebook.com" in link and not redes["facebook"]:
            redes["facebook"] = link
        elif "linkedin.com" in link and not redes["linkedin"]:
            redes["linkedin"] = link

    cache_redes_sociais[nome] = redes
    return redes

# ==========================================================
# 🎯 FILTRO GENÉRICO – QUEM É BOM LEAD
# ==========================================================
def is_bom_lead(nome, desc, termo, receita, capital):
    """
    Filtro genérico de conteúdo, guiado pelas palavras que você
    configurar na interface (INCLUDE_KEYWORDS e EXCLUDE_KEYWORDS).
    """
    texto = f"{nome} {desc} {termo}".lower()

    # 1) Excluir se tiver alguma palavra proibida
    if EXCLUDE_KEYWORDS:
        for p in EXCLUDE_KEYWORDS:
            if p.lower() in texto:
                return False

    # 2) Se houver palavras de inclusão, exige que pelo menos uma apareça
    if INCLUDE_KEYWORDS:
        if not any(p.lower() in texto for p in INCLUDE_KEYWORDS):
            return False

    # 3) (Opcional) Capital mínimo
    if capital and MIN_CAPITAL:
        if capital < MIN_CAPITAL:
            return False

    return True

# ==========================================================
# 🧩 PROCESSAR EMPRESA
# ==========================================================
def processar_empresa(item, termo):
    try:
        nome = item.get("titulo", "").strip()
        link = item.get("link", "")
        desc = item.get("descricao", "")

        if not nome or nome in empresas_processadas:
            return None
        empresas_processadas.add(nome)

        # Extrair CNPJ
        cnpj = extrair_cnpj_texto(desc)
        if not cnpj and link:
            try:
                dominio = link.split("/")[2]
            except Exception:
                dominio = ""
            if dominio and dominio not in cache_dominios:
                cache_dominios[dominio] = extrair_cnpj_site(link)
            cnpj = cache_dominios.get(dominio)

        # Consultar Receita (seguro)
        receita = None
        if cnpj:
            receita = cache_cnpj.get(cnpj)
            if not receita:
                try:
                    receita = consultar_receita(cnpj)
                    cache_cnpj[cnpj] = receita
                except Exception:
                    receita = None

        # Extrair contatos
        contatos = extrair_contatos_site(link)
        if not any(contatos.values()):
            return None  # sem contato = descarta

        # Porte da empresa pela Receita (quando disponível)
        porte = ""
        if receita and isinstance(receita, dict):
            porte = str(
                receita.get("porte")
                or receita.get("porte_da_empresa")
                or receita.get("porte_empresa")
                or ""
            ).upper()

        # descarta micro e pequenas (mantém empresas maiores)
        if porte in ["ME", "MICRO EMPRESA", "EPP", "EMPRESA DE PEQUENO PORTE"]:
            return None

        # Município seguro
        municipio = ""
        if receita and isinstance(receita, dict):
            municipio = str(receita.get("municipio") or "").upper()
        if CIDADES_PERMITIDAS and municipio and not any(c in municipio for c in CIDADES_PERMITIDAS):
            return None

        # Capital social seguro
        capital = 0
        if receita and isinstance(receita, dict):
            capital_str = str(receita.get("capital_social") or "")
            capital = float(re.sub(r"[^\d]", "", capital_str) or 0)

        # 🎯 filtro de conteúdo genérico
        if not is_bom_lead(nome, desc, termo, receita, capital):
            return None

        # Lead scoring
        redes = buscar_redes_sociais(nome)
        score = 0
        if contatos.get("email"): score += 2
        if contatos.get("telefone"): score += 2
        if contatos.get("whatsapp"): score += 3
        if redes.get("instagram"): score += 1
        if redes.get("facebook"): score += 1
        if redes.get("linkedin"): score += 1
        if receita: score += 1

        dados = {
            "nome": nome,
            "url": link,
            "descricao": desc,
            "termo_busca": termo,
            "cnpj": cnpj or "",
            "municipio": municipio,
            "capital": capital,
            "porte": porte,
            **contatos,
            **redes,
            "lead_score": score,
        }

        if receita and isinstance(receita, dict):
            dados.update(receita)

        return dados

    except Exception as e:
        print(f"⚠ Erro processando {item.get('link', '')}: {type(e).__name__} - {e}")
        return None

# ==========================================================
# 💾 SALVAR CSV
# ==========================================================
def salvar_csv(dados, nome="leads_quentes.csv"):
    if not dados:
        print("⚠ Nada para salvar.")
        return
    campos = sorted({k for item in dados for k in item})
    with open(nome, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(dados)
    print(f"💾 CSV salvo: {nome} ({len(dados)} leads quentes)")

# ==========================================================
# 🪟 TELA TKINTER PARA CONFIGURAR PARÂMETROS
# ==========================================================
def configurar_parametros_tk():
    """
    Tela para configurar:
    - Capital mínimo
    - Termos de busca (para DuckDuckGo)
    - Cidades
    - Palavras que indicam bom lead
    - Palavras que excluem lead
    """
    global MIN_CAPITAL, TERMOS_BASE, CIDADES_BUSCA, CIDADES_PERMITIDAS
    global INCLUDE_KEYWORDS, EXCLUDE_KEYWORDS

    root = tk.Tk()
    root.title("Configuração do Scraper de Leads")
    root.geometry("800x750")

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    titulo = ttk.Label(frame, text="Configuração do Scraper de Leads", font=("Segoe UI", 12, "bold"))
    titulo.pack(pady=(0, 10))

    # ---------------- Capital mínimo ----------------
    frame_capital = ttk.LabelFrame(frame, text="Capital social mínimo (R$)", padding=10)
    frame_capital.pack(fill="x", pady=5)

    var_capital = tk.StringVar(value=str(MIN_CAPITAL))
    ttk.Label(frame_capital, text="Somente números (ex: 300000):").pack(anchor="w")
    entry_capital = ttk.Entry(frame_capital, textvariable=var_capital)
    entry_capital.pack(fill="x")

    # ---------------- Termos / segmentos de busca ----------------
    frame_termos = ttk.LabelFrame(frame, text="Termos / segmentos de busca (para a pesquisa)", padding=10)
    frame_termos.pack(fill="both", expand=True, pady=5)

    ttk.Label(
        frame_termos,
        text="Um termo por linha (ex.: hospital particular, clínica hospitalar, centro médico...)."
    ).pack(anchor="w")

    text_termos = tk.Text(frame_termos, height=6)
    text_termos.pack(fill="both", expand=True, pady=(5, 0))
    text_termos.insert("1.0", "\n".join(TERMOS_BASE))

    # ---------------- Cidades ----------------
    frame_cidades = ttk.LabelFrame(frame, text="Cidades para buscar", padding=10)
    frame_cidades.pack(fill="both", expand=True, pady=5)

    ttk.Label(
        frame_cidades,
        text="Uma cidade por linha (ex.: Belo Horizonte MG, Juiz de Fora MG, Rio de Janeiro RJ...)."
    ).pack(anchor="w")

    text_cidades = tk.Text(frame_cidades, height=6)
    text_cidades.pack(fill="both", expand=True, pady=(5, 0))
    text_cidades.insert("1.0", "\n".join(CIDADES_BUSCA))

    # ---------------- Palavras de filtro ----------------
    frame_filtro = ttk.LabelFrame(frame, text="Filtro de conteúdo (quem entra / quem é excluído)", padding=10)
    frame_filtro.pack(fill="both", expand=True, pady=5)

    sub_frame = ttk.Frame(frame_filtro)
    sub_frame.pack(fill="both", expand=True)

    # INCLUDE
    left = ttk.Frame(sub_frame)
    left.pack(side="left", fill="both", expand=True, padx=(0, 5))

    ttk.Label(
        left,
        text="Palavras que indicam bom lead\n(se houver, pelo menos uma precisa aparecer)\nEx.: hospital; clínica; centro médico"
    ).pack(anchor="w")

    text_include = tk.Text(left, height=8)
    text_include.pack(fill="both", expand=True, pady=(5, 0))
    text_include.insert("1.0", "\n".join(INCLUDE_KEYWORDS))

    # EXCLUDE
    right = ttk.Frame(sub_frame)
    right.pack(side="right", fill="both", expand=True, padx=(5, 0))

    ttk.Label(
        right,
        text="Palavras que excluem lead\n(se aparecer, a empresa é descartada)\nEx.: farmácia; pet shop; posto de saúde"
    ).pack(anchor="w")

    text_exclude = tk.Text(right, height=8)
    text_exclude.pack(fill="both", expand=True, pady=(5, 0))
    text_exclude.insert("1.0", "\n".join(EXCLUDE_KEYWORDS))

    # ---------------- Botões ----------------
    frame_botoes = ttk.Frame(frame)
    frame_botoes.pack(fill="x", pady=10)

    def usar_padrao():
        root.destroy()

    def iniciar():
        nonlocal var_capital, text_termos, text_cidades, text_include, text_exclude
        global MIN_CAPITAL, TERMOS_BASE, CIDADES_BUSCA, CIDADES_PERMITIDAS
        global INCLUDE_KEYWORDS, EXCLUDE_KEYWORDS

        # Capital mínimo
        capital_txt = var_capital.get().strip()
        if capital_txt:
            try:
                MIN_CAPITAL = int(re.sub(r"[^\d]", "", capital_txt))
            except ValueError:
                messagebox.showwarning(
                    "Valor inválido",
                    "Capital mínimo inválido. Mantendo valor padrão."
                )

        # Termos base
        termos_txt = text_termos.get("1.0", "end").strip()
        if termos_txt:
            bruto = termos_txt.replace("\r", "\n")
            blocos = []
            for linha in bruto.split("\n"):
                for parte in linha.split(";"):
                    parte = parte.strip()
                    if parte:
                        blocos.append(parte)
            if blocos:
                TERMOS_BASE = blocos

        # Cidades
        cidades_txt = text_cidades.get("1.0", "end").strip()
        if cidades_txt:
            bruto_cid = cidades_txt.replace("\r", "\n")
            cidades = []
            for linha in bruto_cid.split("\n"):
                for parte in linha.split(";"):
                    parte = parte.strip()
                    if parte:
                        cidades.append(parte)
            if cidades:
                CIDADES_BUSCA = cidades

                # Recalcula CIDADES_PERMITIDAS a partir das cidades
                novas_cidades_permitidas = []
                for cidade in CIDADES_BUSCA:
                    partes = cidade.split()
                    if len(partes) >= 2:
                        municipio = " ".join(partes[:-1]).upper()
                        novas_cidades_permitidas.append(municipio)
                if novas_cidades_permitidas:
                    CIDADES_PERMITIDAS = novas_cidades_permitidas

        # INCLUDE_KEYWORDS
        include_txt = text_include.get("1.0", "end").strip()
        if include_txt != "":
            bruto_inc = include_txt.replace("\r", "\n")
            inc = []
            for linha in bruto_inc.split("\n"):
                for parte in linha.split(";"):
                    parte = parte.strip()
                    if parte:
                        inc.append(parte.lower())
            INCLUDE_KEYWORDS = inc
        else:
            INCLUDE_KEYWORDS = []  # sem palavras de inclusão, não limita por texto

        # EXCLUDE_KEYWORDS
        exclude_txt = text_exclude.get("1.0", "end").strip()
        if exclude_txt != "":
            bruto_exc = exclude_txt.replace("\r", "\n")
            exc = []
            for linha in bruto_exc.split("\n"):
                for parte in linha.split(";"):
                    parte = parte.strip()
                    if parte:
                        exc.append(parte.lower())
            EXCLUDE_KEYWORDS = exc
        else:
            EXCLUDE_KEYWORDS = []

        print("\n📌 Configuração utilizada nesta execução:")
        print(f"  • Capital mínimo: {MIN_CAPITAL}")
        print(f"  • Termos base: {', '.join(TERMOS_BASE)}")
        print(f"  • Cidades: {', '.join(CIDADES_BUSCA)}")
        print(f"  • Palavras de inclusão: {', '.join(INCLUDE_KEYWORDS) if INCLUDE_KEYWORDS else '(nenhuma)'}")
        print(f"  • Palavras de exclusão: {', '.join(EXCLUDE_KEYWORDS) if EXCLUDE_KEYWORDS else '(nenhuma)'}\n")

        root.destroy()

    btn_padrao = ttk.Button(frame_botoes, text="Usar padrão e iniciar", command=usar_padrao)
    btn_padrao.pack(side="left", padx=5)

    btn_iniciar = ttk.Button(frame_botoes, text="Iniciar prospecção", command=iniciar)
    btn_iniciar.pack(side="right", padx=5)

    root.mainloop()

# ==========================================================
# 🚀 MAIN
# ==========================================================
def main():
    print("🚀 Iniciando prospecção de leads...\n")

    configurar_parametros_tk()

    leads_quentes = []
    tarefas = []
    pool = ThreadPoolExecutor(max_workers=20)

    for cidade in CIDADES_BUSCA:
        for termo_base in TERMOS_BASE:
            termo = f"{termo_base} {cidade}"
            print(f"🔍 Buscando: {termo}")
            resultados = filtrar_resultados(buscar_duckduckgo(termo, num_results=25))
            for item in resultados:
                tarefas.append(pool.submit(processar_empresa, item, termo))

    print("\n⚙ Processando empresas...\n")
    for t in tqdm(as_completed(tarefas), total=len(tarefas)):
        r = t.result()
        if r:
            leads_quentes.append(r)

    # só mantém leads com score mínimo
    leads_quentes = [x for x in leads_quentes if x.get("lead_score", 0) >= 6]

    print(f"\n🔥 Leads quentes encontrados: {len(leads_quentes)}")
    salvar_csv(leads_quentes)

    atualizar_planilha_completa(
        cred_path="credenciais.json",
        spreadsheet_name="empresas_leads_quentes",
        aba_dados="leads",
        aba_cidade="resumo_cidade",
        aba_segmento="resumo_segmento",
        aba_top="top_clientes",
        base_final=leads_quentes,
    )

    print("\n✅ Prospecção concluída com sucesso!")


if __name__ == "__main__":
    main()
