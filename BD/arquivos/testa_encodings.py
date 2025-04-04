# Importação da biblioteca
import os

# Definição de funções
def corrige_encoding(
    entrada=os.path.join("BD", "arquivos", "dados_operadoras_tratados.csv"),
    saida=os.path.join("BD", "arquivos", "dados_operadoras_tratados_corrigido.csv")
):
    """
    Corrige problemas de encoding de um arquivo CSV.
    """
    print(f'Correção do arquivo {entrada} para tratar o encoding:')
    
    with open(entrada, 'r', encoding='utf-8') as arquivo_entrada:
        texto = arquivo_entrada.read()
        texto_corrigido = texto.encode('latin-1').decode('utf-8')
        
        with open(saida, 'w', encoding='utf-8') as arquivo_saida:
            arquivo_saida.write(texto_corrigido)
def detecta_encoding(
    caminho=os.path.join("BD", "arquivos", "dados_demonstracoes_contabeis_tratados.csv"),
    codificacoes=('utf-8', 'latin-1', 'windows-1252')
):
    """
    Identifica o encoding correto de um arquivo CSV.
    """
    print("Identifica o encoding correto:")
    
    for codificacao in codificacoes:
        try:
            with open(caminho, 'r', encoding=codificacao) as arquivo:
                arquivo.read()
                print(f"Encoding do arquivo {caminho} correto: {codificacao}")
                return
        except UnicodeDecodeError:
            continue
def principal():
    """
    Executa o fluxo principal de correção e detecção de encoding.
    """
    try:
        corrige_encoding()
        detecta_encoding()
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")

# Execução
if __name__ == "__main__":
    principal()