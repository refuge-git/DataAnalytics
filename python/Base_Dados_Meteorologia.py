import pandas as pd
import unicodedata

file_path = "INMET_SE_SP_A701_SAO PAULO - MIRANTE_01-01-2025_A_31-07-2025.CSV"

# Ler CSV tirando as primeiras 8 linhas de cabeçalho
df = pd.read_csv(file_path, sep=";", encoding="utf-8", skiprows=8)

df.columns = [
    unicodedata.normalize("NFKD", col)
    .encode("ASCII", "ignore")
    .decode("utf-8")
    .strip()
    for col in df.columns
]

# Renomear colunas principais
renomear = {
    "data": ["Data"],
    "hora_utc": ["Hora UTC"],
    "chuva_mm": ["PRECIPITACAO TOTAL, HORARIO (mm)",
                 "PRECIPITAO TOTAL, HORRIO (mm)"],
    "temp_c": ["TEMPERATURA DO AR - BULBO SECO, HORARIA (C)"],
    "umidade": ["UMIDADE RELATIVA DO AR, HORARIA (%)"]
}

# Criar mapeamento dinâmico
col_map = {}
for novo, antigos in renomear.items():
    for old in antigos:
        if old in df.columns:
            col_map[old] = novo

df = df.rename(columns=col_map)

df["datetime"] = pd.to_datetime(
    df["data"] + " " + df["hora_utc"],
    format="%Y/%m/%d %H%M UTC",
    errors="coerce"
)

# Converter numéricos (corrigir vírgula decimal)
for col in ["chuva_mm", "temp_c", "umidade"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(",", ".").astype(float)

df["mes"] = df["datetime"].dt.month
df["ano"] = df["datetime"].dt.year

# Função para gerar resumo diário de um mês
def resumo_diario(df_mes):
    df_daily = df_mes.groupby(df_mes["datetime"].dt.date).agg({
        "chuva_mm": "sum" if "chuva_mm" in df_mes else "first",
        "temp_c": ["min", "max", "mean"] if "temp_c" in df_mes else "first",
        "umidade": ["min", "max", "mean"] if "umidade" in df_mes else "first"
    }).reset_index().rename(columns={"datetime": "dia"})
    if "temp_c" in df_mes:
        df_daily.columns = ['dia', 'chuva_mm', 
                            'temp_c_min', 'temp_c_max', 'temp_c_mean', 
                            'umidade_min', 'umidade_max', 'umidade_mean']
    return df_daily

# Resumo diário para cada mês disponível
with pd.ExcelWriter("resumo_diario_mensal.xlsx") as writer:
    for (ano, mes), df_mes in df.groupby(["ano", "mes"]):
        resumo = resumo_diario(df_mes)
        nome_aba = f"{ano}-{str(mes).zfill(2)}"
        resumo.to_excel(writer, sheet_name=nome_aba, index=False)

print("Arquivo 'resumo_diario_mensal.xlsx' gerado!")