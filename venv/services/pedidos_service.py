from flask import jsonify
from config.config import pedidos_collection
from bson import ObjectId
from models.pedido import Pedidos
from services.cliente_service import get_cliente_by_id
from services.produto_service import get_produto_by_id

def lista_pedidos():
    pedidos = pedidos_collection.find().sort("id_pedido",1)
    return [pedido for pedido in pedidos]

def get_pedido_by_id(id_pedido):
    try: 
        dict_pedido = pedidos_collection.find_one({"id_pedido": int(id_pedido)})
        
        if dict_pedido:
            # Se o produto foi encontrado, retorne um obj produto
           return Pedidos(
                id_pedido=dict_pedido['id_pedido'], 
                id_cliente=dict_pedido['id_cliente'], 
                id_produto=dict_pedido['id_produto'], 
                valor=dict_pedido['valor'], 
                data_pedido=dict_pedido['data_pedido']
            )
        else:
            # Se o produto não foi encontrado, retorne None
            return None
    except ValueError:
        # Se o id_pedido não puder ser convertido para inteiro
        print(f"ID inválido: {id_pedido}")
        return None
    except Exception as e:
        print(f"Erro ao buscar pedido por ID: {e}")
        return None


def create_pedido(dados):    
    
    id_cliente = dados['id_cliente']
    id_produto = dados['id_produto']

    # Verificar se o cliente existe
    cliente = get_cliente_by_id(id_cliente)
    print(cliente)
    
    if not cliente:
        return {"error": f"Cliente {id_cliente} não encontrado"}

    # Verificar se o produto existe
    produto = get_produto_by_id(id_produto) 
    
    if not produto:
        return {"error": f"Produto {id_produto} não encontrado"}
   
    novo_pedido = Pedidos(
        id_pedido=dados['id_pedido'], 
        id_cliente=dados['id_cliente'], 
        id_produto=dados['id_produto'], 
        valor=dados['valor'], 
        data_pedido=dados['data_pedido']
     )
        
    pedido = pedidos_collection.insert_one(novo_pedido.serialize())
    print(pedido)    
    if pedido.inserted_id:
        return novo_pedido  # Retornando o pedido criado
    else:
        return None
    