import pandas as pd
import boto3
import io

# Configurações dos buckets e caminhos
s3 = boto3.client('s3')
bucket_trusted = 's3-refuge-analysis-trusted'
bucket_client = 's3-refuge-analysis-client'
folder = 'base-socioeconomica/'
arquivo_csv_trusted = folder + 'base_socieconomica_tratada.csv'
arquivo_csv_client = folder + 'base_socieconomica_tratada_v2.csv'

# Leitura do CSV tratado do bucket trusted
obj = s3.get_object(Bucket=bucket_trusted, Key=arquivo_csv_trusted)
csv_bytes = obj['Body'].read()
csv_buffer = io.StringIO(csv_bytes.decode('utf-8'))
df = pd.read_csv(csv_buffer)

# Seleciona e renomeia colunas
df = df[['Q4', 'Q5', 'Q6', 'Q7', 'Q8']].rename(columns={
    'Q4': 'idade',
    'Q5': 'raca_cor',
    'Q6': 'sexo',
    'Q7': 'identidade_genero',
    'Q8': 'orientacao_sexual'
})

# Substitui siglas NS e NR
df['identidade_genero'] = df['identidade_genero'].replace({'NS': 'Nao se Aplica', 'NR': 'Nao Relatado'})
df['orientacao_sexual'] = df['orientacao_sexual'].replace({'NS': 'Nao se Aplica', 'NR': 'Nao Relatado'})

# Adiciona coluna de id crescente
df.insert(0, 'id', range(1, len(df) + 1))

# Exporta como CSV para memória
csv_final_buffer = io.StringIO()
df.to_csv(csv_final_buffer, index=False)

# Envia para bucket client
s3.put_object(Bucket=bucket_client, Key=arquivo_csv_client, Body=csv_final_buffer.getvalue())

print("✅")