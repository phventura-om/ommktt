from google_api_scraper import buscar_google_serper

def buscar_redes_sociais(api_key, nome_empresa, cidade):
    consulta = f"{nome_empresa} {cidade} instagram facebook linkedin"
    resultados = buscar_google_serper(api_key, consulta, num_results=8)

    instagram = ""
    facebook = ""
    linkedin = ""

    for r in resultados:
        link = r.get("link", "")

        if "instagram.com" in link and not instagram:
            instagram = link

        if "facebook.com" in link and not facebook:
            facebook = link

        if "linkedin.com" in link and not linkedin:
            linkedin = link

    return {
        "instagram": instagram,
        "facebook": facebook,
        "linkedin": linkedin
    }
