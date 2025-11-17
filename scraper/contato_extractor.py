# contato_extractor.py
import re
import requests
from bs4 import BeautifulSoup

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
PHONE_REGEX = r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}"
WHATS_REGEX = r"(?:(?:\+55\s?)?\(?\d{2}\)?\s?)?(?:9\d{4}|[2-9]\d{3})-?\d{4}"

def extrair_contatos_site(url):
    contatos = {"email": "", "telefone": "", "whatsapp": ""}
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        html = resp.text
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ")

        # E-mail
        emails = re.findall(EMAIL_REGEX, text)
        if emails:
            contatos["email"] = emails[0]

        # Telefone / WhatsApp
        telefones = re.findall(PHONE_REGEX, text)
        whats = re.findall(WHATS_REGEX, text)
        if telefones:
            contatos["telefone"] = telefones[0]
        if whats:
            contatos["whatsapp"] = whats[0]

    except Exception as e:
        print(f"⚠ Erro ao extrair contatos de {url}: {e}")
    return contatos
