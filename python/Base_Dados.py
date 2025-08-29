import pandas as pd

file_path = "INMET_SE_SP_A701_SAO PAULO - MIRANTE_01-01-2025_A_31-07-2025.CSV"

# Pular as 8 primeiras linhas, pois não são dados úteis
df = pd.read_csv(file_path, sep=";", encoding="latin1", skiprows=8)

# Renomear colunas
df = df.rename(columns={
    "Data": "data",
    "Hora UTC": "hora_utc",
    "PRECIPITAÇÃO TOTAL, HORÁRIO (mm)": "chuva_mm",
    "TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)": "temp_c",
    "UMIDADE RELATIVA DO AR, HORARIA (%)": "umidade"
})

# Criar coluna datetime
df["datetime"] = pd.to_datetime(df["data"] + " " + df["hora_utc"], format="%Y/%m/%d %H%M UTC")

# Converter numéricos (corrigir vírgula decimal)
for col in ["chuva_mm", "temp_c", "umidade"]:
    df[col] = df[col].astype(str).str.replace(",", ".").astype(float)

# Criar coluna de mês e ano
df["mes"] = df["datetime"].dt.month
df["ano"] = df["datetime"].dt.year

# Resumo diário para um mês escolhido
def resumo_diario(mes_escolhido):
    df_mes = df[df["mes"] == mes_escolhido]
    df_daily = df_mes.groupby(df_mes["datetime"].dt.date).agg({
        "chuva_mm": "sum",
        "temp_c": "mean",
        "umidade": "mean"
    }).reset_index().rename(columns={"datetime": "dia"})
    return df_daily

mes_escolhido = int(input("Digite o número do mês para o resumo diário: "))

    

# Resumo diários do mês selecionado
print("Resumo diário:")
print(resumo_diario(mes_escolhido))

# Resumo mensal até o último mês disponível
df["mes_ano"] = df["datetime"].dt.to_period("M")
df_monthly = df.groupby("mes_ano").agg({
    "chuva_mm": "sum",
    "temp_c": "mean",
    "umidade": "mean"
}).reset_index()

print("\nResumo mensal :")
print(df_monthly)
