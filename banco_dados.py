from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
from sqlalchemy import create_engine, text
import mysql.connector
import traceback
from sqlalchemy.exc import SQLAlchemyError
import time
import os
import zipfile  

chromedriver = r"src\chromedriver.exe"
link1 = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
link2 = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"
diretorio = r"C:\teste_nivelamento_institutecare\arquivos"

def descompactar_arquivos():
    """Função simples para descompactar todos os ZIPs no diretório"""
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".zip"):
            caminho_zip = os.path.join(diretorio, arquivo)
            with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                zip_ref.extractall(diretorio)  # Extrai no mesmo diretório
            print(f'Arquivo {arquivo} descompactado com sucesso!')
def down_rep():
    try:
        chrome_options = Options()
        prefs = {
            "download.default_directory": diretorio,
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True
        }
        chrome_options.add_experimental_option("prefs", prefs)

        service = Service(chromedriver)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Parte do download (mantida igual)
        driver.get(link1)
        driver.maximize_window()

        demo2023_XPATH = '/html/body/table/tbody/tr[20]/td[2]/a'
        arq_btn1 = driver.find_element(By.XPATH, demo2023_XPATH)
        arq_btn1.click()

        for trimestre in ["1T2023.zip", "2T2023.zip", "3T2023.zip", "4T2023.zip"]:
            demo_cont = driver.find_element(By.XPATH, f'//a[text()="{trimestre}"]')
            demo_cont.click()

        driver.back()

        demo2024_XPATH = '/html/body/table/tbody/tr[21]/td[2]/a'
        arq_btn2 = driver.find_element(By.XPATH, demo2024_XPATH)
        arq_btn2.click()

        for trimestre in ["1T2024.zip", "2T2024.zip", "3T2024.zip", "4T2024.zip"]:
            demo_cont = driver.find_element(By.XPATH, f'//a[text()="{trimestre}"]')
            demo_cont.click()

        driver.get(link2)
        driver.maximize_window()

        cad_op = driver.find_element(By.XPATH, '//a[contains(text(), "Relatorio_cadop.csv")]')
        cad_op.click()

        time.sleep(8)
        driver.quit()

        # Nova etapa: Descompactar após o download
        descompactar_arquivos()

    except Exception as e:
        print(f'Ocorreu um erro: {e.__class__.__name__}: {e}')
# def processar_dados():
#     try:
#         # Configurar conexão com o MySQL
#         engine = create_engine('mysql+mysqlconnector://root:root@localhost/contabilidade_ans')
        
#         # Criar banco se não existir
#         with engine.connect() as conn:
#             conn.execute(text("CREATE DATABASE IF NOT EXISTS contabilidade_ans"))
#             conn.execute(text("USE contabilidade_ans"))

#         # Processar operadoras (Relatorio_cadop.csv)
#         operadoras_path = os.path.join(diretorio, 'Relatorio_cadop.csv')
#         df_operadoras = None

#         try:
#             # Verificar e ler arquivo
#             if not os.path.exists(operadoras_path):
#                 raise FileNotFoundError(f"Arquivo {operadoras_path} não encontrado")
            
#             # Ler CSV com tratamento de encoding
#             df_operadoras = pd.read_csv(
#                 operadoras_path,
#                 sep=';',
#                 encoding='ISO-8859-1',
#                 on_bad_lines='skip',
#                 dtype={'CNPJ': str, 'CEP': str}
#             )

#             # Normalizar nomes das colunas
#             df_operadoras.columns = (
#                 df_operadoras.columns
#                 .str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
#                 .str.lower()
#                 .str.replace(' ', '_')
#             )

#             # Renomear colunas para corresponder ao banco de dados
#             df_operadoras = df_operadoras.rename(columns={
#                 'data_registro_ans': 'data_registro_ans'  # Nome correto da coluna
#             })

#             # Verificar colunas obrigatórias
#             required_columns = {'registro_ans', 'cnpj', 'razao_social', 'nome_fantasia', 'modalidade', 'cargo_representante'}
#             missing = required_columns - set(df_operadoras.columns)
            
#             if missing:
#                 raise KeyError(f"""
#                 COLUNAS FALTANDO: {missing}
#                 COLUNAS DISPONÍVEIS: {list(df_operadoras.columns)}
#                 """)

#         except Exception as e:
#             print(f"ERRO NO ARQUIVO DE OPERADORAS: {str(e)}")
#             traceback.print_exc()
#             return

#         # Preencher tabelas normalizadas
#         with engine.begin() as conn:
#             # Inserir modalidades
#             modalidades = df_operadoras['modalidade'].dropna().unique()
#             for m in modalidades:
#                 conn.execute(
#                     text("INSERT IGNORE INTO modalidades (nome) VALUES (:nome)"),
#                     {'nome': str(m)[:100]}
#                 )
            
#             # Inserir cargos
#             cargos = df_operadoras['cargo_representante'].dropna().unique()
#             for c in cargos:
#                 conn.execute(
#                     text("INSERT IGNORE INTO cargos (nome) VALUES (:nome)"),
#                     {'nome': str(c)[:100]}
#                 )

#         # Processar tabela principal de operadoras
#         with engine.connect() as conn:
#             # Obter mapeamento de IDs
#             modalidades_map = pd.read_sql('SELECT id, nome FROM modalidades', conn)
#             cargos_map = pd.read_sql('SELECT id, nome FROM cargos', conn)

#             # Juntar dados
#             df_operadoras = df_operadoras.merge(
#                 modalidades_map, 
#                 left_on='modalidade', 
#                 right_on='nome'
#             ).merge(
#                 cargos_map,
#                 left_on='cargo_representante',
#                 right_on='nome'
#             )

#             # Selecionar colunas para inserção (COM NOME CORRETO DA COLUNA)
#             df_to_insert = df_operadoras[[
#                 'registro_ans', 'cnpj', 'razao_social', 'nome_fantasia',
#                 'id_x', 'id_y', 'data_registro_ans'  # Nome corrigido
#             ]].rename(columns={
#                 'id_x': 'modalidade_id',
#                 'id_y': 'cargo_id'
#             })

#             # Inserir operadoras
#             df_to_insert.to_sql(
#                 'operadoras',
#                 engine,
#                 if_exists='append',
#                 index=False,
#                 chunksize=500
#             )

#         # Processar dados contábeis
#         for arquivo in os.listdir(diretorio):
#             if arquivo.endswith(".csv") and 'T20' in arquivo:
#                 caminho = os.path.join(diretorio, arquivo)
                
#                 try:
#                     # Ler e processar arquivo
#                     df_contabil = pd.read_csv(
#                         caminho,
#                         sep=';',
#                         decimal=',',
#                         thousands='.',
#                         dtype={'VL_SALDO_INICIAL': str, 'VL_SALDO_FINAL': str},
#                         parse_dates=['DATA']
#                     )

#                     # Converter valores numéricos
#                     for col in ['VL_SALDO_INICIAL', 'VL_SALDO_FINAL']:
#                         df_contabil[col] = (
#                             df_contabil[col]
#                             .str.replace('.', '', regex=False)
#                             .str.replace(',', '.', regex=False)
#                             .astype(float)
#                         )

#                     # Padronizar colunas
#                     df_contabil = df_contabil.rename(columns={
#                         'DATA': 'data',
#                         'REG_ANS': 'reg_ans',
#                         'CD_CONTA_CONTABIL': 'cd_conta_contabil',
#                         'DESCRICAO': 'descricao'
#                     })

#                     # Inserir dados
#                     df_contabil.to_sql(
#                         'saldos_contabeis',
#                         engine,
#                         if_exists='append',
#                         index=False,
#                         chunksize=1000
#                     )

#                 except Exception as e:
#                     print(f"Erro no arquivo {arquivo}: {str(e)}")
#                     continue

#         print("Processamento concluído com sucesso!")

#     except SQLAlchemyError as e:
#         print(f"ERRO DE BANCO: {str(e)}")
#         traceback.print_exc()
#     except Exception as e:
#         print(f"ERRO GERAL: {str(e)}")
#         traceback.print_exc()
#     finally:
#         if 'engine' in locals():
#             engine.dispose()


down_rep()
#processar_dados()