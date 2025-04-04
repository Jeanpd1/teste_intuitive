import os

encodings = ['utf-8', 'latin-1', 'windows-1252']
print('Correção do arquivo dados_operadoras_tratados para tratar o encoding:')
for enc in encodings:
    try:
        with open("/scripts/dados_operadoras_tratados.csv", 'r', encoding=enc) as f:
            with open('/scripts/dados_operadoras_tratados_corrigido.csv', 'w', encoding='utf-8') as fw:
                texto_errado = f.read()
                texto_correto = texto_errado.encode('latin-1').decode('utf-8')
                fw.write(texto_correto)
        break
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")

print('Identifica o encoding correto:')
path = '/scripts/dados_demonstracoes_contabeis_tratados.csv'
for enc in encodings:
    try:
        with open(path, 'r', encoding=enc) as f:
            f.read()
            print(f"Encoding do arquivo {path} correto: {enc}")
            break
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")
