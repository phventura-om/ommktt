def classificar_aneel(cnae):
    if not cnae:
        return ("B3", "Baixa tensão")

    if cnae.startswith("10") or cnae.startswith("11") or cnae.startswith("12"):
        return ("A4", "Alta demanda industrial leve")

    if cnae.startswith("20") or cnae.startswith("22"):
        return ("A3a", "Alta demanda industrial média")

    if cnae.startswith("24") or cnae.startswith("25") or cnae.startswith("26"):
        return ("A3", "Alta demanda industrial pesada")

    if cnae.startswith("47"):
        return ("B3", "Comércio, baixa tensão")

    if cnae.startswith("41") or cnae.startswith("42") or cnae.startswith("43"):
        return ("B2", "Construção civil")

    return ("B3", "Baixa tensão geral")
