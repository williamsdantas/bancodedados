from config.config import pedidos_collection
from bson import ObjectId
from models.pedido import Pedidos

def lista_pedidos():
    pedidos = pedidos_collection.find().sort("id_pedido",1)
    return [pedido for pedido in pedidos]