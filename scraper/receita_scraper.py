import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def consultar_receita(cnpj):
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj.replace('.', '').replace('/', '').replace('-', '')}"
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        data = resp.json()

        if "nome" not in data:
            return None

        return {
            "razao_social": data.get("nome"),
            "nome_fantasia": data.get("fantasia"),
            "cnae_principal": data.get("atividade_principal", [{}])[0].get("code"),
            "cnaes_secundarios": ", ".join([i.get("code") for i in data.get("atividades_secundarias", [])]),
            "abertura": data.get("abertura"),
            "status": data.get("situacao"),
            "capital_social": data.get("capital_social"),
            "telefone_receita": data.get("telefone"),
            "email": data.get("email"),
            "endereco_receita": f"{data.get('logradouro')}, {data.get('numero')} - {data.get('bairro')} - {data.get('municipio')} {data.get('uf')}",
            "porte": data.get("porte"),
        }

    except Exception:
        return None
