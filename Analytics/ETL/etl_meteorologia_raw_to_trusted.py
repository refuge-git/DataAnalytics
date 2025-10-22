# # import pandas as pd
# # import unicodedata
# # import os

# # # Caminho absoluto do arquivo CSV original
# # base_dir = os.path.dirname(__file__)
# # file_path = os.path.join(base_dir, "INMET_SE_SP_A701_SAO PAULO - MIRANTE_01-01-2025_A_31-08-2025.csv")

# # # Ler CSV ignorando as 8 primeiras linhas de cabeçalho
# # df = pd.read_csv(file_path, sep=";", encoding="latin1", skiprows=8)

# # # Normalizar nomes das colunas (remover acentos e espaços)
# # df.columns = [
# #     unicodedata.normalize("NFKD", col)
# #     .encode("ASCII", "ignore")
# #     .decode("utf-8")
# #     .strip()
# #     for col in df.columns
# # ]

# # # Mapeamento de nomes de colunas para nomes padronizados
# # renomear = {
# #     "data": ["Data"],
# #     "hora_utc": ["Hora UTC"],
# #     "chuva_mm": ["PRECIPITACAO TOTAL, HORARIO (mm)",
# #                  "PRECIPITAO TOTAL, HORRIO (mm)"],
# #     "temp_c": ["TEMPERATURA DO AR - BULBO SECO, HORARIA (C)"],
# #     "umidade": ["UMIDADE RELATIVA DO AR, HORARIA (%)"]
# # }

# # # Criar dicionário de renomeação com base nas colunas existentes
# # col_map = {}
# # for novo, antigos in renomear.items():
# #     for old in antigos:
# #         if old in df.columns:
# #             col_map[old] = novo

# # # Renomear colunas
# # df = df.rename(columns=col_map)

# # # Criar coluna datetime combinando data e hora
# # df["datetime"] = pd.to_datetime(
# #     df["data"].astype(str) + " " + df["hora_utc"].astype(str),
# #     format="%Y/%m/%d %H%M UTC",
# #     errors="coerce"
# # )

# # # Converter colunas numéricas (corrigir vírgula decimal)
# # for col in ["chuva_mm", "temp_c", "umidade"]:
# #     if col in df.columns:
# #         df[col] = df[col].astype(str).str.replace(",", ".").astype(float)

# # # Extrair mês e ano
# # df["mes"] = df["datetime"].dt.month
# # df["ano"] = df["datetime"].dt.year

# # # Função para gerar resumo diário com colunas separadas
# # def resumo_diario(df_mes):
# #     df_mes["dia"] = df_mes["datetime"].dt.date
# #     resumo = df_mes.groupby("dia").agg({
# #         "chuva_mm": ["min", "max", "mean", "sum"],
# #         "temp_c": ["min", "max", "mean", "sum"],
# #         "umidade": ["min", "max", "mean", "sum"]
# #     })

# #     # Ajustar nomes das colunas
# #     resumo.columns = [
# #         f"{variavel}_{estatistica}"
# #         for variavel, estatistica in resumo.columns
# #     ]

# #     resumo = resumo.reset_index()
# #     return resumo

# # resumos = []
# # for (ano, mes), df_mes in df.groupby(["ano", "mes"]):
# #     resumo = resumo_diario(df_mes)
# #     resumo["ano"] = ano
# #     resumo["mes"] = mes
# #     resumos.append(resumo)

# # df_resumo_total = pd.concat(resumos, ignore_index=True)


# # output_path = os.path.join(os.path.dirname(__file__), "resumo_total.csv")
# # df_resumo_total.to_csv(output_path, index=False, sep=";", encoding="utf-8-sig")


# # print("✅ Arquivo CSV gerado com separador ';' para abrir corretamente no Excel!")

# import pandas as pd
# import unicodedata
# import os

# # Caminho absoluto do arquivo CSV original
# base_dir = os.path.dirname(__file__)
# file_path = os.path.join(base_dir, "INMET_SE_SP_A701_SAO PAULO - MIRANTE_01-01-2025_A_30-09-2025.csv")

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
#     "chuva_mm": ["PRECIPITACAO TOTAL, HORARIO (mm)", "PRECIPITAO TOTAL, HORRIO (mm)"],
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

# # Função para classificar estação do ano
# def classificar_estacao(data):
#     ano = data.year
#     primavera = (pd.Timestamp(f"{ano}-09-22"), pd.Timestamp(f"{ano}-12-20"))
#     verao = [(pd.Timestamp(f"{ano}-12-21"), pd.Timestamp(f"{ano+1}-03-20"))]
#     outono = (pd.Timestamp(f"{ano}-03-21"), pd.Timestamp(f"{ano}-06-20"))
#     inverno = (pd.Timestamp(f"{ano}-06-21"), pd.Timestamp(f"{ano}-09-21"))

#     if primavera[0] <= data <= primavera[1]:
#         return "Primavera"
#     elif any(inicio <= data <= fim for inicio, fim in verao):
#         return "Verao"
#     elif outono[0] <= data <= outono[1]:
#         return "Outono"
#     elif inverno[0] <= data <= inverno[1]:
#         return "Inverno"
#     else:
#         return "Verao"

# # Função para gerar resumo diário com colunas separadas
# def resumo_diario(df_mes):
#     df_mes["dia"] = df_mes["datetime"].dt.date
#     resumo = df_mes.groupby("dia").agg({
#         "chuva_mm": ["min", "max", "mean", "sum"],
#         "temp_c": ["min", "max", "mean", "sum"],
#         "umidade": ["min", "max", "mean", "sum"]
#     })

#     # Ajustar nomes das colunas
#     resumo.columns = [f"{variavel}_{estatistica}" for variavel, estatistica in resumo.columns]
#     resumo = resumo.reset_index()

#     # Adicionar coluna de estação
#     resumo["estacao"] = pd.to_datetime(resumo["dia"]).apply(classificar_estacao)
#     return resumo

# # Gerar resumo mensal
# resumos = []
# for (ano, mes), df_mes in df.groupby(["ano", "mes"]):
#     resumo = resumo_diario(df_mes)
#     resumo["ano"] = ano
#     resumo["mes"] = mes
#     resumos.append(resumo)

# df_resumo_total = pd.concat(resumos, ignore_index=True)

# # Salvar no mesmo diretório do script
# output_path = os.path.join(base_dir, "resumo_total.csv")
# df_resumo_total.to_csv(output_path, index=False, sep=";", encoding="utf-8-sig")

# print("✅ Arquivo CSV gerado com coluna 'estacao' e separador ';' para Excel!")


# -*- coding: utf-8 -*-
import os, glob, unicodedata
import pandas as pd

# ======== Caminhos base (RAW → TRUSTED) ========
def data_analytics_root(script_dir: str) -> str:
    if "DataAnalytics" in script_dir:
        base = script_dir.split("DataAnalytics")[0]
        return os.path.join(base, "DataAnalytics")
    cur = script_dir
    while True:
        cand = os.path.join(cur, "DataAnalytics")
        if os.path.isdir(cand):
            return cand
        parent = os.path.dirname(cur)
        if parent == cur:
            return script_dir
        cur = parent

HERE = os.path.dirname(__file__)
DA_ROOT = data_analytics_root(HERE)
RAW_DIR = os.path.join(DA_ROOT, "Analytics", "s3-refuge-analysis-raw", "base-meteorologia")
TRUSTED_DIR = os.path.join(DA_ROOT, "Analytics", "s3-refuge-analysis-trusted", "base-meteorologia")
os.makedirs(TRUSTED_DIR, exist_ok=True)

# ======== Funções utilitárias ========
def normalize_cols(cols):
    return [
        unicodedata.normalize("NFKD", c).encode("ASCII", "ignore").decode("utf-8").strip()
        for c in cols
    ]

def classificar_estacao(ts):
    ano = ts.year
    primavera = (pd.Timestamp(f"{ano}-09-22"), pd.Timestamp(f"{ano}-12-20"))
    verao = [(pd.Timestamp(f"{ano}-12-21"), pd.Timestamp(f"{ano+1}-03-20"))]
    outono = (pd.Timestamp(f"{ano}-03-21"), pd.Timestamp(f"{ano}-06-20"))
    inverno = (pd.Timestamp(f"{ano}-06-21"), pd.Timestamp(f"{ano}-09-21"))
    if primavera[0] <= ts <= primavera[1]: return "Primavera"
    if any(i <= ts <= f for i, f in verao):  return "Verao"
    if outono[0]    <= ts <= outono[1]:     return "Outono"
    if inverno[0]   <= ts <= inverno[1]:    return "Inverno"
    return "Verao"

def resumo_diario(df_mes):
    df_mes = df_mes.copy()
    df_mes["dia"] = df_mes["datetime"].dt.date
    resumo = df_mes.groupby("dia").agg({
        "chuva_mm": ["min", "max", "mean", "sum"],
        "temp_c": ["min", "max", "mean", "sum"],
        "umidade": ["min", "max", "mean", "sum"]
    })
    resumo.columns = [f"{v}_{e}" for v, e in resumo.columns]
    resumo = resumo.reset_index()
    resumo["estacao"] = pd.to_datetime(resumo["dia"]).apply(classificar_estacao)
    return resumo

def tratar_arquivo(path):
    df = pd.read_csv(path, sep=";", encoding="latin1", skiprows=8)
    df.columns = normalize_cols(df.columns)

    # mapeamento -> nomes padronizados
    renomear = {
        "data": ["Data"],
        "hora_utc": ["Hora UTC"],
        "chuva_mm": [
            "PRECIPITACAO TOTAL, HORARIO (mm)",
            "PRECIPITAO TOTAL, HORRIO (mm)"
        ],
        "temp_c": ["TEMPERATURA DO AR - BULBO SECO, HORARIA (C)"],
        "umidade": ["UMIDADE RELATIVA DO AR, HORARIA (%)"]
    }
    col_map = {}
    for novo, antigos in renomear.items():
        for old in antigos:
            if old in df.columns:
                col_map[old] = novo
    df = df.rename(columns=col_map)

    # datetime
    df["datetime"] = pd.to_datetime(
        df["data"].astype(str) + " " + df["hora_utc"].astype(str),
        format="%Y/%m/%d %H%M UTC", errors="coerce"
    )

    # numéricos
    for c in ["chuva_mm", "temp_c", "umidade"]:
        if c in df.columns:
            df[c] = (
                df[c].astype(str)
                     .str.replace(",", ".", regex=False)
                     .str.replace("--", "", regex=False)
            )
            df[c] = pd.to_numeric(df[c], errors="coerce")

    df["ano"] = df["datetime"].dt.year
    df["mes"] = df["datetime"].dt.month

    resumos = []
    for (ano, mes), df_mes in df.groupby(["ano", "mes"]):
        r = resumo_diario(df_mes)
        r["ano"] = ano
        r["mes"] = mes
        resumos.append(r)
    if not resumos:
        return None
    resumo_total = pd.concat(resumos, ignore_index=True)
    resumo_total["arquivo_origem"] = os.path.basename(path)
    return resumo_total

# ======== Execução principal ========
all_csvs = sorted(glob.glob(os.path.join(RAW_DIR, "*.csv")))
if not all_csvs:
    raise FileNotFoundError(f"Nenhum CSV encontrado em: {RAW_DIR}")

todos_resumos = []
for csv_path in all_csvs:
    try:
        resumo = tratar_arquivo(csv_path)
        if resumo is not None:
            todos_resumos.append(resumo)
            print(f"✅ Processado: {os.path.basename(csv_path)}")
    except Exception as e:
        print(f"⚠️ Erro em {os.path.basename(csv_path)}: {e}")

if not todos_resumos:
    raise RuntimeError("Nenhum resumo gerado.")

df_resumo_total = pd.concat(todos_resumos, ignore_index=True)
output_path = os.path.join(TRUSTED_DIR, "resumo_total.csv")
df_resumo_total.to_csv(output_path, index=False, sep=";", encoding="utf-8-sig")

print(f"📦 Arquivo único de resumo gerado com sucesso:\n{output_path}")
