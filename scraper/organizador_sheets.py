# organizador_sheets.py
import re
import unicodedata
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import WorksheetNotFound


# ============================================
# 🔧 1. AUTENTICAÇÃO / PLANILHA
# ============================================
def conectar_planilha(cred_path, spreadsheet_name):
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope)
    client = gspread.authorize(creds)
    sh = client.open(spreadsheet_name)
    return sh


def obter_aba(sh, aba_name, rows=2000, cols=30, limpar=True):
    try:
        ws = sh.worksheet(aba_name)
    except WorksheetNotFound:
        ws = sh.add_worksheet(title=aba_name, rows=str(rows), cols=str(cols))

    if limpar:
        ws.clear()
    return ws


# ============================================
# 🧼 2. PADRONIZAÇÃO
# ============================================
def limpar_texto(txt):
    if not txt:
        return ""
    txt = str(txt)
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(c for c in txt if not unicodedata.combining(c))
    return txt.strip()


def validar_cnpj(cnpj):
    if not cnpj:
        return False
    cnpj_numbers = re.sub(r"\D", "", str(cnpj))
    return len(cnpj_numbers) == 14


def parse_capital(capital):
    if not capital:
        return 0.0
    s = str(capital).strip()
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except Exception:
        return 0.0


# ============================================
# 🔧 3. ORGANIZAÇÃO DA BASE
# ============================================
def organizar_base(base_final):
    nova_lista = []
    vistos = set()

    for item in base_final:
        nome = limpar_texto(item.get("nome_google", ""))
        cidade = limpar_texto(item.get("cidade", ""))
        segmento = limpar_texto(item.get("segmento", ""))
        cnpj = item.get("cnpj", "")

        chave = (nome.lower(), cidade.lower(), re.sub(r"\D", "", str(cnpj)))
        if chave in vistos:
            continue
        vistos.add(chave)

        if not validar_cnpj(cnpj):
            continue

        capital = parse_capital(item.get("capital_social", ""))

        novo = {
            "nome": nome,
            "cidade": cidade,
            "segmento": segmento,
            "cnpj": cnpj,
            "porte": limpar_texto(item.get("porte", "")),
            "capital_social": capital,
            "endereco": limpar_texto(
                item.get("endereco_receita", item.get("endereco", ""))
            ),
            "cnae_principal": limpar_texto(item.get("cnae_principal", "")),
            "classe_aneel": limpar_texto(item.get("classe_aneel", "")),
            "descricao_classe": limpar_texto(item.get("descricao_classe", "")),
            "url": item.get("url", ""),
        }

        nova_lista.append(novo)

    # ordena por cidade → segmento → nome
    nova_lista = sorted(
        nova_lista, key=lambda x: (x["cidade"], x["segmento"], x["nome"])
    )
    return nova_lista


# ============================================
# 📊 4. RESUMOS / DASHBOARD
# ============================================
def gerar_resumo_por_cidade(dados):
    resumo = {}
    for d in dados:
        cidade = d["cidade"] or "N/A"
        if cidade not in resumo:
            resumo[cidade] = {"cidade": cidade, "qtd_empresas": 0, "capital_total": 0.0}
        resumo[cidade]["qtd_empresas"] += 1
        resumo[cidade]["capital_total"] += d.get("capital_social", 0.0)

    lista = list(resumo.values())
    lista.sort(key=lambda x: x["qtd_empresas"], reverse=True)
    return lista


def gerar_resumo_por_segmento(dados):
    resumo = {}
    for d in dados:
        seg = d["segmento"] or "N/A"
        if seg not in resumo:
            resumo[seg] = {
                "segmento": seg,
                "qtd_empresas": 0,
                "capital_total": 0.0,
            }
        resumo[seg]["qtd_empresas"] += 1
        resumo[seg]["capital_total"] += d.get("capital_social", 0.0)

    lista = list(resumo.values())
    lista.sort(key=lambda x: x["qtd_empresas"], reverse=True)
    return lista


def selecionar_top_clientes(dados, n=50):
    base = [d for d in dados if d.get("capital_social", 0) > 0]
    base.sort(key=lambda x: x["capital_social"], reverse=True)
    return base[:n]


# ============================================
# 📤 5. EXPORTAÇÃO PARA ABAS
# ============================================
def exportar_para_aba(ws, dados):
    if not dados:
        print(f"⚠ Nenhum dado para exportar na aba '{ws.title}'.")
        return

    header = list(dados[0].keys())
    ws.insert_row(header, 1)
    linhas = [list(d.values()) for d in dados]
    ws.insert_rows(linhas, 2)
    print(f"✔ Aba '{ws.title}' atualizada com {len(linhas)} linhas.")


def atualizar_planilha_completa(
    cred_path="credenciais.json",
    spreadsheet_name="icp_completo",
    aba_dados="dados",
    aba_cidade="resumo_cidade",
    aba_segmento="resumo_segmento",
    aba_top="top_clientes",
    base_final=None,
):
    if not base_final:
        print("⚠ Base vazia, nada para enviar ao Sheets.")
        return

    print("📊 Organizando base para Google Sheets...")
    base_limpa = organizar_base(base_final)

    sh = conectar_planilha(cred_path, spreadsheet_name)

    # aba 1: dados completos
    ws_dados = obter_aba(sh, aba_dados)
    exportar_para_aba(ws_dados, base_limpa)

    # aba 2: resumo por cidade
    resumo_cidade = gerar_resumo_por_cidade(base_limpa)
    ws_cidade = obter_aba(sh, aba_cidade)
    exportar_para_aba(ws_cidade, resumo_cidade)

    # aba 3: resumo por segmento
    resumo_segmento = gerar_resumo_por_segmento(base_limpa)
    ws_seg = obter_aba(sh, aba_segmento)
    exportar_para_aba(ws_seg, resumo_segmento)

    # aba 4: top clientes (capital)
    top = selecionar_top_clientes(base_limpa, n=50)
    ws_top = obter_aba(sh, aba_top)
    exportar_para_aba(ws_top, top)

    print("✅ Planilha atualizada com base, resumos e top clientes.")
