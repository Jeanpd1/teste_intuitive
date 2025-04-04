# Importação das bibliotecas
import pdfplumber
import pandas as pd
import zipfile
import os

# Definição da função
def ler_pdf():
    '''
    Lê um arquivo PDF com dados da ANS, processa as tabelas internas e gera um arquivo ZIP contendo os dados em CSV. 
    Substitui automaticamente termos como 'OD' e 'AMB' por descrições completas durante o processamento. 
    Se ocorrer algum erro, limpa os arquivos temporários e exibe a mensagem de falha.
    Os caminhos do PDF e ZIP estão fixos no código, mas podem ser ajustados conforme necessidade!
    '''
    try:
        # Configurações fixas
        SUBSTITUICOES = {
            'OD': 'Seg. Odontológica',
            'AMB': 'Seg. Ambulatorial'
        }
        
        # Caminhos renomeados
        dir_pdf = r"C:\teste_nivelamento_institutecare\arquivos\Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
        dir_zip = r"C:\teste_nivelamento_institutecare\arquivos\teste_jean_pedersoli.zip"
        csv_temp = "temp.csv"

        # Extrair dados do PDF
        dados = []
        with pdfplumber.open(dir_pdf) as pdf:
            for pagina in pdf.pages:
                if tabela := pagina.extract_table():
                    dados.extend(tabela)

        # Criar DataFrame
        df = pd.DataFrame(dados[1:], columns=dados[0])

        # Substituir colunas
        for col in df.columns:
            if 'OD' in col.upper():
                df[col] = SUBSTITUICOES['OD']
            elif 'AMB' in col.upper():
                df[col] = SUBSTITUICOES['AMB']

        # Salvar e compactar
        df.to_csv(csv_temp, index=False, encoding='utf-8-sig')
        
        with zipfile.ZipFile(dir_zip, 'w') as zipf:
            zipf.write(csv_temp, 'dados_ans.csv')
            
        os.remove(csv_temp)
        print(f"Arquivo {dir_zip} criado com sucesso!")

    except Exception as e:
        print(f"Erro: {str(e)}")
        if os.path.exists(csv_temp):
            os.remove(csv_temp)


# Execução
if __name__ == '__main__':
    ler_pdf()