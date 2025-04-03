import pandas as pd
import glob
import csv
from datetime import datetime

def processar_dados():
    try:
        # 1. Processar Demonstrações Contábeis
        arquivos_contabeis = glob.glob('./arquivos/demonstracoes_contabeis/*.csv')
        if arquivos_contabeis:
            dfs = [pd.read_csv(arq, sep=';', dtype='string', encoding='utf-8-sig') for arq in arquivos_contabeis]
            df_contabil = pd.concat(dfs)
            
            # Tratamentos adicionados
            df_contabil = df_contabil.apply(lambda x: x.str.strip() if x.dtype == "string" else x)
            
            df_contabil['REG_ANS'] = (
                df_contabil['REG_ANS']
                .str.replace(r'\D', '', regex=True)
                .str[:6]
                .str.zfill(6)
            )
            
            # Conversão numérica segura
            for col in ['VL_SALDO_INICIAL', 'VL_SALDO_FINAL']:
                df_contabil[col] = (
                    df_contabil[col]
                    .str.replace(r'[^\d,]', '', regex=True)
                    .str.replace(',', '.', regex=False)
                    .astype(float)
                )
            
            # Filtro reforçado
            df_contabil = df_contabil[
                df_contabil['REG_ANS'].str.match(r'^\d{6}$') &
                df_contabil['CD_CONTA_CONTABIL'].str.match(r'^\d{8}$')
            ]
            
            df_contabil.to_csv('./arquivos/demonstracoes_contabeis/dados_demonstracoes_contabeis_tratados.csv', 
                              sep=';', index=False, encoding='utf-8')
            print('Dados contábeis salvos!')

        # 2. Processar Operadoras
        try:
            df_operadoras = pd.read_csv(
                './arquivos/operadoras_ativas/Relatorio_cadop.csv',
                sep=';',
                dtype='string',
                encoding='latin-1'
            )
            
            # Padronização de colunas
            df_operadoras.columns = df_operadoras.columns.str.strip().str.lower().str.replace(' ', '_')
            
            # Tratamento do CNPJ
            df_operadoras['cnpj'] = (
                df_operadoras['cnpj']
                .str.replace(r'\D', '', regex=True)
                .str[:14]
                .str.zfill(14)
            )
            
            # Tratamento do registro_ans
            df_operadoras['registro_ans'] = (
                df_operadoras['registro_ans']
                .str.replace(r'\D', '', regex=True)
                .str[:6]
                .str.zfill(6)
            )
            
            # Tratamento de datas (novo)
            if 'data_registro_ans' in df_operadoras.columns:
                df_operadoras['data_registro_ans'] = (
                    pd.to_datetime(
                        df_operadoras['data_registro_ans'], 
                        errors='coerce',
                        format='mixed'
                    )
                    .dt.strftime('%Y-%m-%d')
                )
                df_operadoras = df_operadoras.dropna(subset=['data_registro_ans'])
            
            # Filtro final
            df_operadoras = df_operadoras[
                df_operadoras['registro_ans'].str.match(r'^\d{6}$') &
                df_operadoras['cnpj'].str.match(r'^\d{14}$')
            ]
            
            df_operadoras.to_csv(
                './arquivos/operadoras_ativas/dados_operadoras_tratados.csv',
                sep=';',
                index=False,
                encoding='utf-8',
                date_format='%Y-%m-%d'
            )
            print('Dados das operadoras salvos!')
            
        except FileNotFoundError:
            print('Arquivo de operadoras não encontrado!')
        except KeyError as e:
            print(f'Coluna não encontrada: {str(e)}')

    except Exception as e:
        print(f'Ocorreu um erro: {str(e)}')


processar_dados()