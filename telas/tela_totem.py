from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QScrollArea,
    QMessageBox
)
from PySide6.QtCore import Qt


class TelaTotem(QWidget):
    def __init__(self, banco, tela_anterior=None):
        super().__init__()

        self.banco = banco
        self.tela_anterior = tela_anterior
        self.carrinho = []

        self.setWindowTitle("Cantina IFSP CJO")
        self.setMinimumSize(1000, 700)

        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(45, 30, 45, 30)
        layout_principal.setSpacing(12)

        botao_voltar = QPushButton("← Voltar")
        botao_voltar.setObjectName("voltar")
        botao_voltar.clicked.connect(self.voltar)
        layout_principal.addWidget(botao_voltar)

        titulo = QLabel("CANTINA IFSP CJO")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setObjectName("titulo")

        subtitulo = QLabel("Faça seu pedido")
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("""
            font-size: 20px;
        """)

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(subtitulo)

        area = QScrollArea()
        area.setWidgetResizable(True)

        conteudo = QWidget()
        layout_produtos = QVBoxLayout()

        produtos = self.banco.buscar_produtos()

        categoria_atual = ""
        linha = None
        quantidade_na_linha = 0

        for id_produto, nome, categoria, preco in produtos:

            if categoria != categoria_atual:
                categoria_atual = categoria

                titulo_categoria = QLabel(categoria)
                titulo_categoria.setStyleSheet("""
                    font-size: 24px;
                    font-weight: bold;
                    margin-top: 15px;
                """)

                layout_produtos.addWidget(titulo_categoria)

                linha = QHBoxLayout()
                layout_produtos.addLayout(linha)
                quantidade_na_linha = 0

            card = QFrame()
            card.setObjectName("card")
            card.setMinimumSize(220, 155)

            layout_card = QVBoxLayout()

            nome_label = QLabel(nome)
            nome_label.setAlignment(Qt.AlignCenter)
            nome_label.setWordWrap(True)
            nome_label.setStyleSheet("""
                font-size: 17px;
                font-weight: bold;
            """)

            preco_label = QLabel(f"R$ {preco:.2f}")
            preco_label.setAlignment(Qt.AlignCenter)

            botao = QPushButton("ADICIONAR")

            botao.clicked.connect(
                lambda _, id=id_produto, n=nome, p=preco:
                self.adicionar_carrinho(id, n, p)
            )

            layout_card.addWidget(nome_label)
            layout_card.addWidget(preco_label)
            layout_card.addWidget(botao)

            card.setLayout(layout_card)

            linha.addWidget(card)

            quantidade_na_linha += 1

            if quantidade_na_linha == 4:
                linha = QHBoxLayout()
                layout_produtos.addLayout(linha)
                quantidade_na_linha = 0

        conteudo.setLayout(layout_produtos)
        area.setWidget(conteudo)

        layout_principal.addWidget(area)

        self.botao_carrinho = QPushButton("🛒  VER CARRINHO (0)")
        self.botao_carrinho.setObjectName("carrinho")
        self.botao_carrinho.setMinimumHeight(50)
        self.botao_carrinho.clicked.connect(self.mostrar_carrinho)

        layout_principal.addWidget(self.botao_carrinho)

        self.setLayout(layout_principal)

    def adicionar_carrinho(self, id_produto, nome, preco):

        for item in self.carrinho:
            if item["id"] == id_produto:
                item["quantidade"] += 1
                break
        else:
            self.carrinho.append({
                "id": id_produto,
                "nome": nome,
                "preco": preco,
                "quantidade": 1
            })

        quantidade_total = sum(
            item["quantidade"] for item in self.carrinho
        )

        self.botao_carrinho.setText(
            f"🛒  VER CARRINHO ({quantidade_total})"
        )

    def mostrar_carrinho(self):

        if not self.carrinho:
            QMessageBox.information(
                self,
                "Carrinho",
                "Seu carrinho está vazio."
            )
            return

        janela = QWidget()
        janela.setWindowTitle("Seu Carrinho")
        janela.setMinimumSize(600, 500)

        layout = QVBoxLayout()

        titulo = QLabel("SEU CARRINHO")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        layout.addWidget(titulo)

        total = 0

        for item in self.carrinho:

            linha = QHBoxLayout()

            nome = QLabel(
                f"{item['nome']}  x{item['quantidade']}"
            )

            subtotal = item["preco"] * item["quantidade"]
            total += subtotal

            valor = QLabel(
                f"R$ {subtotal:.2f}"
            )

            menos = QPushButton("-")
            mais = QPushButton("+")
            remover = QPushButton("REMOVER")

            menos.clicked.connect(
                lambda _, id=item["id"]:
                self.diminuir_quantidade(id, janela)
            )

            mais.clicked.connect(
                lambda _, id=item["id"]:
                self.aumentar_quantidade(id, janela)
            )

            remover.clicked.connect(
                lambda _, id=item["id"]:
                self.remover_item(id, janela)
            )

            linha.addWidget(nome)
            linha.addWidget(valor)
            linha.addWidget(menos)
            linha.addWidget(mais)
            linha.addWidget(remover)

            layout.addLayout(linha)

        linha_total = QHBoxLayout()

        texto_total = QLabel(
            f"TOTAL: R$ {total:.2f}"
        )

        texto_total.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
        """)

        linha_total.addWidget(texto_total)

        layout.addLayout(linha_total)

        botao_finalizar = QPushButton("FINALIZAR PEDIDO")
        botao_finalizar.setMinimumHeight(50)

        botao_finalizar.clicked.connect(
            lambda: self.finalizar_pedido(janela)
        )

        layout.addWidget(botao_finalizar)

        janela.setLayout(layout)

        self.janela_carrinho = janela
        janela.show()

    def aumentar_quantidade(self, id_produto, janela):

        for item in self.carrinho:
            if item["id"] == id_produto:
                item["quantidade"] += 1
                break

        janela.close()
        self.mostrar_carrinho()

    def diminuir_quantidade(self, id_produto, janela):

        for item in self.carrinho:

            if item["id"] == id_produto:

                item["quantidade"] -= 1

                if item["quantidade"] <= 0:
                    self.carrinho.remove(item)

                break

        janela.close()

        if self.carrinho:
            self.mostrar_carrinho()

        self.atualizar_botao_carrinho()

    def remover_item(self, id_produto, janela):

        self.carrinho = [
            item for item in self.carrinho
            if item["id"] != id_produto
        ]

        janela.close()

        if self.carrinho:
            self.mostrar_carrinho()

        self.atualizar_botao_carrinho()

    def atualizar_botao_carrinho(self):

        quantidade_total = sum(
            item["quantidade"]
            for item in self.carrinho
        )

        self.botao_carrinho.setText(
            f"🛒  VER CARRINHO ({quantidade_total})"
        )

    def finalizar_pedido(self, janela):
        from telas.tela_pagamento import TelaPagamento
        janela.close()

        self.tela_pagamento = TelaPagamento(
            self.banco,
            self.carrinho,
            self
        )

        self.tela_pagamento.show()

    def voltar(self):
        self.close()
        if self.tela_anterior:
            self.tela_anterior.show()
