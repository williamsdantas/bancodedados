from flask import Blueprint, jsonify, request
from config.config import pedidos_collection,clientes_collection, produtos_collection
from models.pedido import Pedidos
from services.pedidos_service import lista_pedidos, get_pedido_by_id, create_pedido


pedidos_bp = Blueprint('pedidos_bp', __name__)

@pedidos_bp.route("/pedidos",methods=['GET'])
def lista_pedidos():
    try:
        pedidos = lista_pedidos() 
        
        for pedido in pedidos:
            pedido['_id'] = str(pedido['_id'])
        
        return jsonify(pedido), 200

    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao listar pedidos.", 500
    

@pedidos_bp.route("/inserirPedido", methods=['POST'])
def set_pedido():
    dados = request.get_json()
    
    pedido = create_pedido(dados)
    if isinstance(pedido, Pedidos):
        return jsonify(pedido.serialize()), 201
    else:
        return pedido, 500  

    
    
    