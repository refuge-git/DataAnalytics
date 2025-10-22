# -*- coding: utf-8 -*-
"""
ETL para tratar resumo_total.csv:
- Separa dia em ano, mês e dia
- Adiciona coluna de estação com base na data
- Salva em: Analytics/s3-refuge-analysis-client/base-meteorologia/resumo_total_estacoes.csv
"""

import os
import pandas as pd

# Caminhos
HERE = os.path.dirname(os.path.abspath(__file__))
DA_ROOT = os.path.join(HERE.split("DataAnalytics")[0], "DataAnalytics")
TRUSTED_DIR = os.path.join(DA_ROOT, "Analytics", "s3-refuge-analysis-trusted", "base-meteorologia")
CLIENT_DIR = os.path.join(DA_ROOT, "Analytics", "s3-refuge-analysis-client", "base-meteorologia")
os.makedirs(CLIENT_DIR, exist_ok=True)

INPUT_FILE = os.path.join(TRUSTED_DIR, "resumo_total.csv")
OUTPUT_FILE = os.path.join(CLIENT_DIR, "resumo_total_estacoes.csv")

# Função de classificação de estação
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

# Execução
def main():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Arquivo não encontrado: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE, sep=";", encoding="utf-8-sig")

    if "dia" not in df.columns:
        raise KeyError("Coluna 'dia' não encontrada no arquivo.")

    df["dia"] = pd.to_datetime(df["dia"], errors="coerce")
    df["ano"] = df["dia"].dt.year
    df["mes"] = df["dia"].dt.month
    df["dia_num"] = df["dia"].dt.day
    df["estacao"] = df["dia"].apply(classificar_estacao)

    df.to_csv(OUTPUT_FILE, index=False, sep=";", encoding="utf-8-sig")
    print(f"✅ Arquivo tratado salvo em:\n{OUTPUT_FILE}\nLinhas: {len(df):,}")

if __name__ == "__main__":
    main()
