from flask import jsonify
from config.config import pedidos_collection
from bson import ObjectId
from models.pedido import Pedidos
from services.cliente_service import get_cliente_by_id
from services.produto_service import get_produto_by_id

# serviço responsável pela listagem  de pedidos. 
# a implementação da consulta retorna uma lista ordenada pelo id_pedido
def lista_todos_pedidos():
    pedidos = pedidos_collection.find().sort("id_pedido",1)
    return [pedido for pedido in pedidos]

# serviço responsável pela pesquisa de pedido pelo id_pedido
# a implementação da pesquisa retorna um obj pedido , ou None.
def get_pedido_by_id(id_pedido):
    try: 
        return pedidos_collection.find_one({"id_pedido": int(id_pedido)})
        
    except ValueError:
        # Se o id_pedido não puder ser convertido para inteiro
        print(f"ID inválido: {id_pedido}")
        return None
    except Exception as e:
        print(f"Erro ao buscar pedido por ID: {e}")
        return None
    
# serviço responsável pela alteração de produto com o id informado.
# a implementação altera o produto pelo id_produto, e retorna o objeto produto alterado.
def update_pedido(id_pedido, dados):
    try:
    
        pedido = get_pedido_by_id(id_pedido)
        if pedido:
            
            id_cliente = dados['id_cliente']
            id_produto = dados['id_produto']
            
            # Verificar se o cliente existe
            cliente = get_cliente_by_id(id_cliente)     
            if cliente is None:
                return f"Cliente {id_cliente} não encontrado"

            # Verificar se o produto existe
            produto = get_produto_by_id(id_produto)         
            if produto is None:
                return f"Produto {id_produto} não encontrado"
            
            # Busca e atualiza o pedido usando find_one_and_update
            pedido_atualizado = pedidos_collection.find_one_and_update(
                {"id_pedido": int(id_pedido)},  # Condição de busca
                {"$set": dados},  # Dados a serem atualizados
                return_document=True  # Retorna o documento atualizado
            )
            
            if pedido_atualizado:
                # Retorna o pedido atualizado como um objeto pedido
                return Pedidos(
                    id_pedido=pedido_atualizado['id_pedido'], 
                    id_cliente=pedido_atualizado['id_cliente'], 
                    id_produto=pedido_atualizado['id_produto'], 
                    valor=pedido_atualizado['valor'], 
                    data_pedido=pedido_atualizado['data_pedido']
                )
            else:
                # Se nenhum pedido foi atualizado
                return None
        else: return f"Não existe um pedido com o id {id_pedido}"

    except Exception as e:
        print(f"Erro ao atualizar pedido: {e}")
        return None

# serviço responsável pela criação de cliente no catálogo de clientes
# a implementação não permite inclusão de clientes com id_cliente repetidos.
def create_pedido(dados):    
    
    
    id_pedido = dados['id_pedido']
    
    pedido = get_pedido_by_id(id_pedido)
    
    if pedido is None:
        
        id_cliente = dados['id_cliente']
        id_produto = dados['id_produto']
        
        # Verificar se o cliente existe
        cliente = get_cliente_by_id(id_cliente)     
        if cliente is None:
            return f"Cliente {id_cliente} não encontrado"

        # Verificar se o produto existe
        produto = get_produto_by_id(id_produto)         
        if produto is None:
            return f"Produto {id_produto} não encontrado"
    
        novo_pedido = Pedidos(
            id_pedido=dados['id_pedido'], 
            id_cliente=dados['id_cliente'], 
            id_produto=dados['id_produto'], 
            valor=dados['valor'], 
            data_pedido=dados['data_pedido']
        )
        
        pedido = pedidos_collection.insert_one(novo_pedido.serialize())
    
        if pedido.inserted_id:
            return novo_pedido  # Retornando o pedido criado
        else:
            return None
    else:
        return f"Já existe um pedido com o id {id_pedido}"
    
# serviço responsável pela exclusão de pedido com o id informado.
# a implementação pesquisa o pedido pelo id_pedido, mas exclui pelo "_id" do documento.
#Retorna NOne, se o pedido não existir.
def delete_pedido(id_pedido):
    try:

        # Converter id_pedido para inteiro (ajuste se necessário)
        id_pedido = int(id_pedido)

        # Buscar o documento utilizando o id_produto personalizado
        resultado_busca = get_pedido_by_id(id_pedido)
        
        if resultado_busca:
            _id = resultado_busca["_id"]

            resultado = pedidos_collection.delete_one({"_id": _id})

            if resultado.deleted_count == 1:
                return True
        return None

    except Exception as e:
        return f"Erro ao excluir o pedido: {e}", 500
    