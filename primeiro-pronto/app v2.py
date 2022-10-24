from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_api import status

banco_de_dados = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
banco_de_dados.init_app(app)

class Mensagem(banco_de_dados.Model):
    id = banco_de_dados.Column(banco_de_dados.Integer, primary_key=True)
    celular = banco_de_dados.Column(banco_de_dados.String(15))
    email = banco_de_dados.Column(banco_de_dados.String(100))
    nome = banco_de_dados.Column(banco_de_dados.String(60))
    mensagem = banco_de_dados.Column(banco_de_dados.Text())

with app.app_context():
    banco_de_dados.create_all()
    Mensagem.query.delete()

@app.route("/")
def hello_ti360():
    return jsonify({"message": "Hello TI360!"})

@app.route("/mensagens", methods=["GET"])
def ola_ti360_get():
    return jsonify({"mensagem": "Olá TI360 GET!"})

@app.route("/mensagens", methods=["POST"])
def criar_mensagens():
    dados = request.get_json()
    try:
        if "email" not in dados:
            return jsonify({"mensagem": "Email não informado"}), status.HTTP_400_BAD_REQUEST
        
        if "celular" not in dados:
            return jsonify({"mensagem": "Celular não informado"}), status.HTTP_400_BAD_REQUEST
        
        if "nome" not in dados:
            return jsonify({"mensagem": "Nome não informado"}), status.HTTP_400_BAD_REQUEST
        
        if "mensagem" not in dados:
            return jsonify({"mensagem": "Mensagem não informada"}), status.HTTP_400_BAD_REQUEST

        mensagem = Mensagem(
            celular=dados["celular"],
            email=dados["email"],
            nome=dados["nome"],
            mensagem=dados["mensagem"],
        )
        banco_de_dados.session.add(mensagem)
        banco_de_dados.session.commit()

        return jsonify({"mensagem": "Mensagem criada com sucesso!"}), status.HTTP_201_CREATED
    except(Exception):
        return jsonify({"mensagem": "Dados inválidos"}), status.HTTP_400_BAD_REQUEST

@app.route("/mensagens", methods=["PUT"])
def editar_mensagens():
    return jsonify({"mensagem": "Edição realizada com sucesso!"})

@app.route("/mensagens", methods=["DELETE"])
def deletar_mensagens():
    return jsonify({"mensagem": "Remoção realizada com sucesso!"})

@app.route("/mensagens/<id>", methods=["GET"])
def pegar_mensagens(id):
    mensagem = Mensagem.query.get(id)

    if mensagem is None:
        return jsonify({"mensagem": "Mensagem não encontrada"}), status.HTTP_404_NOT_FOUND
        
    return jsonify({
        "mensagem": mensagem.mensagem,
        "nome": mensagem.nome,
        "email": mensagem.email,
        "celular": mensagem.celular
    })

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8080)