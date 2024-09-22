from bson import ObjectId
from flask import Flask, jsonify, request
from config.config import bd, pedidos_collection, produtos_collection, clientes_collection

from routes.clientes import clientes_bp

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World."

@app.route("/produtos")
def lista_produtos():
    try:
        produtos = produtos_collection.find()

        produtos_serializado = []
        for produto in produtos:
            produto['_id'] = str(produto['_id'])
            produtos_serializado.append(produto)
        
        return jsonify(produtos_serializado), 200

    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao listar produtos.", 500

@app.route("/inserirProduto", methods=['POST'])
def set_produto():
    dados = request.get_json()

    novo_produto = Produtos(
        id_produto=dados['id_produto'],
        nome=dados['nome'],
        categoria=dados['categoria'],
        preco=dados['preco'],
        descricao=dados["descricao"]
    )

    resultado = produtos_collection.insert_one(novo_produto.serialize())

    if  resultado.inserted_id:
        novo_produto.id_produto = str(resultado.inserted_id)
        return jsonify(novo_produto.serialize()), 201
    else:
        return "Erro ao inserir produto.", 500

@app.route("/alteraProduto/<id_produto>", methods=["PUT"])
def update_produto(id_produto):
    try:
        dados = request.get_json()

        # Converter id_produto para inteiro (ajuste se necessário)
        id_produto = int(id_produto)

        # Buscar o documento utilizando o id_produto personalizado
        resultado_busca = produtos_collection.find_one({"id_produto": id_produto})

        if resultado_busca:
            _id = resultado_busca["_id"]

            # Atualiza o documento utilizando o _id
            resultado_atualizacao = produtos_collection.update_one(
                {"_id": _id},
                {"$set": dados}
            )

            if resultado_atualizacao.modified_count == 1:
                return f"produto {id_produto} atualizado com sucesso.", 200
            else:
                return f"Erro ao atualizar produto.", 500
        else:
            return f"produto com id {id_produto} não encontrado.", 404

    except Exception as e:
        return f"Erro ao atualizar produto: {e}", 500

@app.route("/excluiproduto/<id_produto>", methods=["DELETE"])
def delete_produto(id_produto):
    try:

        # Converter id_produto para inteiro (ajuste se necessário)
        id_produto = int(id_produto)

        # Buscar o documento utilizando o id_produto personalizado
        resultado_busca = produtos_collection.find_one({"id_produto": id_produto})

        if resultado_busca:
            _id = resultado_busca["_id"]

            resultado = produtos_collection.delete_one(
                {"_id": _id}
            )
            print(resultado)
            if resultado.deleted_count == 1:
                return f"produto {id_produto} excluido com sucesso.", 200
            else:
                return f"produto com id {id_produto} não encontrado.", 404

    except Exception as e:
        return f"Erro ao excluir produto: {e}", 500

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
#app.register_blueprint(produtos_bp)
#app.register_blueprint(pedidos_bp)

if __name__ == "__main__":
    app.run(debug=True)