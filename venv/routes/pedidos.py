from flask import Blueprint, jsonify, request
from config.config import pedidos_collection,clientes_collection, produtos_collection
from models.pedido import Pedidos
from services.pedidos_service import lista_todos_pedidos, get_pedido_by_id, create_pedido, delete_pedido, update_pedido


pedidos_bp = Blueprint('pedidos_bp', __name__)

@pedidos_bp.route("/pedidos",methods=['GET'])
def lista_pedidos():
    try:
        pedidos = lista_todos_pedidos() 
        
        if pedidos:
            for pedido in pedidos:
                pedido['_id'] = str(pedido['_id'])
            return jsonify(pedidos), 200
        else: return None
    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao listar pedidos.", 500
    
@pedidos_bp.route("/pedidos/<id_pedido>", methods=["GET"])
def consultaPedido_por_id(id_pedido):
    try:
         # Converter id_pedido para inteiro 
        id_pedido = int(id_pedido)
        
        pedido = get_pedido_by_id(id_pedido)
        
        if pedido:
            pedido['_id'] = str(pedido['_id'])
            return jsonify(pedido), 200 
        else:           
            return f"O id {id_pedido} informado não foi encontrado.",200
    except ValueError:
        # Se o id_produto não for um número inteiro válido
        return f"O ID precisa ser um número inteiro", 400
    
    
@pedidos_bp.route("/alteraPedido/<id_pedido>", methods=["PUT"])
def atualiza_pedido(id_pedido):
    try:
        dados = request.get_json()

        # Converter id_pedido para inteiro (ajuste se necessário)
        id_pedido = int(id_pedido)

        # Atualiza o documento utilizando o _id
        pedido_atualizacao = update_pedido(id_pedido, dados)
    
        if pedido_atualizacao:
            return jsonify(pedido_atualizacao.serialize()),200
        else:
            return f"Erro ao atualizar pedido.", 500

    except Exception as e:
        return f"Erro ao atualizar pedido: {e}", 500
    
@pedidos_bp.route("/inserirPedido", methods=['POST'])
def set_pedido():
    dados = request.get_json()
    
    pedido = create_pedido(dados)
    if isinstance(pedido, Pedidos):
        return jsonify(pedido.serialize()), 201
    else:
        return pedido, 500  
    
@pedidos_bp.route("/excluiPedido/<id_pedido>", methods=["DELETE"])
def excluir_pedido(id_pedido):
    try:

        # Converter id_pedido para inteiro (ajuste se necessário)
        id_pedido = int(id_pedido)       
        
        resultado = delete_pedido(id_pedido)
                    
        if resultado:
            return "", 204
        else:
            return f"pedido com id {id_pedido} não encontrado.", 404
    except ValueError:
        # Se o id_produto não for um número inteiro válido
        return f"O ID precisa ser um número inteiro", 400
    except Exception as e:
        return {f"Erro ao excluir produto: {e}"}, 500

    
    
    