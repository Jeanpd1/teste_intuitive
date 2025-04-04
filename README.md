# Testes de nivelamento Intuitive Care
------------------------------------------------

## Requisitos

- [Python 3.10+](https://www.python.org/)
- [Docker](https://www.docker.com/)

---------------------------------------------------------

## Download e Compactação dos Anexos do Rol de Procedimentos da ANS (Web Scraping)

Este script (web_scraping.py) automatiza o processo de download dos Anexos I e II da página de atualização do Rol de Procedimentos e Eventos em Saúde da ANS (Agência Nacional de Saúde Suplementar), e realiza a compactação desses arquivos em um .zip.

### O que o script faz:
- Acessa automaticamente o site da ANS.
- Aceita cookies automaticamente.
- Baixa os arquivos PDF dos Anexos I e II.
- Salva os arquivos em uma pasta local definida.
- Compacta os PDFs em um único arquivo .zip.

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

----------------------------------------------------------------------

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

### Como executar esta sessão:
1. Verifique se o caminho do chromedriver está correto:
   chromedriver = r"src\chromedriver.exe" 
2. Instalar o Python 3.10+
3. Executar (Opcional): `python -m venv venv`
4. Executar: `pip install -r requirements.txt`
5. Executar na raiz do projeto o start.bat
   - Ele extrai o arquivo BD/dump_intuitivecare_bd.zip para BD/dump_intuitivecare_bd.sql
   - Obs.: Necessário para criar toda a base.
6. Executar o docker-compose na raiz do projeto: `docker-compose up -d`
   - Acesso com o Workbench MySQL ou o DBeaver e veja se as bases foram criadas e estão preenchidas
   - Obs.: Para acessar com o DBeaver, siga os passos abaixo:
     - URL: jdbc:mysql://localhost:3306?allowPublicKeyRetrieval=true&useSSL=false
     - Senha: root
7. Execute o BD\3_analises.sql, nele contém queries de análie trismestral e anual.

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

--------------------------------------------------------------

## API de Busca de Operadoras (servidor_api)
Este módulo implementa uma API REST usando Flask, permitindo realizar buscas por operadoras de saúde com base no nome fantasia, a partir de um arquivo CSV processado.

### O que o script faz:
- Carrega os dados de operadoras de um arquivo CSV previamente tratado e corrigido.
- Expõe uma rota /buscar que aceita um parâmetro q (query string) para buscar registros cujo nome fantasia contenha o termo informado.
- Retorna os resultados em formato JSON.

### Requisitos
- Python 3.8+
- Flask
- Pandas

### Como executar esta sessão:
1º Instale as bibliotecas necessárias (caso ainda não estejam instaladas).
2º Execute o script.
3º Acesse a API localmente:
   http://127.0.0.1:5000/buscar?q=amil

É possível conferir um .json com uma coleção de pesquisas feitas através do app Postman em:
   Docs\coleção_resultados_intuitivecare.postman_collection.json
   
Esse Script roda em conjunto com arquivo .vue que está na próxima seção.

-----------------------------------------------------------------------------

## Interface Web (busca_operadora.vue)
Este componente Vue.js permite realizar buscas em tempo real por operadoras de saúde, conectando-se à API Flask local.

### O que o componente faz:
- Permite digitar um termo (mínimo de 3 caracteres) para buscar operadoras.
- Exibe os resultados com nome fantasia, CNPJ, cidade e UF.
- Faz as requisições à API Flask (http://127.0.0.1:5000/buscar) conforme o usuário digita.

## Como usar:
1º Copie o componente para o diretório components do seu projeto Vue.
2º Importe e registre o componente no seu app ou página principal:
   import BuscaOperadoras from "@/components/BuscaOperadoras.vue";
3º Certifique-se de que o backend Flask esteja rodando localmente.


## Requisitos:
- Projeto Vue.js já configurado (Vue CLI ou Vite).
- Backend Flask rodando localmente com o endpoint /busca
