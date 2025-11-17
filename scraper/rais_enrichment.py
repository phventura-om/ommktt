import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def buscar_funcionarios_proxy(cnpj):
    """Rastreia estimativa de funcionários usando bases públicas."""
    url = f"https://cnpj.biz/{cnpj.replace('.', '').replace('/', '').replace('-', '')}"
    try:
        html = requests.get(url, headers=HEADERS, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")

        bloco = soup.find("table", {"class": "table table-striped"})
        if not bloco:
            return None

        funcionarios = None
        faturamento = None

        for row in bloco.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) >= 2:
                chave = cols[0].get_text(strip=True)
                valor = cols[1].get_text(strip=True)

                if "Funcionários" in chave:
                    funcionarios = valor
                if "Faturamento Presumido" in chave:
                    faturamento = valor

        return {
            "funcionarios_estimado": funcionarios,
            "faturamento_estimado": faturamento
        }
    except:
        return None
