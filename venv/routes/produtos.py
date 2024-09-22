from flask import Blueprint, jsonify, request
from config.config import produtos_collection
from models.produto import Produtos
from services.produto_service import lista_todos_produtos, create_produto

produtos_bp = Blueprint('produtos_bp', __name__)

@produtos_bp.route("/produtos", methods=["GET"])
def lista_produtos():
    try:
        # Verifique se lista_todos_produtos retorna um cursor ou uma lista
        produtos = list(lista_todos_produtos())  # Garantir que seja uma lista
        
        for produto in produtos:
            if '_id' in produto:
                produto['_id'] = str(produto['_id'])
        
        return jsonify(produtos), 200

    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao listar produtos.", 500

@produtos_bp.route("/inserirProduto", methods=['POST'])
def set_produto():
    dados = request.get_json()
    try:
        novoProduto = create_produto(dados)
        
        if novoProduto is not None:
            return jsonify(novoProduto.serialize()), 201
        else:
            return f"O id {dados['id_produto']} já foi utilizado por outro produto.", 500  # Caso já tenha sido inserido
    except Exception as e:
        return "Erro ao inserir produto.", 500  

#
@produtos_bp.route("/alteraProduto/<id_produto>", methods=["PUT"])
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

@produtos_bp.route("/excluiproduto/<id_produto>", methods=["DELETE"])
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