from flask import Flask, request, jsonify
import phonenumbers

app = Flask(__name__)

@app.route('/api/valida_telefone_latam', methods=['POST'])
def valida_telefone():
    dados = request.get_json()
    telefone = dados['telefone']

    if not telefone:
        response = {
            'Erro': 'Por favor, preencha o campo telefone com um número válido.'
        }
        return jsonify(response), 400

    if '+' not in telefone:
        telefone = f'+{telefone}'

    try:
        parsed_number = phonenumbers.parse(telefone, None)
        is_valid = phonenumbers.is_valid_number(parsed_number)
        region_code = phonenumbers.region_code_for_number(parsed_number)

        if is_valid and region_code in ('AR', 'BO', 'BR', 'CL', 'CO', 'CR', 'CU', 'DO', 'EC', 'GT', 'HN', 'MX', 'NI', 'PA', 'PY', 'PE', 'PR', 'UY', 'VE'):
            response = {
                'valid': True,
                'regiao': region_code
            }
            return jsonify(response), 200
        else:
            response = {
                'valid': False,
                'regiao': 'Desconhecida'
            }
            return jsonify(response), 200

    except phonenumbers.phonenumberutil.NumberParseException:
        response = {
            'Erro': 'Você inseriu um número inválido!'
        }
        return jsonify(response), 400

if __name__ == '__main__':
    app.run()