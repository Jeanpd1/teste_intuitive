# Teste Intuitive

## Criar ambiente [virtual](https://virtualenv.pypa.io/en/latest/user_guide.html) (isolamento)

python -m venv venv

## Executar o docker no PowerShell

- `docker run --name intuitivecare_bd -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -p 33060:33060 -v "C:\CAMINHO_COMPLETO\docker-configs\intuitivecare_bd":/var/lib/mysql -v "C:\CAMINHO_COMPLETO\arquivos":/var/lib/mysql-files/ -d mysql:latest`
- `docker exec -i intuitivecare_bd mysql -u root -proot -e "CREATE DATABASE IF NOT EXISTS bd_nivelamento_intuitiveCare;"`
- `docker exec -i intuitivecare_bd mysql -u root -proot bd_nivelamento_intuitiveCare < "C:\CAMINHO_COMPLETO\BD\bd_nivelamento_intuitiveCare.sql"`
- `Get-Content "C:\teste_nivelamento_institutecare\BD\bd_nivelamento_intuitiveCare.sql" | docker exec -i intuitivecare_bd mysql -u root -proot bd_nivelamento_intuitiveCare.sql`
- `docker exec -it intuitivecare_bd bash`

## Passos

1. PASSO 1 DOCUMENTADO AQUI
   - DETALHE 1
   - DETALHE 2
2. PASSO 2 DOCUMENTADO AQUI
   - DETALHE 1
   - DETALHE 2
3. TESTE DE BANCO DE DADOS
   - Mova os arquivos dentro de BD/arquivos
   - Execute o script testa_encodings.py, ele vai verificar o encoding e gerar o arquivo `dados_operadoras_tratados_corrigido.csv`
   - 

## Conectar com outros clientes no docker (DBeaver)

- jdbc:mysql://localhost:3306?allowPublicKeyRetrieval=true&useSSL=false


## Download e Compactação dos Anexos do Rol de Procedimentos da ANS (Web Scraping)

Este script (web_scraping.py) automatiza o processo de download dos Anexos I e II da página de atualização do Rol de Procedimentos e Eventos em Saúde da ANS (Agência Nacional de Saúde Suplementar), e realiza a compactação desses arquivos em um .zip.

### O que o script faz:
- Acessa automaticamente o site da ANS.
- Aceita cookies automaticamente.
- Baixa os arquivos PDF dos Anexos I e II.
- Salva os arquivos em uma pasta local definida.
- Compacta os PDFs em um único arquivo .zip.

### Estrutura esperada:
.
|---src/
|   |---chromedriver.exe
|---arquivos/
|   |---Anexo I.pdf
|   |---Anexo II.pdf
|   |---rol_procedimentos_eventos_saude.zip
|---script.py

### Como executar esta sessão:
1º Verifique se o caminho para o chromedriver está correto:
   chromedriver = r"src\chromedriver.exe"
2º Instale as bibliotecas necessárias (se ainda não estiverem instaladas):
3º Execute o Script

### Funções do script:
- download_anexos(chromedriver, link):
   Automatiza o acesso ao site da ANS e realiza o download dos anexos.
- compactar_anexos(download_dir, zip_nome): 
   Compacta os arquivos PDF baixados em um .zip.

### Observações importantes:
- Certifique-se de que o chromedriver seja compatível com a versão do seu navegador Chrome.
- O tempo de espera após o download (time.sleep(8)) pode ser ajustado conforme a velocidade da internet.
- Em caso de mudanças na estrutura da página da ANS, os seletores XPATH precisarão ser atualizados.

----------------

## Leitura e Processamento de PDF da ANS (Transformação de dados)

Este script (transformacao_dados.py) tem como objetivo ler e processar automaticamente o conteúdo de um arquivo PDF disponibilizado pela ANS (normalmente o Rol de Procedimentos). Ele extrai as tabelas contidas no PDF, transforma os dados em um arquivo CSV e compacta esse CSV em um arquivo ZIP.

### O que o script faz:
- Abre o PDF com tabelas utilizando pdfplumber.
- Concatena os dados de todas as páginas.
- Realiza substituições automáticas de siglas:
- Converte 'OD' em 'Seg. Odontológica'
- Converte 'AMB'em 'Seg. Ambulatorial'
- Gera um .csv temporário com os dados extraídos.
- Compacta o arquivo .csv em um .zip.
- Remove o CSV temporário ao final do processo.

### Estrutura esperada:
.
|---arquivos/
|   |-- Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf
|   |-- teste_jean_pedersoli.zip
|---transformacao_dados.py

### Como executar esta sessão:
1º Verifique se os caminhos definidos no script estão corretos:
   dir_pdf = r"C:\teste_nivelamento_institutecare\arquivos\Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
   dir_zip = r"C:\teste_nivelamento_institutecare\arquivos\teste_jean_pedersoli.zip"
 O nome do arquivo zipado pode ser alterado normalmente.
2º Instale as bibliotecas necessárias (se ainda não estiverem instaladas).
3º Execute o script.

### Funções do script:
- ler_pdf()
   Lê o PDF da ANS, extrai tabelas, realiza substituições padronizadas, salva os dados em CSV e gera um .zip com o conteúdo final.

### Observações importantes:
- O script assume que o PDF segue a estrutura padrão utilizada pela ANS.
- Caso o PDF não contenha tabelas ou o formato esteja diferente, pode ser necessário adaptar a lógica de extração.
- Os termos substituídos (OD, AMB) são apenas exemplos — podem ser ajustados conforme o conteúdo do PDF.
- O CSV final é salvo com codificação utf-8-sig, compatível com Excel.

-----------------------------------------------------------------------

## Coleta, Processamento e Correção de Dados da ANS (banco_dados.py)
Este script (banco_dados.py) realiza web scraping, tratamento de dados e correção de encoding a partir de arquivos disponibilizados pela ANS (Agência Nacional de Saúde Suplementar). Ele automatiza o download, extração, padronização e validação de dados de operadoras e demonstrações contábeis.

### O que o script faz:
- Acessa automaticamente dois diretórios públicos da ANS.
- Baixa os arquivos ZIP contendo dados trimestrais de demonstrações contábeis e o arquivo CSV das operadoras.
- Descompacta os arquivos baixados.
- Trata e filtra os dados contábeis e cadastrais, validando CNPJ e códigos.
- Corrige encoding de arquivos com problemas de leitura.
- Detecta a codificação correta dos arquivos para garantir a compatibilidade.

### Estrutura esperada:
.
|---src/
|   |---chromedriver.exe
|---BD/
|   |---arquivos_bd/
|       |---dados_operadoras_tratados.csv
|       |---dados_operadoras_corrigido.csv
|       |---dados_demonstracoes_contabeis_tratados.csv
|---arquivos/
|   |---demonstracoes_contabeis/
|   |---operadoras_ativas/
|---banco_dados.py

### Como executar esta sessão:
1º Verifique se o caminho do chromedriver está correto:
   chromedriver = r"src\chromedriver.exe"
2º Instale as bibliotecas necessárias (caso ainda não estejam instaladas).
3º Execute o script.

### Funções do script:
- baixar_e_descompactar()
   Automatiza o acesso aos diretórios da ANS, realiza o download dos arquivos ZIP e descompacta-os nas pastas de destino.
- processar_dados()
Lê os arquivos CSV de demonstrações contábeis e operadoras, realiza o tratamento dos dados (conversão de valores, validações de CNPJ e código da ANS) e salva os arquivos tratados.
- testa_corrige_enconding()
   Corrige encoding problemático do arquivo de operadoras e identifica o encoding correto do arquivo de demonstrações contábeis, testando entre utf-8, latin-1 e windows-1252.

### Observações importantes:
- Certifique-se de que a versão do Chrome instalada seja compatível com o chromedriver utilizado.
- O tempo de espera entre downloads (time.sleep(5)) pode ser ajustado conforme a velocidade da internet.
- O script já inclui tratamento de erros para lidar com ausências de arquivos ou falhas de leitura.

