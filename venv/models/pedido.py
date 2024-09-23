class Pedidos():
    def __init__(self,id_pedido,id_produto,id_cliente,data_pedido,valor):
        self.id_pedido = id_pedido
        self.id_produto = id_produto
        self.id_cliente = id_cliente
        self.data_pedido = data_pedido
        self.valor = valor

    def serialize(self):
        return {
            "id_pedido": self.id_pedido,
            "id_cliente": self.id_cliente,
            "id_produto": self.id_produto,
            "data_pedido": self.data_pedido,
            "valor": self.valor,
        }   