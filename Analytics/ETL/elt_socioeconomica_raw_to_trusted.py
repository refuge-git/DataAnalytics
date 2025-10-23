import pandas as pd
import unicodedata
import boto3
import io

# Função para remover acentuação e "ç"
def limpar_texto(texto):
    if isinstance(texto, str):
        texto = texto.replace('ç', 'c').replace('Ç', 'C')
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
        texto = texto.strip()
    return texto

# Configurações dos buckets e caminhos
s3 = boto3.client('s3')
bucket_raw = 's3-refuge-analysis-raw'
bucket_trusted = 's3-refuge-analysis-trusted'
folder = 'base-socioeconomica/'
arquivo_excel = folder + 'B_Base de dados - Entrega com dicionário_xlsx.xlsx'
arquivo_csv = folder + 'base_socieconomica_tratada.csv'

# Leitura do Excel bruto (apenas a aba "Amostra")
obj = s3.get_object(Bucket=bucket_raw, Key=arquivo_excel)
excel_bytes = obj['Body'].read()
excel_buffer = io.BytesIO(excel_bytes)

# Força leitura da aba correta
df = pd.read_excel(excel_buffer, sheet_name='Amostra', engine='openpyxl')

# Limpeza de colunas e dados
df.columns = [limpar_texto(col) for col in df.columns]
df = df.applymap(limpar_texto)

# Exporta como CSV para memória
csv_buffer = io.StringIO()
df.to_csv(csv_buffer, index=False)

# Envia para bucket trusted
s3.put_object(Bucket=bucket_trusted, Key=arquivo_csv, Body=csv_buffer.getvalue())

print("✅")