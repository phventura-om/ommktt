# organizador_sheets.py
import os
import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

# ==========================================================
# 🔌 Função robusta para conectar ao Google Sheets
# ==========================================================
def conectar_planilha(spreadsheet_name: str, cred_path: str = "credenciais.json"):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = None

    # 1️⃣ Tenta carregar via arquivo local (rodando no VSCode / servidor próprio)
    if os.path.exists(cred_path):
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope)
            gc = gspread.authorize(creds)
            return gc.open(spreadsheet_name)
        except Exception as e:
            st.error(f"Erro ao carregar credenciais locais: {e}")

    # 2️⃣ Se não existe arquivo → tenta via Streamlit Secrets
    if "gcp_service_account" in st.secrets:
        try:
            service_info = dict(st.secrets["gcp_service_account"])
            creds = ServiceAccountCredentials.from_json_keyfile_dict(service_info, scope)
            gc = gspread.authorize(creds)
            return gc.open(spreadsheet_name)
        except Exception as e:
            st.error(f"Erro ao carregar credenciais via Streamlit Secrets: {e}")

    # 3️⃣ Se nada funcionar → erro final
    raise FileNotFoundError(
        "Nenhuma credencial encontrada. "
        "Coloque credenciais.json na raiz OU configure st.secrets['gcp_service_account']."
    )

# ==========================================================
# ✏️ Função principal de atualização
# ==========================================================
def atualizar_planilha_completa(
    spreadsheet_name: str,
    aba_resumo: str,
    aba_leads: str,
    base_resumo: list,
    base_final: list,
    cred_path: str = "credenciais.json"
):
    # Conecta na planilha
    sh = conectar_planilha(spreadsheet_name, cred_path)

    # Atualiza resumo
    ws_resumo = sh.worksheet(aba_resumo)
    ws_resumo.clear()

    if base_resumo:
        ws_resumo.update("A1", base_resumo)

    # Atualiza leads
    ws_leads = sh.worksheet(aba_leads)
    ws_leads.clear()

    if base_final:
        ws_leads.update("A1", base_final)

    return True
