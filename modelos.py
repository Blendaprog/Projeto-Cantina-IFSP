class Produto:
    def __init__(self, id, nome, categoria, preco, estoque, disponivel):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.estoque = estoque
        self.disponivel = disponivel

class Pedido:
    def __init__(self, id, data, hora, tipo, status, pagamento):
        self.id = id
        self.data = data
        self.hora = hora
        self.tipo = tipo
        self.status = status
        self.pagamento = pagamento

class Itens_pedido:
    def __init__(self, id, pedido_id, produto_id, quantidade, preco):
        self.id = id
        self.pedido_id = pedido_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco = preco

class Despesas:
    def __init__(self, id, descricao, valor, data):
        self.id = id
        self.descricao = descricao
        self.valor = valor
        self.data = data