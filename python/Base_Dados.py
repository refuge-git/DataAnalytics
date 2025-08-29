import pandas as pd
import unicodedata
import matplotlib.pyplot as plt

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

deseja_grafico = input("\nDeseja ver os gráficos dos resumos apresentados? ")

if deseja_grafico.lower() == "sim":
    # Gráfico do resumo diário
    df_daily = resumo_diario(mes_escolhido)
    if not df_daily.empty:
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Barras de chuva
        ax1.bar(df_daily["dia"], df_daily["chuva_mm"], color="skyblue", alpha=0.6, label="Chuva (mm)")
        ax1.set_xlabel("Dia")
        ax1.set_ylabel("Chuva (mm)", color="skyblue")
        ax1.tick_params(axis='y', labelcolor="skyblue")

        # Linhas de temperatura e umidade
        ax2 = ax1.twinx()
        ax2.plot(df_daily["dia"], df_daily["temp_c"], color="orange", marker="o", label="Temperatura (°C)")
        ax2.plot(df_daily["dia"], df_daily["umidade"], color="blue", marker="o", label="Umidade (%)")
        ax2.set_ylabel("Temperatura/Umidade", color="black")

        fig.autofmt_xdate(rotation=45)
        fig.tight_layout()
        fig.legend(loc="upper right")
        plt.title(f"Resumo diário - Mês {mes_escolhido}")
        plt.show()

    # Gráfico resumo mensal
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.bar(df_monthly["mes_ano"].astype(str), df_monthly["chuva_mm"], color="skyblue", alpha=0.6, label="Chuva (mm)")
    ax1.set_xlabel("Mês/Ano")
    ax1.set_ylabel("Chuva (mm)", color="skyblue")
    ax1.tick_params(axis='y', labelcolor="skyblue")

    ax2 = ax1.twinx()
    ax2.plot(df_monthly["mes_ano"].astype(str), df_monthly["temp_c"], color="orange", marker="o", label="Temperatura (°C)")
    ax2.plot(df_monthly["mes_ano"].astype(str), df_monthly["umidade"], color="blue", marker="o", label="Umidade (%)")
    ax2.set_ylabel("Temperatura/Umidade", color="black")

    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.legend(loc="upper right")
    plt.title("Resumo mensal")
    plt.show()
else:
    print("Saindo...")