import pandas as pd
import glob
import os

# Caminho para os arquivos CSV
caminho = 'Analytics/Base-Meteorologia/Analysis/Atendimento/Atendimento_mes_*.csv'

# Lista todos os arquivos
arquivos = glob.glob(caminho)

# Lê e junta todos os arquivos
df_total = pd.concat([pd.read_csv(arquivo) for arquivo in arquivos], ignore_index=True)

# Remove aspas da coluna 'data_hora' se houver
df_total['data_hora'] = df_total['data_hora'].str.replace('"', '')

# Divide a coluna 'data_hora' em duas: 'DATA' e 'HORA'
df_total[['DATA', 'HORA']] = df_total['data_hora'].str.split(' ', expand=True)

# Substitui os valores de fk_tipo por texto sem acento
df_total['ATENDIMENTO'] = df_total['fk_tipo'].map({1: 'Refeicao', 2: 'Banho'})

# Remove colunas que não serão usadas
df_total.drop(columns=['data_hora', 'fk_tipo'], inplace=True)

# Renomeia colunas para maiúsculas
df_total.rename(columns={
    'id_registro_atendimento': 'ID_REGISTRO_ATENDIMENTO',
    'fk_beneficiario': 'ID_BENEFICIARIO'
}, inplace=True)

# Reorganiza as colunas
colunas = ['ID_REGISTRO_ATENDIMENTO', 'ID_BENEFICIARIO', 'ATENDIMENTO', 'DATA', 'HORA']
df_total = df_total[colunas]

# Remove linhas onde ATENDIMENTO está vazio ou nulo
df_total = df_total[df_total['ATENDIMENTO'].notna() & (df_total['ATENDIMENTO'] != '')]

# Ordena pela data e hora
df_total = df_total.sort_values(by=['DATA', 'HORA'])

diretorio_script = os.path.dirname(os.path.abspath(__file__))
caminho_saida = os.path.join(diretorio_script, 'Atendimento_completo.csv')

# Exporta para CSV com separador ponto e vírgula
df_total.to_csv(caminho_saida, index=False, sep=';')
