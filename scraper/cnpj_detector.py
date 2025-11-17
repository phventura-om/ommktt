import re
import requests

PADRAO_CNPJ = re.compile(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}")

def extrair_cnpj_texto(texto):
    encontrados = PADRAO_CNPJ.findall(texto)
    return encontrados[0] if encontrados else ""

def extrair_cnpj_site(url):
    try:
        resp = requests.get(url, timeout=10)
        html = resp.text
        return extrair_cnpj_texto(html)
    except:
        return ""

def buscar_cnpj_google_serper(api_key, nome_empresa):
    try:
        import google_api_scraper
        resultados = google_api_scraper.buscar_google_serper(
            api_key,
            f"{nome_empresa} CNPJ",
            num_results=5
        )
        for item in resultados:
            if "descricao" in item and item["descricao"]:
                cnpj = extrair_cnpj_texto(item["descricao"])
                if cnpj:
                    return cnpj
        return ""
    except:
        return ""