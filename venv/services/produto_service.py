from config.config import produtos_collection
from bson import ObjectId
from models.produto import Produtos

def lista_todos_produtos():
    produtos = produtos_collection.find().sort("id_produto",1)
    return [produto for produto in produtos]

def get_produto_by_id(id_produto):
    try: 
        dict_produto = produtos_collection.find_one({"id_produto": int(id_produto)})
        
        if dict_produto:
            # Se o produto foi encontrado, retorne um obj produto
           return Produtos(
                id_produto=dict_produto['id_produto'], 
                nome=dict_produto['nome'], 
                descricao=dict_produto['descricao'], 
                preco=dict_produto['preco'], 
                categoria=dict_produto['categoria']
            )
        else:
            # Se o produto não foi encontrado, retorne None
            return None
    except ValueError:
        # Se o id_produto não puder ser convertido para inteiro
        print(f"ID inválido: {id_produto}")
        return None
    except Exception as e:
        print(f"Erro ao buscar produto por ID: {e}")
        return None

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