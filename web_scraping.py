# Importação das bibliotecas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os
import zipfile

# Definição de funções
def download_anexos(chromedriver, link):   
    '''   
    Automatiza o download dos anexos I e II da página de atualização do Rol de Procedimentos da ANS.
    Configura um diretório específico para salvar os arquivos PDF, aceita cookies automaticamente e utiliza 
    seletores XPATH para localizar e baixar os documentos. Requer ChromeDriver compatível com a versão do 
    navegador e as bibliotecas Selenium, webdriver-manager e time. Trata exceções durante a execução 
    para garantir robustez.
    '''
   
    try:
            
        # Configurações do Chrome para download automático
        chrome_options = Options()
        prefs = {
            "download.default_directory": r"C:\teste_nivelamento_institutecare\arquivos",  # Diretório de download
            "download.prompt_for_download": False,               # Desativa pop-ups
            "plugins.always_open_pdf_externally": True           # Força o download de PDFs diretamente
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # Inicializa o WebDriver com as configurações
        service = Service(chromedriver)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Abre o site desejado
        driver.get(link)

        # Maximiza a janela do navegador
        driver.maximize_window()

        # Aceita os cookies
        accept_cookies_XPATH = '//button[text()="Aceitar cookies"]'
        cookie_btn = driver.find_element(By.XPATH, accept_cookies_XPATH)
        cookie_btn.click()

        # Localiza o link do arquivo e baixa
        anexo_1 = driver.find_element(By.XPATH, '//a[text()="Anexo I."]')
        anexo_1.click()

        anexo_2 = driver.find_element(By.XPATH, '//a[text()="Anexo II."]')
        anexo_2.click()

        time.sleep(8) # Dependendo da banda de internet, alterar para o browser não fechar antes do download

        # Fecha o navegador
        driver.quit()

    except Exception as e:
        print(f'Ocorreu um erro: {e.__class__.__name__}')
def compactar_anexos(download_dir, zip_nome):
    try:
        # Cria diretório para o ZIP se não existir
        os.makedirs(os.path.dirname(zip_nome), exist_ok=True)
        
        # Lista todos os PDFs baixados
        arquivos = [os.path.join(download_dir, f) for f in os.listdir(download_dir) 
                   if f.endswith('.pdf')]

        with zipfile.ZipFile(zip_nome, "w", zipfile.ZIP_DEFLATED) as zipf:
            for arquivo in arquivos:
                # Adiciona mantendo estrutura de pastas relativa
                arcname = os.path.basename(arquivo)
                zipf.write(arquivo, arcname=arcname)
        
        print(f"Arquivo ZIP criado: {zip_nome}")
        print(f"Arquivos compactados: {len(arquivos)}")

    except Exception as e:
        print(f"Erro na compactação: {str(e)}")

# Variáveis 
chromedriver = r"src\chromedriver.exe"
link = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
diretorio = r"C:\teste_nivelamento_institutecare\arquivos"  # Diretório de downloads
zip_nome = r"C:\teste_nivelamento_institutecare\arquivos\rol_procedimentos_eventos_saude.zip"

# Execução
download_anexos(chromedriver, link)
compactar_anexos(diretorio, zip_nome)
