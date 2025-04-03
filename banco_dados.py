import pandas as pd
import glob
import csv
import os
from datetime import datetime

def processar_dados():
    try:
        # =============================================
        # 1. Processar Operadoras
        # =============================================
        try:
            # Criar diretório se não existir
            os.makedirs('./arquivos/operadoras_ativas', exist_ok=True)
            
            # Carregar dados
            df_operadoras = pd.read_csv(
                './arquivos/operadoras_ativas/Relatorio_cadop.csv',
                sep=';',
                dtype='string',
                encoding='latin-1'
            )

            # ... (todo o processamento anterior mantido)

            # Caminho completo do arquivo de saída
            output_path = './arquivos/operadoras_ativas/dados_operadoras_tratados.csv'
            
            # Salvar com verificação explícita
            df_operadoras.to_csv(
                output_path,
                sep=';',
                index=False,
                encoding='utf-8',
                quoting=csv.QUOTE_MINIMAL,
                mode='w'  # Força sobrescrita
            )
            
            # Verificação pós-salvamento
            if os.path.exists(output_path):
                print(f'[SUCESSO] Arquivo salvo em: {os.path.abspath(output_path)}')
                print(f'Tamanho do arquivo: {os.path.getsize(output_path)} bytes')
            else:
                print('[ERRO] Arquivo não foi gerado!')

        except PermissionError:
            print('[ERRO] Permissão negada para salvar o arquivo!')
        except Exception as e:
            print(f'[ERRO] Falha ao salvar: {str(e)}')

    except Exception as e:
        print(f'[ERRO CRÍTICO] {str(e)}')

if __name__ == "__main__":
    processar_dados()