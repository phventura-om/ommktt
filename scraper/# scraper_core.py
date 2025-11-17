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
from organizador_sheets import atualizar_planilha_completa  # já sem cred_path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MAX_REQ_PER_SEC = 3

DOMINIOS_BANIDOS = [
    "guiapj.com", "cuiket.com", "descubraonline.com", "acheempresa.com",
    "telelistas.net", "solutudo.com.br", "cnpj.biz", "br.biz", "guiamais.com",
    "dnb.com", "yelp.com", "facebook.com", "linkedin.com"
]

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
PHONE_REGEX = r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}"
WHATS_REGEX = r"(?:(?:\+55\s?)?\(?\d{2}\)?\s?)?(?:9\d{4}|[2-9]\d{3})-?\d{4}"

cache_cnpj = {}
cache_dominios = {}
cache_contatos = {}
cache_redes_sociais = {}


# ==========================================================
# Helpers
# ==========================================================
def buscar_duckduckgo(termo, num_results=25):
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
    except:
        return []


def filtrar_resultados(resultados):
    vistos = set()
    out = []
    for r in resultados:
        link = r.get("link")
        if not link:
            continue
        try:
            dom = link.split("/")[2]
        except:
            continue
        if any(d in dom for d in DOMINIOS_BANIDOS):
            continue
        if dom in vistos:
            continue
        vistos.add(dom)
        out.append(r)
    return out


def extrair_contatos_site(url):
    contatos = {"email": "", "telefone": "", "whatsapp": ""}
    if not url:
        return contatos
    try:
        dominio = url.split("/")[2]
    except:
        dominio = ""
    if dominio in cache_contatos:
        return cache_contatos[dominio]

    caminhos = ["", "/contato", "/fale-conosco", "/sobre", "/quem-somos"]
    for c in caminhos:
        link = url.rstrip("/") + c
        try:
            r = requests.get(link, timeout=10, verify=False,
                             headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code != 200:
                continue
            txt = BeautifulSoup(r.text, "html.parser").get_text(" ")

            if not contatos["email"]:
                em = re.findall(EMAIL_REGEX, txt)
                if em:
                    contatos["email"] = em[0]

            if not contatos["telefone"]:
                ph = re.findall(PHONE_REGEX, txt)
                if ph:
                    contatos["telefone"] = ph[0]

            if not contatos["whatsapp"]:
                ws = re.findall(WHATS_REGEX, txt)
                if ws:
                    contatos["whatsapp"] = ws[0]

            if any(contatos.values()):
                break
        except:
            continue

    cache_contatos[dominio] = contatos
    return contatos


def buscar_redes_sociais(nome):
    if nome in cache_redes_sociais:
        return cache_redes_sociais[nome]

    termo = f"{nome} instagram facebook linkedin"
    res = buscar_duckduckgo(termo)
    redes = {"instagram": "", "facebook": "", "linkedin": ""}
    for r in res:
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
# ICP (CEMIG PF e PJ)
# ==========================================================
def is_icp_cemig(texto, consumo, tipo):
    texto = texto.lower()

    # deve ser CEMIG
    if not any(x in texto for x in ["mg", "minas gerais", "cemig"]):
        return False

    # PF: consumo >= 500
    if tipo == "PF" and consumo < 500:
        return False

    # PJ: consumo >= 500 (ideal 1000)
    if tipo == "PJ" and consumo < 500:
        return False

    # motivos típicos
    motivos = [
        "redução de custo",
        "economia de energia",
        "economizar luz",
        "energia sustentável",
        "sem instalação",
        "economizar"
    ]
    if not any(m in texto for m in motivos):
        return True  # não obrigatório 100%

    return True


# ==========================================================
# Processamento
# ==========================================================
def processar_empresa(item, termo, config):
    nome = item.get("titulo", "").strip()
    link = item.get("link", "")
    desc = item.get("descricao", "")

    if not nome:
        return None

    texto_full = f"{nome} {desc} {termo}"

    # CNPJ
    cnpj = extrair_cnpj_texto(desc)
    if not cnpj and link:
        try:
            dom = link.split("/")[2]
        except:
            dom = ""
        if dom not in cache_dominios:
            cache_dominios[dom] = extrair_cnpj_site(link)
        cnpj = cache_dominios.get(dom)

    # Receita
    receita = None
    if cnpj:
        receita = cache_cnpj.get(cnpj)
        if not receita:
            try:
                receita = consultar_receita(cnpj)
                cache_cnpj[cnpj] = receita
            except:
                receita = None

    # Contatos
    contatos = extrair_contatos_site(link)
    if not any(contatos.values()):
        return None

    # Dados receita
    consumo = 0
    municipio = ""
    porte = ""

    if receita:
        municipio = str(receita.get("municipio", "")).upper()
        cap_str = str(receita.get("capital_social", "")).replace(".", "").replace(",", "")
        consumo = int(re.sub(r"[^\d]", "", cap_str) or 0)
        porte = str(receita.get("porte", "")).upper()

    # Filtrar ME/EPP
    if porte in ["ME", "MICRO EMPRESA", "EPP"]:
        return None

    # Aplicar ICP CEMIG
    if not is_icp_cemig(texto_full, consumo, config["tipo_cliente"]):
        return None

    redes = buscar_redes_sociais(nome)

    lead = {
        "nome": nome,
        "url": link,
        "descricao": desc,
        "cnpj": cnpj or "",
        "municipio": municipio,
        "capital": consumo,
        "porte": porte,
        **contatos,
        **redes,
        "icp_tipo": config["tipo_cliente"]
    }

    if receita:
        lead.update(receita)

    return lead


# ==========================================================
# Função principal
# ==========================================================
def run_scraper(config, progress_callback=None):
    termos = config["termos"]
    cidades = config["cidades"]

    config["tipo_cliente"] = config.get("tipo_cliente", "PJ")  # PF ou PJ

    leads = []
    tarefas = []
    pool = ThreadPoolExecutor(max_workers=20)

    empresas_vistas = set()

    for cidade in cidades:
        for termo in termos:
            termo_busca = f"{termo} {cidade}"
            res = filtrar_resultados(buscar_duckduckgo(termo_busca))

            for item in res:
                nome = item.get("titulo", "").strip()
                if not nome or nome in empresas_vistas:
                    continue
                empresas_vistas.add(nome)
                tarefas.append(pool.submit(processar_empresa, item, termo_busca, config))

    total = len(tarefas)
    done = 0

    for t in as_completed(tarefas):
        try:
            r = t.result()
            if r:
                leads.append(r)
        except:
            pass

        done += 1
        if progress_callback:
            progress_callback(done, total, int(done / total * 100))

    # Criar tabela e resumo
    resumo = [
        ["Métrica", "Valor"],
        ["Leads qualificados", len(leads)],
        ["Tipo de cliente", config["tipo_cliente"]],
        ["Cidades", ", ".join(cidades)],
        ["Termos", ", ".join(termos)],
    ]

    tabela = []
    if leads:
        campos = sorted({k for lead in leads for k in lead.keys()})
        tabela.append(campos)
        for lead in leads:
            tabela.append([lead.get(c, "") for c in campos])

    # Atualizar sheets sem cred_path
    try:
        atualizar_planilha_completa(
            spreadsheet_name=config.get("spreadsheet_name", "Leads ICP"),
            aba_resumo=config.get("aba_resumo", "resumo_icp"),
            aba_leads=config.get("aba_leads", "leads_organizados"),
            base_resumo=resumo,
            base_final=tabela
        )
    except Exception as e:
        print("Erro ao atualizar Sheets:", e)

    return leads
