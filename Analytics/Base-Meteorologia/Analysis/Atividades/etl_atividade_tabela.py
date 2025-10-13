import pandas as pd
import glob

# Caminho para os arquivos de atividade
caminho = 'Analytics/Base-Meteorologia/Analysis/Atividades/Atividade_mes_*.csv'

# Lista todos os arquivos
arquivos = glob.glob(caminho)

# Lê e junta todos os arquivos
df_total = pd.concat([pd.read_csv(arquivo) for arquivo in arquivos], ignore_index=True)

# Remove aspas da coluna 'data_hora' se houver
df_total['data_hora'] = df_total['data_hora'].str.replace('"', '')

# Divide a coluna 'data_hora' em duas: 'Data' e 'Hora'
df_total[['Data', 'Hora']] = df_total['data_hora'].str.split(' ', expand=True)

# Remove a coluna original se quiser deixar mais limpo
df_total.drop(columns=['data_hora'], inplace=True)

# Reorganiza as colunas (opcional)
colunas = ['id_registro_atendimento', 'fk_beneficiario', 'tipo_nome', 'tipo_descricao', 'Data', 'Hora']
df_total = df_total[colunas]

# Exporta para CSV com separador ponto e vírgula
df_total.to_csv('Atividade_completa.csv', index=False, sep=';')
