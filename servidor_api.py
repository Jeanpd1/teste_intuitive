# Importação das bibliotecas
from flask import Flask, request, jsonify
import pandas as pd

# Definição da função
def create_app(csv_path: str) -> Flask:
    """
    Cria e configura a aplicação Flask para busca de operadoras.
    Argumentos: csv_path (str): Caminho para o arquivo CSV contendo os dados das operadoras.
    Retornos: Instância da aplicação Flask configurada.
    """
    app = Flask(__name__)

    try:
        df = pd.read_csv(csv_path, sep=None, engine="python", encoding="utf-8") # Carregar o CSV corretamente        
        df.columns = df.columns.str.strip().str.lower() # Corrigir nomes de colunas e garantir consistência        
        coluna_busca = "nome_fantasia"  # Usar a coluna correta para busca
        df[coluna_busca] = df[coluna_busca].astype(str).str.lower()
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar ou processar o CSV: {e}")

    @app.route("/buscar", methods=["GET"])
    def buscar_operadora():
        """
        Rota para buscar operadoras pelo nome fantasia.
        Parâmetros:q (str): Termo de busca enviado como query parameter.
        Retorna:JSON: Lista de registros que contêm o termo buscado.
        """
        try:
            termo = request.args.get("q", "").strip().lower()
            if not termo:
                return jsonify({"erro": "Parâmetro 'q' é obrigatório"}), 400

            resultados = df[df[coluna_busca].str.contains(termo, na=False, case=False)]
            return jsonify(resultados.to_dict(orient="records"))
        except Exception as e:
            return jsonify({"erro": f"Erro ao processar a requisição: {str(e)}"}), 500

    return app

# Variável
CSV_PATH = "BD/arquivos/dados_operadoras_tratados_corrigido.csv"

# Execução
if __name__ == "__main__":
    app = create_app(CSV_PATH)
    app.run(debug=True)
