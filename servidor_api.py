from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Carregar o CSV
csv_path = r"arquivos\operadoras_ativas\dados_operadoras_tratados.csv"
df = pd.read_csv(csv_path, sep=";", on_bad_lines="skip", engine="python", encoding="utf-8")


# Rota de busca textual
@app.route('/api/busca', methods=['GET'])
def buscar_operadora():
    termo = request.args.get('termo', '').lower()

    if not termo:
        return jsonify({"erro": "Parâmetro 'termo' é obrigatório"}), 400

    # Filtrar registros que contenham o termo
    resultados = df[df.apply(lambda row: row.astype(str).str.contains(termo, case=False).any(), axis=1)]

    return jsonify(resultados.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)