# scraper_core.py
import csv
import time
import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from ddgs import DDGS
import urllib3

from cnpj_detector import extrair_cnpj_site, extrair_cnpj_texto
from receita_scraper import consultar_receita
from organizador_sheets import atualizar_planilha_completa

# Desativa avisos SSL chatos
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================================
# ⚙️ CONFIGURAÇÕES GERAIS
# ==========================================================
MAX_REQ_PER_SEC = 3

DOMINIOS_BANIDOS = [
    "guiapj.com", "cuiket.com", "descubraonline.com", "acheempresa.com",
    "telelistas.net", "solutudo.com.br", "cnpj.biz", "br.biz", "guiamais.com",
    "dnb.com", "yelp.com", "facebook.com", "linkedin.com"
]

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
PHONE_REGEX = r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}"
WHATS_REGEX = r"(?:(?:\+55\s?)?\(?\d{2}\)?\s?)?(?:9\d{4}|[2-9]\d{3})-?\d{4}"

# caches simples em memória
cache_cnpj = {}
cache_dominios = {}
cache_redes_sociais = {}
cache_contatos = {}


# ==========================================================
# 🔍 BUSCA (DuckDuckGo)
# ==========================================================
def buscar_duckduckgo(termo, num_results=25):
    """Busca gratuita via DuckDuckGo."""
    time.sleep(1 / MAX_REQ_PER_SEC)
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(termo, max_results=num_results))
            return [
                {
                    "titulo": r.get("title", ""),
                    "link": r.get("href", ""),
                    "descricao": r.get("body", "")
                }
                for r in results
            ]
    except Exception as e:
        print(f"⚠ Erro DuckDuckGo: {e}")
        return []


def filtrar_resultados(resultados):
    """Remove sites genéricos e domínios repetidos."""
    vistos = set()
    filtrados = []
    for r in resultados:
        link = r.get("link", "")
        if not link:
            continue
        try:
            dominio = link.split("/")[2]
        except Exception:
            continue

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
def extrair_contatos_site(url):
    """Busca e-mail, telefone e WhatsApp em algumas páginas padrão do site."""
    contatos = {"email": "", "telefone": "", "whatsapp": ""}
    if not url:
        return contatos

    try:
        dominio = url.split("/")[2]
    except Exception:
        dominio = ""

    if dominio and dominio in cache_contatos:
        return cache_contatos[dominio]

    caminhos_contato = ["", "/contato", "/fale-conosco", "/sobre", "/quem-somos"]
    for caminho in caminhos_contato:
        link = url.rstrip("/") + caminho
        try:
            resp = requests.get(
                link,
                timeout=10,
                verify=False,
                headers={"User-Agent": "Mozilla/5.0"}
            )
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

    if dominio:
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
# 🎯 FILTRO GENÉRICO DE ICP
# ==========================================================
def is_bom_lead(texto, include_keywords, exclude_keywords, capital, capital_minimo):
    """
    Aplica filtro textual + capital mínimo.
    - include_keywords: se não estiver vazio → exige pelo menos uma palavra presente
    - exclude_keywords: se palavra aparecer → exclui
    """
    texto = texto.lower()

    # palavras de exclusão
    for p in exclude_keywords or []:
        if p.lower() in texto:
            return False

    # palavras de inclusão
    if include_keywords:
        if not any(p.lower() in texto for p in include_keywords):
            return False

    # capital mínimo
    if capital_minimo and capital and capital < capital_minimo:
        return False

    return True


# ==========================================================
# 🧩 PROCESSAMENTO DE UMA EMPRESA
# ==========================================================
def processar_empresa(item, termo, config):
    include_keywords = config["include_keywords"]
    exclude_keywords = config["exclude_keywords"]
    capital_minimo = config["capital_minimo"]
    cidades_permitidas = config["cidades_permitidas"]

    nome = item.get("titulo", "").strip()
    link = item.get("link", "")
    desc = item.get("descricao", "")

    if not nome:
        return None

    # --- CNPJ ---
    cnpj = extrair_cnpj_texto(desc)
    if not cnpj and link:
        try:
            dominio = link.split("/")[2]
        except Exception:
            dominio = ""
        if dominio and dominio not in cache_dominios:
            cache_dominios[dominio] = extrair_cnpj_site(link)
        cnpj = cache_dominios.get(dominio)

    # --- Receita Federal ---
    receita = None
    if cnpj:
        receita = cache_cnpj.get(cnpj)
        if not receita:
            try:
                receita = consultar_receita(cnpj)
                cache_cnpj[cnpj] = receita
            except Exception:
                receita = None

    # --- Contatos ---
    contatos = extrair_contatos_site(link)
    if not any(contatos.values()):
        return None

    # --- Porte, município, capital ---
    porte = ""
    municipio = ""
    capital = 0
    if receita and isinstance(receita, dict):
        porte = str(
            receita.get("porte")
            or receita.get("porte_da_empresa")
            or receita.get("porte_empresa")
            or ""
        ).upper()
        municipio = str(receita.get("municipio") or "").upper()
        capital_str = str(receita.get("capital_social") or "")
        capital = float(re.sub(r"[^\d]", "", capital_str) or 0)

    # descarta ME/EPP
    if porte in ["ME", "MICRO EMPRESA", "EPP", "EMPRESA DE PEQUENO PORTE"]:
        return None

    # filtra município
    if cidades_permitidas and municipio and municipio not in cidades_permitidas:
        return None

    # filtro de ICP
    texto_full = f"{nome} {desc} {termo}"
    if not is_bom_lead(texto_full, include_keywords, exclude_keywords, capital, capital_minimo):
        return None

    # --- Redes sociais + score ---
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


# ==========================================================
# 🚀 FUNÇÃO PRINCIPAL DO SCRAPER
# ==========================================================
def run_scraper(config, progress_callback=None):
    """
    Roda a prospecção com base em um dict de configuração.

    config espera:
      - termos: list[str]
      - cidades: list[str] (ex.: 'Belo Horizonte MG')
      - capital_minimo: int
      - include_keywords: list[str]
      - exclude_keywords: list[str]
      - enviar_sheets: bool  (se True, atualiza planilha)

    progress_callback(opcional): função chamada como
      progress_callback(current, total, percent)
    para você atualizar barra de progresso no front.
    """

    termos = config.get("termos", [])
    cidades = config.get("cidades", [])
    capital_minimo = int(config.get("capital_minimo", 0))
    include_keywords = config.get("include_keywords", [])
    exclude_keywords = config.get("exclude_keywords", [])
    enviar_sheets = bool(config.get("enviar_sheets", True))

    # calcula municípios permitidos a partir das cidades
    cidades_permitidas = []
    for c in cidades:
        partes = c.split()
        if len(partes) >= 2:
            municipio = " ".join(partes[:-1]).upper()
            cidades_permitidas.append(municipio)

    # injeta no config para uso interno
    config["capital_minimo"] = capital_minimo
    config["include_keywords"] = include_keywords
    config["exclude_keywords"] = exclude_keywords
    config["cidades_permitidas"] = cidades_permitidas

    leads_quentes = []
    tarefas = []
    empresas_vistas = set()
    pool = ThreadPoolExecutor(max_workers=20)

    # monta tarefas
    for cidade in cidades:
        for termo_base in termos:
            termo = f"{termo_base} {cidade}"
            resultados = filtrar_resultados(buscar_duckduckgo(termo, num_results=25))
            for item in resultados:
                nome = item.get("titulo", "").strip()
                if not nome or nome in empresas_vistas:
                    continue
                empresas_vistas.add(nome)
                tarefas.append(pool.submit(processar_empresa, item, termo, config))

    total = len(tarefas) or 1
    concluido = 0

    for t in as_completed(tarefas):
        try:
            r = t.result()
        except Exception as e:
            print("⚠ Erro em tarefa:", e)
            r = None

        if r:
            leads_quentes.append(r)

        concluido += 1
        if progress_callback:
            pct = int(concluido / total * 100)
            progress_callback(concluido, total, pct)

    # filtra por score mínimo
    leads_quentes = [x for x in leads_quentes if x.get("lead_score", 0) >= 6]

    # atualiza planilha no Google Sheets (se habilitado)
    if enviar_sheets and leads_quentes:
        atualizar_planilha_completa(
            cred_path="credenciais.json",
            spreadsheet_name="empresas_leads_quentes",
            aba_dados="leads",
            aba_cidade="resumo_cidade",
            aba_segmento="resumo_segmento",
            aba_top="top_clientes",
            base_final=leads_quentes,
        )

    return leads_quentes
