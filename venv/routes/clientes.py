from flask import Blueprint, jsonify, request
from config.config import clientes_collection
from models.cliente import Cliente
from services.cliente_service import get_all_clientes , create_cliente , update_cliente, get_cliente_by_id , delete_cliente

clientes_bp = Blueprint('clientes_bp', __name__)

@clientes_bp.route("/clientes", methods=["GET"])
def lista_clientes():
    try:
        clientes = get_all_clientes()
        
        for cliente in clientes:
            cliente['_id'] = str(cliente['_id'])
        return jsonify(clientes), 200
    except Exception as e:
        return f"Erro ao listar clientes: {e}", 500

@clientes_bp.route("/inserirCliente", methods=['POST'])
def set_cliente():
    dados = request.get_json()

    try:
        novo_cliente = create_cliente(dados)  # Usando a função que cria o cliente
        
        if isinstance(novo_cliente,Cliente):
            # Retornando os dados do cliente criado, incluindo o ID gerado
            return jsonify(novo_cliente.serialize()), 201  # Serializando o novo cliente
        else:
            return novo_cliente, 500 
        
    except Exception as e:
        return "Erro ao inserir cliente.", 500  # Mensagem de erro genérica


@clientes_bp.route("/alteraCliente/<id_cliente>", methods=["PUT"])
def atualiza_cliente(id_cliente):
    try:
        dados = request.get_json()

        # Converter id_cliente para inteiro (ajuste se necessário)
        id_cliente = int(id_cliente)
        
        cliente_atualizado = update_cliente(id_cliente,dados)
       
        if cliente_atualizado:
            return jsonify(cliente_atualizado.serialize()),200
        else:
             return f"O id {id_cliente} informado não foi encontrado.",500
    except ValueError:
        # Se o id_cliente não for um número inteiro válido
        return f"O ID precisa ser um número inteiro", 400
    except Exception as e:
        return f"Erro ao atualizar cliente: {e}", 500
    

#
#
@clientes_bp.route("/clientes/<id_cliente>", methods=["GET"])
def consultaCliente_por_id(id_cliente):
    try:
         # Converter id_cliente para inteiro 
        id_cliente = int(id_cliente)
        
        cliente = get_cliente_by_id(id_cliente)
        
        if cliente:
            cliente['_id'] = str(cliente['_id'])
            return jsonify(cliente), 200 
        else:           
            return f"O id {id_cliente} informado não foi encontrado.",200
    except ValueError:
        # Se o id_cliente não for um número inteiro válido
        return f"O ID precisa ser um número inteiro", 400
    

@clientes_bp.route("/excluiCliente/<id_cliente>", methods=["DELETE"])
def excluir_cliente(id_cliente):
    try:

        # Converter id_cliente para inteiro (ajuste se necessário)
        id_cliente = int(id_cliente)       
        
        resultado = delete_cliente(id_cliente)
        print(f"resultado: {resultado}")    
            
        if resultado:
            return "", 204
        else:
            return f"Cliente com id {id_cliente} não encontrado.", 404
    except ValueError:
        # Se o id_cliente não for um número inteiro válido
        return f"O ID precisa ser um número inteiro", 400
    except Exception as e:
        return {f"Erro ao excluir cliente: {e}"}, 500
