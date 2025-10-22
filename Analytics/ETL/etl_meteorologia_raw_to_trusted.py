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

    resumo = resumo_diario(df)
    resumo["arquivo_origem"] = os.path.basename(path)
    return resumo

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
