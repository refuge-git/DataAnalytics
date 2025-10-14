# import pandas as pd
# import unicodedata
# import os

# # Caminho absoluto do arquivo CSV original
# base_dir = os.path.dirname(__file__)
# file_path = os.path.join(base_dir, "INMET_SE_SP_A701_SAO PAULO - MIRANTE_01-01-2025_A_31-08-2025.csv")

# # Ler CSV ignorando as 8 primeiras linhas de cabeçalho
# df = pd.read_csv(file_path, sep=";", encoding="latin1", skiprows=8)

# # Normalizar nomes das colunas (remover acentos e espaços)
# df.columns = [
#     unicodedata.normalize("NFKD", col)
#     .encode("ASCII", "ignore")
#     .decode("utf-8")
#     .strip()
#     for col in df.columns
# ]

# # Mapeamento de nomes de colunas para nomes padronizados
# renomear = {
#     "data": ["Data"],
#     "hora_utc": ["Hora UTC"],
#     "chuva_mm": ["PRECIPITACAO TOTAL, HORARIO (mm)",
#                  "PRECIPITAO TOTAL, HORRIO (mm)"],
#     "temp_c": ["TEMPERATURA DO AR - BULBO SECO, HORARIA (C)"],
#     "umidade": ["UMIDADE RELATIVA DO AR, HORARIA (%)"]
# }

# # Criar dicionário de renomeação com base nas colunas existentes
# col_map = {}
# for novo, antigos in renomear.items():
#     for old in antigos:
#         if old in df.columns:
#             col_map[old] = novo

# # Renomear colunas
# df = df.rename(columns=col_map)

# # Criar coluna datetime combinando data e hora
# df["datetime"] = pd.to_datetime(
#     df["data"].astype(str) + " " + df["hora_utc"].astype(str),
#     format="%Y/%m/%d %H%M UTC",
#     errors="coerce"
# )

# # Converter colunas numéricas (corrigir vírgula decimal)
# for col in ["chuva_mm", "temp_c", "umidade"]:
#     if col in df.columns:
#         df[col] = df[col].astype(str).str.replace(",", ".").astype(float)

# # Extrair mês e ano
# df["mes"] = df["datetime"].dt.month
# df["ano"] = df["datetime"].dt.year

# # Função para gerar resumo diário com colunas separadas
# def resumo_diario(df_mes):
#     df_mes["dia"] = df_mes["datetime"].dt.date
#     resumo = df_mes.groupby("dia").agg({
#         "chuva_mm": ["min", "max", "mean", "sum"],
#         "temp_c": ["min", "max", "mean", "sum"],
#         "umidade": ["min", "max", "mean", "sum"]
#     })

#     # Ajustar nomes das colunas
#     resumo.columns = [
#         f"{variavel}_{estatistica}"
#         for variavel, estatistica in resumo.columns
#     ]

#     resumo = resumo.reset_index()
#     return resumo

# resumos = []
# for (ano, mes), df_mes in df.groupby(["ano", "mes"]):
#     resumo = resumo_diario(df_mes)
#     resumo["ano"] = ano
#     resumo["mes"] = mes
#     resumos.append(resumo)

# df_resumo_total = pd.concat(resumos, ignore_index=True)


# output_path = os.path.join(os.path.dirname(__file__), "resumo_total.csv")
# df_resumo_total.to_csv(output_path, index=False, sep=";", encoding="utf-8-sig")


# print("✅ Arquivo CSV gerado com separador ';' para abrir corretamente no Excel!")

import pandas as pd
import unicodedata
import os

# Caminho absoluto do arquivo CSV original
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "INMET_SE_SP_A701_SAO PAULO - MIRANTE_01-01-2025_A_30-09-2025.csv")

# Ler CSV ignorando as 8 primeiras linhas de cabeçalho
df = pd.read_csv(file_path, sep=";", encoding="latin1", skiprows=8)

# Normalizar nomes das colunas (remover acentos e espaços)
df.columns = [
    unicodedata.normalize("NFKD", col)
    .encode("ASCII", "ignore")
    .decode("utf-8")
    .strip()
    for col in df.columns
]

# Mapeamento de nomes de colunas para nomes padronizados
renomear = {
    "data": ["Data"],
    "hora_utc": ["Hora UTC"],
    "chuva_mm": ["PRECIPITACAO TOTAL, HORARIO (mm)", "PRECIPITAO TOTAL, HORRIO (mm)"],
    "temp_c": ["TEMPERATURA DO AR - BULBO SECO, HORARIA (C)"],
    "umidade": ["UMIDADE RELATIVA DO AR, HORARIA (%)"]
}

# Criar dicionário de renomeação com base nas colunas existentes
col_map = {}
for novo, antigos in renomear.items():
    for old in antigos:
        if old in df.columns:
            col_map[old] = novo

# Renomear colunas
df = df.rename(columns=col_map)

# Criar coluna datetime combinando data e hora
df["datetime"] = pd.to_datetime(
    df["data"].astype(str) + " " + df["hora_utc"].astype(str),
    format="%Y/%m/%d %H%M UTC",
    errors="coerce"
)

# Converter colunas numéricas (corrigir vírgula decimal)
for col in ["chuva_mm", "temp_c", "umidade"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(",", ".").astype(float)

# Extrair mês e ano
df["mes"] = df["datetime"].dt.month
df["ano"] = df["datetime"].dt.year

# Função para classificar estação do ano
def classificar_estacao(data):
    ano = data.year
    primavera = (pd.Timestamp(f"{ano}-09-22"), pd.Timestamp(f"{ano}-12-20"))
    verao = [(pd.Timestamp(f"{ano}-12-21"), pd.Timestamp(f"{ano+1}-03-20"))]
    outono = (pd.Timestamp(f"{ano}-03-21"), pd.Timestamp(f"{ano}-06-20"))
    inverno = (pd.Timestamp(f"{ano}-06-21"), pd.Timestamp(f"{ano}-09-21"))

    if primavera[0] <= data <= primavera[1]:
        return "Primavera"
    elif any(inicio <= data <= fim for inicio, fim in verao):
        return "Verao"
    elif outono[0] <= data <= outono[1]:
        return "Outono"
    elif inverno[0] <= data <= inverno[1]:
        return "Inverno"
    else:
        return "Verao"

# Função para gerar resumo diário com colunas separadas
def resumo_diario(df_mes):
    df_mes["dia"] = df_mes["datetime"].dt.date
    resumo = df_mes.groupby("dia").agg({
        "chuva_mm": ["min", "max", "mean", "sum"],
        "temp_c": ["min", "max", "mean", "sum"],
        "umidade": ["min", "max", "mean", "sum"]
    })

    # Ajustar nomes das colunas
    resumo.columns = [f"{variavel}_{estatistica}" for variavel, estatistica in resumo.columns]
    resumo = resumo.reset_index()

    # Adicionar coluna de estação
    resumo["estacao"] = pd.to_datetime(resumo["dia"]).apply(classificar_estacao)
    return resumo

# Gerar resumo mensal
resumos = []
for (ano, mes), df_mes in df.groupby(["ano", "mes"]):
    resumo = resumo_diario(df_mes)
    resumo["ano"] = ano
    resumo["mes"] = mes
    resumos.append(resumo)

df_resumo_total = pd.concat(resumos, ignore_index=True)

# Salvar no mesmo diretório do script
output_path = os.path.join(base_dir, "resumo_total.csv")
df_resumo_total.to_csv(output_path, index=False, sep=";", encoding="utf-8-sig")

print("✅ Arquivo CSV gerado com coluna 'estacao' e separador ';' para Excel!")
