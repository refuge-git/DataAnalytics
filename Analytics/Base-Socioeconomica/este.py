import pandas as pd
import unicodedata

# Caminho do arquivo de entrada e saída
input_path = "Base de dados - Socioeconomica.xlsx"
output_path = "base_socioeconomica.csv"

# Função para remover acentuação e ç
def remover_acentos(texto):
    if isinstance(texto, str):
        texto = unicodedata.normalize('NFD', texto)
        texto = texto.encode('ascii', 'ignore').decode('utf-8')
        return texto.replace('ç', 'c').replace('Ç', 'C')
    return texto

# Ler planilha Excel (primeira aba)
df = pd.read_excel(input_path)

# Renomear colunas específicas
df = df.rename(columns={
    "Q4": "idade",
    "Q5": "raca_cor",
    "Q6": "sexo",
    "Q7": "orientacao_sexual"
})

# Remover acentos dos nomes das colunas
df.columns = [remover_acentos(col) for col in df.columns]

# Remover acentos do conteúdo das células (para colunas de texto)
df = df.applymap(remover_acentos)

# Salvar como CSV
df.to_csv(output_path, index=False, encoding='utf-8', sep=';')

print(f"Arquivo gerado com sucesso: {output_path}")
