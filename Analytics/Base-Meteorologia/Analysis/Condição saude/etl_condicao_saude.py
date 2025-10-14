import csv
import unicodedata
import os

def remover_pontuacao(texto):
    if not texto:
        return ''
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    texto = ''.join(c for c in texto if c.isalnum() or c.isspace())
    return texto.strip()

# Caminhos dos arquivos
entrada = r'C:\Users\biahr\OneDrive\Documentos\PROJ-REFUGE\DataAnalytics\Analytics\Base-Meteorologia\Analysis\Condição saude\condicao_saude.csv'
saida = r'C:\Users\biahr\OneDrive\Documentos\PROJ-REFUGE\DataAnalytics\Analytics\Base-Meteorologia\Analysis\Condição saude\condicao_saude_tratado.csv'

# Verifica se o arquivo existe
if not os.path.exists(entrada):
    print(f"Arquivo não encontrado:\n{entrada}")
else:
    with open(entrada, mode='r', encoding='utf-8') as infile, open(saida, mode='w', encoding='utf-8', newline='') as outfile:
        leitor = csv.reader(infile)
        escritor = csv.writer(outfile, delimiter=';')

        cabecalho = next(leitor)
        # Remove a coluna 'mes'
        cabecalho_tratado = [remover_pontuacao(col) for col in cabecalho[1:]]
        escritor.writerow(cabecalho_tratado)

        for linha in leitor:
            # Remove a coluna 'mes' (índice 0)
            dados = linha[1:]
            dados_tratados = []
            for i, campo in enumerate(dados):
                # Mantém data e hora sem alteração
                if i == 0 or i == 1:  # data, hora
                    dados_tratados.append(campo.strip())
                else:
                    dados_tratados.append(remover_pontuacao(campo))
            escritor.writerow(dados_tratados)

    print(f"Arquivo tratado salvo com sucesso em:\n{saida}")
