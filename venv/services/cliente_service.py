from config.config import clientes_collection
from bson import ObjectId
from models.cliente import Cliente

# serviço responsável pela listagem  de clientes. 
# a implementação da consulta retorna uma lista ordenada pelo id_cliente
def get_all_clientes():
    clientes = clientes_collection.find().sort("id_cliente", 1)
    return [cliente for cliente in clientes]

# serviço responsável pela pesquisa de cleintes pelo id_cliente
# a implementação da pesquisa retorna um obj cliente , ou None.
def get_cliente_by_id(id_cliente):
    try:        
        return clientes_collection.find_one({"id_cliente": int(id_cliente)})
            
    except ValueError:
        # Se o id_cliente não puder ser convertido para inteiro
        print(f"ID inválido: {id_cliente}")
        return None
    except Exception as e:
        print(f"Erro ao buscar cliente por ID: {e}")
        return None

# serviço responsável pela criação de cliente no catálogo de clientes
# a implementação não permite inclusão de clientes com id_cliente repetidos.
def create_cliente(dados):
    
     # Verifica se já existe um cliente com o mesmo id_cliente
    cliente = get_cliente_by_id(dados['id_cliente']) 

    if cliente is None:
        novo_cliente = Cliente(
        id_cliente=dados['id_cliente'],
        nome=dados['nome'],
        email=dados['email'],
        cpf=dados['cpf'],
        data_nascimento=dados["data_nascimento"])
        
        cliente = clientes_collection.insert_one(novo_cliente.serialize())
        
        if cliente.inserted_id:
            return novo_cliente  # Retornando o cliente criado
        else:
            return None
    return None
    
# serviço responsável pela alteração de cliente com o id informado.
# a implementação altera o cliente pelo id_cliente, e retorna o objeto cliente alterado.
def update_cliente(id_cliente, dados):
    try:
        # Busca e atualiza o cliente usando find_one_and_update
        cliente_atualizado = clientes_collection.find_one_and_update(
            {"id_cliente": int(id_cliente)},  # Condição de busca
            {"$set": dados},  # Dados a serem atualizados
            return_document=True  # Retorna o documento atualizado
        )
        
        if cliente_atualizado:
            # Retorna o cliente atualizado como um objeto Cliente
            return Cliente(
                            id_cliente=cliente_atualizado['id_cliente'],
                            nome=cliente_atualizado['nome'],
                            email=cliente_atualizado['email'],
                            cpf=cliente_atualizado['cpf'],
                            data_nascimento=cliente_atualizado['data_nascimento']
                        )
        else:
            # Se nenhum cliente foi encontrado para o id_cliente fornecido
            return None

    except Exception as e:
        print(f"Erro ao atualizar cliente: {e}")
        return None
    
# serviço responsável pela exclusão de cliente com o id informado.
# a implementação pesquisa o cliente pelo id_cliente, mas exclui pelo "_id" do documento.
def delete_cliente(id_cliente):
    try:

        # Converter id_cliente para inteiro (ajuste se necessário)
        id_cliente = int(id_cliente)

        # Buscar o documento utilizando o id_cliente personalizado
        resultado_busca = get_cliente_by_id(id_cliente)
        
        print(f"cliente encontrado:{resultado_busca}")
        
        if resultado_busca:
            _id = resultado_busca["_id"]

            resultado = clientes_collection.delete_one({"_id": _id})

            if resultado.deleted_count == 1:
                return True
        return None

    except Exception as e:
        return f"Erro ao excluir cliente: {e}", 500
