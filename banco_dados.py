# Importação das bibliotecas
import pdfplumber
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
import glob
import time
import os
import zipfile


# Definição de funções
def baixar_e_descompactar():
    '''
    A função baixa arquivos dos links usando Selenium com o Chrome, 
    realiza os cliques necessários para iniciar os downloads, em seguida, 
    descompacta todos os arquivos ZIP encontrados nas pastas de destino,
    tratando possíveis erros durante o processo.
    '''
    try:
        for link, config in diretorios.items():
            # Configura o Chrome
            chrome_options = Options()
            chrome_options.add_experimental_option("prefs", {
                "download.default_directory": config["pasta"],
                "download.prompt_for_download": False
            })
            
            driver = webdriver.Chrome(
                service=Service(chromedriver),
                options=chrome_options
            )
            driver.get(config["url"])
            driver.maximize_window()
            
            # Download dos arquivos específicos
            if link == "link1":
                # Ano 2023
                driver.find_element(By.XPATH, '/html/body/table/tbody/tr[20]/td[2]/a').click()
                for trimestre in ["1T2023.zip", "2T2023.zip", "3T2023.zip", "4T2023.zip"]:
                    driver.find_element(By.XPATH, f'//a[text()="{trimestre}"]').click()
                driver.back()
                
                # Ano 2024
                driver.find_element(By.XPATH, '/html/body/table/tbody/tr[21]/td[2]/a').click()
                for trimestre in ["1T2024.zip", "2T2024.zip", "3T2024.zip", "4T2024.zip"]:
                    driver.find_element(By.XPATH, f'//a[text()="{trimestre}"]').click()
            
            elif link == "link2":
                driver.find_element(By.XPATH, '//a[contains(text(), "Relatorio_cadop.csv")]').click()
            
            # Espera e fecha
            time.sleep(5)
            driver.quit()
            
            # Descompacta arquivos ZIP
            for arquivo in os.listdir(config["pasta"]):
                if arquivo.endswith(".zip"):
                    with zipfile.ZipFile(os.path.join(config["pasta"], arquivo), 'r') as zip_ref:
                        zip_ref.extractall(config["pasta"])
                    print(f'Arquivo {arquivo} descompactado em {config["pasta"]}!')
                    
    except Exception as e:
        print(f"Erro: {str(e)}")


def processar_dados():
    '''
    Processa e trata os dados baixados, unifica arquivos CSV de demonstrações contábeis, 
    convertendo valores numéricos, validando formatos de dados e salvando os resultados
    tratados em novos arquivos. Emite mensagens sobre o progresso e lida com erros como
    arquivos ausentes ou problemas inesperados.
    '''
    try:
        # Processa o arquivo de Demonstrações Contábeis
        arquivos_contabeis = glob.glob('./arquivos/demonstracoes_contabeis/*.csv')
        if arquivos_contabeis:
            # Lê e junta arquivos
            dfs = [pd.read_csv(arq, sep=';', dtype='string') for arq in arquivos_contabeis]
            df_contabil = pd.concat(dfs)
            
            # Converte os valores numéricos
            for col in ['VL_SALDO_INICIAL', 'VL_SALDO_FINAL']:
                df_contabil[col] = df_contabil[col].str.replace('.', '').str.replace(',', '.').astype(float)
            
            # Filtra os dados válidos
            df_contabil = df_contabil[
                df_contabil['REG_ANS'].str.match(r'^\d{6}$') &
                df_contabil['CD_CONTA_CONTABIL'].str.match(r'^\d{8}$')
            ]
            
            df_contabil.to_csv('BD/arquivos_bd/dados_demonstracoes_contabeis_tratados.csv', 
                               sep=';', index=False)
            print('Dados contabeis salvos!')

        # Processa o arquivo de Operadoras
        try:
            df_operadoras = pd.read_csv(
                './arquivos/operadoras_ativas/Relatorio_cadop.csv',
                sep=';',
                dtype='string'
            )
            
            # Limpa e valida a coluna cnpj
            df_operadoras['CNPJ'] = df_operadoras['CNPJ'].str.replace(r'\D', '', regex=True)
            df_operadoras = df_operadoras[
                df_operadoras['Registro_ANS'].str.match(r'^\d{6}$') &
                df_operadoras['CNPJ'].str.match(r'^\d{14}$')
            ]
            
            df_operadoras.to_csv('BD/arquivos_bd/dados_operadoras_tratados.csv', sep=';', index=False)
            print('Dados das operadoras salvos!')
            
        except FileNotFoundError:
            print('Arquivo de operadoras não encontrado!')

    except Exception as e:
        print(f'Ocorreu um erro: {str(e)}')


def testa_corrige_enconding():
    try:        
        print('Correção do arquivo dados_operadoras_tratados para tratar o encoding:')
        with open("BD/arquivos_bd/dados_operadoras_tratados.csv", 'r', encoding='latin-1') as f:
            with open('BD/arquivos_bd/dados_operadoras_corrigido.csv', 'w', encoding='utf-8') as fw:
                texto_errado = f.read()
                texto_correto = texto_errado.encode('latin-1').decode('utf-8')
                fw.write(texto_correto)

        print('Identifica o encoding correto:')
        encodings = ['utf-8', 'latin-1', 'windows-1252']
        path = 'BD/arquivos_bd/dados_demonstracoes_contabeis_tratados.csv'
        for enc in encodings:
            try:
                with open(path, 'r', encoding=enc) as f:
                    f.read()
                    print(f"Encoding do arquivo {path} correto: {enc}")
                    break
            except UnicodeDecodeError:
                continue
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")


# Variáveis
chromedriver = r"src\chromedriver.exe"
diretorios = {
    "link1": {
        "url": "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/",
        "pasta": r"C:\teste_nivelamento_institutecare\arquivos\demonstracoes_contabeis"
    },
    "link2": {
        "url": "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/",
        "pasta": r"C:\teste_nivelamento_institutecare\arquivos\operadoras_ativas"
    }
}

# Execução
if __name__ == "__main__":
    # baixar_e_descompactar()
    # processar_dados()
    testa_corrige_enconding()
    