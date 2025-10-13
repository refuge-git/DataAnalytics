import pandas as pd

# Carregar o arquivo e as colunas de interesse
file_path = "Base de dados - Socioeconomica.xlsx"
df = pd.read_excel(file_path, usecols=["Q4", "Q5", "Q6", "Q7"])

# Renomear colunas para facilitar
df = df.rename(columns={
    "Q4": "idade",
    "Q5": "raca_cor_etnia",
    "Q6": "sexo",
    "Q7": "identidade_genero"
})

# Garantir que idade é numérica
df["idade"] = pd.to_numeric(df["idade"], errors="coerce")

# Faixas etárias por sexo
faixas = [
    (18, 29, "18-29"),
    (30, 59, "30-59"),
    (60, 200, "60+")
]

def contar_faixa_etaria(df, sexo):
    resultados = {}
    for inicio, fim, label in faixas:
        count = df[(df["sexo"].str.lower() == sexo) & (df["idade"] >= inicio) & (df["idade"] <= fim)].shape[0]
        resultados[label] = count
    resultados["total"] = df[df["sexo"].str.lower() == sexo].shape[0]
    return resultados

masculino = contar_faixa_etaria(df, "masculino")
feminino = contar_faixa_etaria(df, "feminino")

# Raça/cor/etnia por sexo
racas = ["branca", "preta", "parda", "amarela", "indígena"]

def contar_raca_por_sexo(df, sexo):
    resultados = {}
    for raca in racas:
        count = df[(df["sexo"].str.lower() == sexo) & (df["raca_cor_etnia"].str.lower() == raca)].shape[0]
        resultados[raca] = count
    # Contar não informados
    nao_informados = df[
        (df["sexo"].str.lower() == sexo) &
        (df["raca_cor_etnia"].str.lower().isin([
            "não declarou", "não informada", "não respondeu", "prefere não declarar", "ns", "não se aplica"
        ]))
    ].shape[0]
    resultados["não declarado"] = nao_informados
    return resultados

raca_feminino = contar_raca_por_sexo(df, "feminino")
raca_masculino = contar_raca_por_sexo(df, "masculino")

# Identidade de gênero
generos = {
    "cisgênero": ["homem cisgênero", "mulher cisgênero", "homem cisgenero", "mulher cisgenero"],
    "transgênero": ["homem trans", "mulher trans", "transgênero", "transgenero"],
    "agênero": ["agênero", "agenero"],
    "não declarado": ["ns", "não declarou", "não informada", "não respondeu", "prefere não declarar"]
}

def contar_genero(df):
    resultados = {}
    for gen, variantes in generos.items():
        count = df[df["identidade_genero"].str.lower().isin([v.lower() for v in variantes])].shape[0]
        resultados[gen] = count
    return resultados

genero_counts = contar_genero(df)

# Salvar os resultados em um arquivo Excel com abas separadas
with pd.ExcelWriter("insights_socioeconomicos.xlsx") as writer:
    # Faixas etárias
    faixa_df = pd.DataFrame([masculino, feminino], index=["Masculino", "Feminino"])
    faixa_df.to_excel(writer, sheet_name="Faixas Etárias")
    # Raça/cor/etnia
    raca_df = pd.DataFrame([raca_masculino, raca_feminino], index=["Masculino", "Feminino"])
    raca_df.to_excel(writer, sheet_name="Raça Cor Etnia")
    # Identidade de gênero
    genero_df = pd.DataFrame([genero_counts])
    genero_df.to_excel(writer, sheet_name="Identidade de Gênero")

print("Arquivo gerado!")