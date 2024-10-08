from flask import Blueprint, jsonify, request
from config.config import produtos_collection
from models.produto import Produtos
from services.produto_service import lista_todos_produtos, create_produto, get_produto_by_id, delete_produto, update_produto

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
    
#
#
@produtos_bp.route("/produtos/<id_produto>", methods=["GET"])
def consultaProduto_por_id(id_produto):
    try:
         # Converter id_produto para inteiro 
        id_produto = int(id_produto)
        
        produto = get_produto_by_id(id_produto)
        
        if produto:
            produto['_id'] = str(produto['_id'])
            return jsonify(produto), 200 
        else:           
            return f"O id {id_produto} informado não foi encontrado.",200
    except ValueError:
        # Se o id_produto não for um número inteiro válido
        return f"O ID precisa ser um número inteiro", 400

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
def atualiza_produto(id_produto):
    try:
        dados = request.get_json()

        # Converter id_produto para inteiro (ajuste se necessário)
        id_produto = int(id_produto)

        # Atualiza o documento utilizando o _id
        produto_atualizacao = update_produto(id_produto, dados)
    
        if produto_atualizacao:
            return jsonify(produto_atualizacao.serialize()),200
        else:
            return f"Erro ao atualizar produto.", 500

    except Exception as e:
        return f"Erro ao atualizar produto: {e}", 500

    
@produtos_bp.route("/excluiProduto/<id_produto>", methods=["DELETE"])
def excluir_produto(id_produto):
    try:

        # Converter id_produto para inteiro (ajuste se necessário)
        id_produto = int(id_produto)       
        
        resultado = delete_produto(id_produto)
                    
        if resultado:
            return "", 204
        else:
            return f"produto com id {id_produto} não encontrado.", 404
    except ValueError:
        # Se o id_produto não for um número inteiro válido
        return f"O ID precisa ser um número inteiro", 400
    except Exception as e:
        return {f"Erro ao excluir produto: {e}"}, 500