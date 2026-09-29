import sqlite3
from datetime import datetime


class Banco:
    def __init__(self, nome_banco="cantina.db"):
        self.nome_banco = nome_banco
        self.conexao = sqlite3.connect(self.nome_banco)
        self.conexao.execute("PRAGMA foreign_keys = ON")
        self.criar_tabelas()

    def criar_tabelas(self):
        cursor = self.conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL,
                estoque INTEGER DEFAULT 0,
                disponivel INTEGER DEFAULT 1
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                hora TEXT NOT NULL,
                tipo TEXT NOT NULL,
                status TEXT NOT NULL,
                total REAL NOT NULL,
                pagamento TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS itens_pedido (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                preco REAL NOT NULL,
                FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS despesas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                data TEXT NOT NULL
            )
        """)

        self.conexao.commit()

    def cadastrar_produtos_iniciais(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT COUNT(*) FROM produtos")
        if cursor.fetchone()[0] > 0:
            return

        produtos = [
            ("Croissant de presunto e queijo", "Salgados", 7.00),
            ("Risole de 4 queijos", "Salgados", 5.50),
            ("Risole de carne", "Salgados", 5.50),
            ("Croissant 3 queijos", "Salgados", 6.50),
            ("Hambúrguer com cheddar", "Salgados", 7.00),
            ("Enroladinho de bauru", "Salgados", 7.00),
            ("Pão de batata com calabresa", "Salgados", 6.50),
            ("Pão de batata de frango", "Salgados", 6.50),
            ("Esfiha de carne", "Salgados", 7.00),
            ("Coxinha", "Salgados", 5.50),
            ("Pão de queijo", "Salgados", 3.50),
            ("Caldo", "Salgados", 20.00),
            ("Espeto", "Salgados", 9.00),
            ("Guaraná 350ml", "Bebidas", 5.50),
            ("Fanta uva 350ml", "Bebidas", 5.50),
            ("Fanta laranja 350ml", "Bebidas", 5.50),
            ("Coca-Cola zero açúcar 350ml", "Bebidas", 5.50),
            ("Coca-Cola 350ml", "Bebidas", 5.50),
            ("Suco Tropical 480ml", "Bebidas", 8.00),
            ("Suco Kmais 300ml", "Bebidas", 7.50),
            ("Refrigerante Caçula 200ml", "Bebidas", 2.50),
            ("Doce", "Doces", 3.00), ("Paçoca", "Doces", 1.00),
            ("Bombom", "Doces", 2.50), ("Trento", "Doces", 4.50),
            ("Biscoito", "Doces", 3.50), ("Emília", "Doces", 2.50),
            ("Halls", "Doces", 2.50), ("Bolo", "Doces", 6.00),
            ("Suspiro", "Doces", 3.00), ("Pão de mel", "Doces", 5.00),
            ("Copinho de banana", "Doces", 3.00), ("Cocada", "Doces", 3.00),
            ("Doce em massa de batata-doce", "Doces", 3.00),
            ("Cajuzinho", "Doces", 3.00), ("Geladão", "Doces", 7.00),
            ("Cremosinho", "Doces", 2.50), ("Maria bolacha", "Doces", 3.00),
            ("Café", "Doces", 2.00), ("Cup Noodles", "Outros", 7.00),
        ]
        cursor.executemany("""
            INSERT INTO produtos (nome, categoria, preco, estoque, disponivel)
            VALUES (?, ?, ?, 100, 1)
        """, produtos)
        self.conexao.commit()

    def buscar_produtos(self):
        cursor = self.conexao.cursor()
        cursor.execute("""
            SELECT id, nome, categoria, preco
            FROM produtos
            WHERE disponivel = 1 AND estoque > 0
            ORDER BY CASE categoria
                WHEN 'Salgados' THEN 1
                WHEN 'Bebidas' THEN 2
                WHEN 'Doces' THEN 3
                ELSE 4 END, nome
        """)
        return cursor.fetchall()

    def registrar_pedido(self, carrinho, pagamento):
        agora = datetime.now()
        data = agora.strftime("%d/%m/%Y")
        hora = agora.strftime("%H:%M")
        total = sum(item["preco"] * item["quantidade"] for item in carrinho)

        cursor = self.conexao.cursor()
        cursor.execute("""
            INSERT INTO pedidos (data, hora, tipo, status, total, pagamento)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (data, hora, "Totem", "Recebido", total, pagamento))
        pedido_id = cursor.lastrowid

        for item in carrinho:
            cursor.execute("""
                INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco)
                VALUES (?, ?, ?, ?)
            """, (pedido_id, item["id"], item["quantidade"], item["preco"]))
            cursor.execute("""
                UPDATE produtos SET estoque = estoque - ? WHERE id = ?
            """, (item["quantidade"], item["id"]))

        self.conexao.commit()
        return pedido_id, total

    def fechar(self):
        self.conexao.close()
