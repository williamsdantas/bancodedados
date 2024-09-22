from flask import Blueprint, jsonify, request
from config.config import pedidos_collection
from models.pedido import Pedidos
from services.pedidos_service import lista_pedidos

pedidos_bp = Blueprint('pedidos_bp', __name__)

@pedidos_bp.route("/pedidos")
def lista_pedidos():
    try:
        pedidos = lista_pedidos() 
        
        for pedido in pedidos:
            pedido['_id'] = str(pedido['_id'])
        
        return jsonify(pedido), 200

    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao listar pedidos.", 500