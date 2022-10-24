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


def remover(obj):
    banco_de_dados.session.delete(obj)
    banco_de_dados.session.commit()

def validar_mensagem(dados):
    if "email" not in dados:
        return jsonify({"mensagem": "Email não informado"}), status.HTTP_400_BAD_REQUEST
    
    if "celular" not in dados:
        return jsonify({"mensagem": "Celular não informado"}), status.HTTP_400_BAD_REQUEST
    
    if "nome" not in dados:
        return jsonify({"mensagem": "Nome não informado"}), status.HTTP_400_BAD_REQUEST
    
    if "mensagem" not in dados:
        return jsonify({"mensagem": "Mensagem não informada"}), status.HTTP_400_BAD_REQUEST

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
        validar_mensagem(dados)

        mensagem = Mensagem(
            celular=dados["celular"],
            email=dados["email"],
            nome=dados["nome"],
            mensagem=dados["mensagem"],
            conheceu=dados["conheceu"],
            lugar=dados["lugar"]
        )
        banco_de_dados.session.add(mensagem)
        banco_de_dados.session.commit()

        return jsonify({"mensagem": "Mensagem criada com sucesso!"}), status.HTTP_201_CREATED
    except(Exception):
        return jsonify({"mensagem": "Dados inválidos"}), status.HTTP_400_BAD_REQUEST

@app.route("/mensagens/<id>", methods=["PUT"])
def editar_mensagens(id):
    mensagem = Mensagem.query.get(id)

    if mensagem is None:
        return jsonify({"mensagem": "Mensagem não encontrada"}), status.HTTP_404_NOT_FOUND

    dados = request.get_json()
    try:
        validar_mensagem(dados)
        
        mensagem.celular = dados["celular"]
        mensagem.email = dados["email"]
        mensagem.nome = dados["nome"]
        mensagem.mensagem = dados["mensagem"]
        mensagem.lugar = dados["lugar"]
        mensagem.conheceu = dados["conheceu"]
        banco_de_dados.session.commit()

        return jsonify({"mensagem": "Mensagem editada com sucesso!"}), status.HTTP_200_OK
    except Exception as e:
        return jsonify({"mensagem": f"Dados inválidos{e}"}), status.HTTP_400_BAD_REQUEST

@app.route("/mensagens/<id>", methods=["DELETE"])
def deletar_mensagens(id):
    mensagem = Mensagem.query.get(id)
    remover(mensagem)

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
        "celular": mensagem.celular,
        "lugar": mensagem.lugar,
        "conheceu": mensagem.conheceu
    })

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8080)