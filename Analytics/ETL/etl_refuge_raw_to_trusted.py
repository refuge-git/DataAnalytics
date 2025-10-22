

# -*- coding: utf-8 -*-
"""
ETL combinado para:
1) condicao_saude.csv  -> condicao_saude_tratado.csv
2) Atendimento_mes_*.csv -> Atendimentos.csv

Uso:
    python etl_refuge_combined.py
"""
from __future__ import annotations
import csv
import glob
import os
import sys
import unicodedata
from typing import Optional, List
import pandas as pd

def remover_pontuacao(texto: Optional[str]) -> str:
    if not texto:
        return ''
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    texto = ''.join(c for c in texto if c.isalnum() or c.isspace())
    return texto.strip()

def safe_mkdir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def find_first(path_glob: str) -> Optional[str]:
    files = glob.glob(path_glob, recursive=True)
    return files[0] if files else None

def process_local_status(
    pasta_base: Optional[str] = None,
    nome_entrada: str = 'Local_status.csv',
    nome_saida: str = 'Local_status_transformado.csv',
) -> str:
    diretorio_script = os.path.dirname(os.path.abspath(__file__))

    if not pasta_base:
        pasta_base = os.path.join(diretorio_script.split('DataAnalytics')[0], 'DataAnalytics')

    pasta_origem = os.path.join(pasta_base, 'Analytics', 's3-refuge-analysis-raw', 'base-refuge')
    pasta_destino = os.path.join(pasta_base, 'Analytics', 's3-refuge-analysis-trusted', 'base-refuge')


    safe_mkdir(pasta_destino)

    caminho_entrada = os.path.join(pasta_origem, nome_entrada)
    caminho_saida = os.path.join(pasta_destino, nome_saida)

    if not os.path.exists(caminho_entrada):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_entrada}")

    try:
        df = pd.read_csv(caminho_entrada, sep=',')
        df.to_csv(caminho_saida, sep=';', index=False)
        print(f"✅ Local_status: arquivo convertido e salvo em\n{caminho_saida}")
        return caminho_saida
    except Exception as e:
        raise RuntimeError(f"Erro ao processar Local_status.csv: {e}")

def process_condicao_saude(
    pasta_base: Optional[str] = None,
    nome_entrada: str = 'condicao_saude.csv',
    nome_saida: str = 'condicao_saude_tratado.csv',
) -> str:
    import re

    diretorio_script = os.path.dirname(os.path.abspath(__file__))

    # Define pasta base começando a partir de DataAnalytics
    if not pasta_base:
        pasta_base = os.path.join(diretorio_script.split('DataAnalytics')[0], 'DataAnalytics')

    pasta_origem = os.path.join(pasta_base, 'Analytics', 's3-refuge-analysis-raw', 'base-refuge')
    pasta_destino = os.path.join(pasta_base, 'Analytics', 's3-refuge-analysis-trusted', 'base-refuge')

    safe_mkdir(pasta_destino)

    entrada_resolvida = os.path.join(pasta_origem, nome_entrada)
    if not os.path.exists(entrada_resolvida):
        raise FileNotFoundError(f"Arquivo não encontrado: {entrada_resolvida}")

    saida_path = os.path.join(pasta_destino, nome_saida)

    # normaliza nome de coluna p/ achar índices de forma tolerante
    def _norm_col(s: str) -> str:
        s = s or ''
        s = unicodedata.normalize('NFKD', s)
        s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
        s = s.replace('_', ' ').strip()
        s = re.sub(r'\s+', ' ', s)
        return s

    # remove “Diagnóstico de/Diagnostico de ” (com ou sem acento), case-insensitive
    rx_diag = re.compile(r'^\s*diagn[oó]stico\s+de\s+', re.IGNORECASE)

    with open(entrada_resolvida, mode='r', encoding='utf-8-sig', newline='') as infile, \
         open(saida_path, mode='w', encoding='utf-8', newline='') as outfile:

        leitor = csv.reader(infile)
        escritor = csv.writer(outfile, delimiter=';')

        try:
            cabecalho = next(leitor)
        except StopIteration:
            raise ValueError('Arquivo condicao_saude.csv está vazio.')

        norm = [_norm_col(c) for c in cabecalho]

        # acha coluna de descrição
        try:
            i_desc = norm.index('descricao')
        except ValueError:
            raise KeyError("Coluna 'descricao' não encontrada em condicao_saude.csv")

        # acha coluna de data/hora (aceita variações)
        i_data = None
        for cand in ('data registro', 'data_registro', 'datahora', 'data hora', 'data'):
            if cand in norm:
                i_data = norm.index(cand)
                break
        if i_data is None:
            raise KeyError("Coluna de data/hora não encontrada (ex.: 'data_registro').")

        # monta cabeçalho de saída:
        # - substitui DESCRICAO -> DOENCA
        # - substitui DATA_REGISTRO -> DATA ; HORA
        # - mantém as demais colunas (limpas com remover_pontuacao)
        cab_out: List[str] = []
        for idx, col in enumerate(cabecalho):
            if idx == i_desc:
                cab_out.append('DOENCA')
            elif idx == i_data:
                cab_out.extend(['DATA', 'HORA'])
            else:
                cab_out.append(remover_pontuacao(col))
        escritor.writerow(cab_out)

        # processa linhas
        for linha in leitor:
            if not linha:
                continue

            desc_raw = (linha[i_desc] if i_desc < len(linha) else '').strip()
            data_raw = (linha[i_data] if i_data < len(linha) else '').strip()

            # 1) DOENÇA: remove prefixo “Diagnóstico de ”
            doenca = rx_diag.sub('', desc_raw).strip()

            # 2) DATA/HORA: separa; se vier só data, hora fica vazia
            if ' ' in data_raw:
                data_part, hora_part = data_raw.split(' ', 1)
            else:
                data_part, hora_part = data_raw, ''

            # 3) Constrói linha de saída
            out_row: List[str] = []
            for idx, campo in enumerate(linha):
                if idx == i_desc:
                    out_row.append(doenca)
                elif idx == i_data:
                    out_row.extend([data_part, hora_part])
                else:
                    out_row.append(remover_pontuacao(campo))
            escritor.writerow(out_row)

    print(f"✅ Saúde: arquivo tratado (DOENCA + DATA/HORA) salvo em\n{saida_path}")
    return saida_path


def process_atendimentos(
    pasta_base: Optional[str] = None,
    padrao_entrada: str = 'Atendimento_mes_*.csv',
) -> str:
    diretorio_script = os.path.dirname(os.path.abspath(__file__))

    if not pasta_base:
        pasta_base = os.path.join(diretorio_script.split('DataAnalytics')[0], 'DataAnalytics')

    pasta_origem = os.path.join(pasta_base, 'Analytics', 's3-refuge-analysis-raw', 'base-refuge')
    pasta_destino = os.path.join(pasta_base, 'Analytics', 's3-refuge-analysis-trusted', 'base-refuge')

    safe_mkdir(pasta_destino)

    caminho_glob = os.path.join(pasta_origem, padrao_entrada)
    arquivos = glob.glob(caminho_glob)

    print(f"{len(arquivos)} arquivo(s) de atendimento encontrado(s) em: {pasta_origem}")
    for arq in arquivos:
        print(" -", os.path.basename(arq))

    if not arquivos:
        raise FileNotFoundError(f"Nenhum CSV encontrado no caminho: {caminho_glob}")

    dfs = []
    for arquivo in arquivos:
        try:
            df = pd.read_csv(arquivo, sep=None, engine='python')
            dfs.append(df)
        except Exception as e:
            print(f"Erro ao ler {arquivo}: {e}")

    if not dfs:
        raise RuntimeError('Falha ao ler todos os arquivos de atendimento.')

    df_total = pd.concat(dfs, ignore_index=True)

    if 'data_hora' in df_total.columns:
        df_total['data_hora'] = df_total['data_hora'].astype(str).str.replace('"', '', regex=False)
        df_total[['DATA', 'HORA']] = df_total['data_hora'].str.split(' ', expand=True)
    else:
        raise KeyError("A coluna 'data_hora' não foi encontrada nos arquivos CSV.")

    col_tipo = None
    for c in df_total.columns:
        if 'tipo' in c.lower():
            col_tipo = c
            break
    if not col_tipo:
        raise KeyError("Nenhuma coluna referente a 'tipo' foi encontrada nos arquivos CSV.")

    # Apenas copia o valor original da coluna tipo para ATENDIMENTO
    df_total['ATENDIMENTO'] = df_total[col_tipo].astype(str).str.strip()

    df_total.drop(columns=[col for col in ['data_hora', col_tipo] if col in df_total.columns], inplace=True, errors='ignore')

    df_total.rename(columns={
        'id_registro_atendimento': 'ID_REGISTRO_ATENDIMENTO',
        'fk_beneficiario': 'ID_BENEFICIARIO'
    }, inplace=True)

    colunas = ['ID_REGISTRO_ATENDIMENTO', 'ID_BENEFICIARIO', 'ATENDIMENTO', 'DATA', 'HORA']
    colunas_existentes = [c for c in colunas if c in df_total.columns]
    df_total = df_total[colunas_existentes]

    df_total = df_total[df_total['ATENDIMENTO'].notna() & (df_total['ATENDIMENTO'] != '')]
    if {'DATA', 'HORA'}.issubset(df_total.columns):
        df_total = df_total.sort_values(by=['DATA', 'HORA'])

    caminho_saida = os.path.join(pasta_destino, 'Atendimentos.csv')
    df_total.to_csv(caminho_saida, index=False, sep=';')

    print(f"✅ Atendimentos: arquivo final salvo em\n{caminho_saida}")
    print(f"Total de linhas: {len(df_total)}")
    return caminho_saida


def main():
    saida_saude = process_condicao_saude()
    saida_atend = process_atendimentos()
    saida_local = process_local_status()

    print('\n=== RESUMO ===')
    print('Saúde  ->', saida_saude)
    print('Atend. ->', saida_atend)
    print('Local  ->', saida_local)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('\n❌ Falha na execução:', e)
        sys.exit(1)