from flask import Flask, request, jsonify

app = Flask(__name__)

def calcular_parcela(P, i, n):
    """
    Calcula a parcela mensal de um empréstimo com base no saldo devedor, taxa de juros e prazo.

    :param P: Saldo devedor
    :param i: Taxa de juros mensal em decimal
    :param n: Prazo em meses
    :return: Valor da parcela mensal
    """
    return (P * i) / (1 - (1 + i) ** -n)

@app.route('/calcular_parcela', methods=['POST'])
def calcular_parcela_api():
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({'error': 'Formato de dados inválido'}), 400

        saldo_devedor = data.get('saldo_devedor')
        taxa = data.get('taxa')
        prazo = data.get('prazo')

        if saldo_devedor is None or taxa is None or prazo is None:
            return jsonify({'error': 'Dados insuficientes'}), 400

        try:
            saldo_devedor = float(saldo_devedor)
            taxa = float(taxa) / 100  # Converter para decimal
            prazo = int(prazo)
        except (ValueError, TypeError):
            return jsonify({'error': 'Dados inválidos'}), 400

        parcela = calcular_parcela(saldo_devedor, taxa, prazo)
        return jsonify({'parcela_mensal': parcela})

    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
