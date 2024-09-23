from config.config import produtos_collection
from bson import ObjectId
from models.produto import Produtos

# serviço responsável pela listagem  de produtos. 
# a implementação da consulta retorna uma lista ordenada pelo id_produto
def lista_todos_produtos():
    produtos = produtos_collection.find().sort("id_produto",1)
    return [produto for produto in produtos]

# serviço responsável pela pesquisa de produtos pelo id_produto
# a implementação da pesquisa retorna um obj produto , ou None.
def get_produto_by_id(id_produto):
    try: 
        return produtos_collection.find_one({"id_produto": int(id_produto)})
        
    except ValueError:
        # Se o id_produto não puder ser convertido para inteiro
        print(f"ID inválido: {id_produto}")
        return None
    except Exception as e:
        print(f"Erro ao buscar produto por ID: {e}")
        return None

# serviço responsável pela criação de produto no catálogo de produtosw
# a implementação não permite inclusão de produtos com id_produto repetidos.
def create_produto(dados):
    
    produto = get_produto_by_id(dados['id_produto']) 
        
    if produto is None:
        novo_produto = Produtos(
            id_produto=dados['id_produto'], 
            nome=dados['nome'], 
            descricao=dados['descricao'], 
            preco=dados['preco'], 
            categoria=dados['categoria']
        )
        
        produto = produtos_collection.insert_one(novo_produto.serialize())
        
        if produto.inserted_id:
            return novo_produto  # Retornando o cliente criado
        else:
            return None
    return None

# serviço responsável pela exclusão de produto com o id informado.
# a implementação pesquisa o produto pelo id_produto, mas exclui pelo "_id" do documento.
#Retorna NOne, se o protudo não existir.
def delete_produto(id_produto):
    try:

        # Converter id_produto para inteiro (ajuste se necessário)
        id_produto = int(id_produto)

        # Buscar o documento utilizando o id_produto personalizado
        resultado_busca = get_produto_by_id(id_produto)
        
        if resultado_busca:
            _id = resultado_busca["_id"]

            resultado = produtos_collection.delete_one({"_id": _id})

            if resultado.deleted_count == 1:
                return True
        return None

    except Exception as e:
        return f"Erro ao excluir o produto: {e}", 500