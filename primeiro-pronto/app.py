from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def hello_ti360():
    return jsonify({"message": "Hello TI360!"})

@app.route("/mensagens", methods=["GET"])
def ola_ti360_get():
    return jsonify({"mensagem": "Olá TI360 GET!"})

@app.route("/mensagens", methods=["POST"])
def ola_ti360_post():
    dados = request.get_json()

    print(dados['celular'])
    print(dados['email'])

    return {"message": "Cadastro realizado com sucesso!"}, 201

@app.route("/mensagens", methods=["PUT"])
def editar_mensagens():
    return jsonify({"mensagem": "Edição realizada com sucesso!"})

@app.route("/mensagens", methods=["DELETE"])
def deletar_mensagens():
    return jsonify({"mensagem": "Remoção realizada com sucesso!"})

@app.route("/mensagens/<id>", methods=["GET"])
def pegar_mensagens(id):
    return jsonify({"mensagem": f"Olá seu id é {id}!"})

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8080)

    