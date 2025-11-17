import requests
import time

def buscar_google_serper(api_key, query, num_results=10):
    url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query,
        "num": num_results,
        "hl": "pt-br",
        "gl": "br"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        print("❌ Erro na API:", response.text)
        return []

    data = response.json()

    resultados = []

    # Resultados orgânicos
    for item in data.get("organic", []):
        resultados.append({
            "titulo": item.get("title"),
            "link": item.get("link"),
            "descricao": item.get("snippet"),
        })

    # Painel lateral (Business info)
    business = data.get("knowledgeGraph", {})

    if business:
        resultados.append({
            "titulo": business.get("title"),
            "link": business.get("website"),
            "telefone": business.get("phone"),
            "endereco": business.get("address"),
            "nota": business.get("rating"),
            "reviews": business.get("reviewCount"),
            "categoria": business.get("type"),
            "descricao": business.get("description"),
        })

    return resultados
