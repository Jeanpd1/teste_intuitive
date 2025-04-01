import pandas as pd
import numpy as np
import glob
import os

# Configurações
PASTA_ENTRADA = './arquivos/demonstracoes_contabeis/*.csv'  # Todos os CSVs na pasta
CAMINHO_SAIDA = './arquivos/demonstracoes_contabeis/dados_demonstracoes_contabeis_tratados.csv'

def processar_dados():
    # Carregar todos os arquivos CSV
    arquivos = glob.glob(PASTA_ENTRADA)
    
    if not arquivos:
        print("Nenhum arquivo CSV encontrado na pasta!")
        return

    # Ler e concatenar arquivos
    dfs = []
    for arquivo in arquivos:
        try:
            df = pd.read_csv(
                arquivo,
                sep=';',
                quotechar='"',
                thousands='.',
                decimal=',',
                parse_dates=['DATA'],
                dtype={
                    'REG_ANS': 'string',
                    'CD_CONTA_CONTABIL': 'string'
                }
            )
            dfs.append(df)
            print(f"Arquivo {os.path.basename(arquivo)} carregado: {len(df)} registros")
        except Exception as e:
            print(f"Erro no arquivo {arquivo}: {str(e)}")

    if not dfs:
        print("Nenhum dado válido para processar!")
        return

    df_consolidado = pd.concat(dfs, ignore_index=True)

    # Limpeza de espaços em brancos e dados duplicados
    df_clean = df_consolidado.dropna(how='all').drop_duplicates()

    # Converter campos numéricos
    df_clean['VL_SALDO_INICIAL'] = pd.to_numeric(df_clean['VL_SALDO_INICIAL'], errors='coerce')
    df_clean['VL_SALDO_FINAL'] = pd.to_numeric(df_clean['VL_SALDO_FINAL'], errors='coerce')

    # Normalizar texto
    df_clean['DESCRICAO'] = (
        df_clean['DESCRICAO']
        .str.strip()
        .str.upper()
        .str.normalize('NFKD')
        .str.encode('ascii', errors='ignore')
        .str.decode('utf-8')
    )

    # Validar registros
    validos = (
        df_clean['REG_ANS'].str.match(r'^\d{6}$', na=False) &
        df_clean['CD_CONTA_CONTABIL'].str.match(r'^\d{8}$', na=False) &
        df_clean['VL_SALDO_INICIAL'].between(-1000, 1000000) &
        df_clean['VL_SALDO_FINAL'].between(-1000, 1000000)
    )

    df_final = df_clean[validos].copy()

    # Preencher valores faltantes
    df_final[['VL_SALDO_INICIAL', 'VL_SALDO_FINAL']] = df_final[
        ['VL_SALDO_INICIAL', 'VL_SALDO_FINAL']
    ].fillna(0)

    # Ordenar e resetar índice
    df_final = df_final.sort_values(['REG_ANS', 'DATA']).reset_index(drop=True)

    # Exportar resultados
    try:
        df_final.to_csv(
            CAMINHO_SAIDA,
            sep=';',
            decimal=',',
            index=False,
            encoding='utf-8-sig'
        )
        print(f"\nProcessamento concluído!")
        print(f"Arquivo final salvo em: {CAMINHO_SAIDA}")
        print(f"Registros originais: {len(df_consolidado)}")
        print(f"Registros válidos: {len(df_final)}")
        print(f"Registros removidos: {len(df_consolidado) - len(df_final)}")
    except Exception as e:
        print(f"\nErro ao exportar arquivo final: {str(e)}")

if __name__ == "__main__":
    processar_dados()