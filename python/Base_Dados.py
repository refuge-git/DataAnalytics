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

# Resumo diário para um mês escolhido
def resumo_diario(mes_escolhido):
    df_mes = df[df["mes"] == mes_escolhido]
    if df_mes.empty:
        return f"Nenhum dado disponível para o mês {mes_escolhido}."
    df_daily = df_mes.groupby(df_mes["datetime"].dt.date).agg({
        "chuva_mm": "sum" if "chuva_mm" in df_mes else "first",
        "temp_c": "mean" if "temp_c" in df_mes else "first",
        "umidade": "mean" if "umidade" in df_mes else "first"
    }).reset_index().rename(columns={"datetime": "dia"})
    return df_daily

mes_escolhido = int(input("Digite o número do mês para o resumo diário: "))

print("\nResumo diário:")
print(resumo_diario(mes_escolhido))

# Resumo mensal até o último mês disponível
df["mes_ano"] = df["datetime"].dt.to_period("M")
df_monthly = df.groupby("mes_ano").agg({
    "chuva_mm": "sum" if "chuva_mm" in df else "first",
    "temp_c": "mean" if "temp_c" in df else "first",
    "umidade": "mean" if "umidade" in df else "first"
}).reset_index()

print("\nResumo mensal:")
print(df_monthly)
