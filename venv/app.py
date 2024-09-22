from bson import ObjectId
from flask import Flask, jsonify, request
from config.config import bd, pedidos_collection

from routes.clientes import clientes_bp
from routes.produtos import produtos_bp
from routes.pedidos import pedidos_bp

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World."

@app.route("/pedidos", methods=['POST'])
def set_pedido():
    dados = request.get_json()
    id_cliente = dados['id_cliente']
    id_produto = dados['id_produto']

    # Verificar se o cliente existe
    cliente = clientes_collection.find_one({"id_cliente": id_cliente})
    if not cliente:
        return jsonify({"error": "Cliente não encontrado"}), 404

    # Verificar se o produto existe
    produto = produtos_collection.find_one({"id_produto": id_produto})
    if not produto:
        return jsonify({"error": "Produto não encontrado"}), 404

    # Criar o novo pedido
    novo_pedido = {
        "id_cliente": id_cliente,
        "id_produto": id_produto,
        "data_pedido": id_pedido,
        "valor": valor
    }
    resultado = pedidos_collection.insert_one(novo_pedido)

    if resultado.inserted_id:
        return jsonify({"Pedido criado com sucesso"}), 201
    else:
        return jsonify({"Erro ao criar pedido"}), 500

# Registrar os blueprints
app.register_blueprint(clientes_bp)
app.register_blueprint(produtos_bp)
app.register_blueprint(pedidos_bp)

if __name__ == "__main__":
    app.run(debug=True)