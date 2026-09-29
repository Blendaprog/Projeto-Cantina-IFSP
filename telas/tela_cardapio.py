from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QScrollArea
)
from PySide6.QtCore import Qt


class TelaCardapio(QWidget):
    def __init__(self, banco, tela_anterior=None):
        super().__init__()

        self.banco = banco
        self.tela_anterior = tela_anterior

        self.setWindowTitle("Cardápio - Cantina IFSP CJO")
        self.setMinimumSize(1000, 700)

        layout_principal = QVBoxLayout()

        # BOTÃO VOLTAR

        botao_voltar = QPushButton("← VOLTAR")
        botao_voltar.setMinimumHeight(50)
        botao_voltar.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
        """)

        botao_voltar.clicked.connect(
            self.voltar
        )

        layout_principal.addWidget(
            botao_voltar
        )

        # TÍTULO

        titulo = QLabel("CARDÁPIO")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 34px;
            font-weight: bold;
        """)

        layout_principal.addWidget(titulo)

        subtitulo = QLabel(
            "Confira os produtos disponíveis na Cantina IFSP CJO"
        )

        subtitulo.setAlignment(
            Qt.AlignCenter
        )

        subtitulo.setStyleSheet("""
            font-size: 18px;
        """)

        layout_principal.addWidget(
            subtitulo
        )

        # ÁREA DOS PRODUTOS

        area = QScrollArea()
        area.setWidgetResizable(True)

        conteudo = QWidget()
        layout_produtos = QVBoxLayout()

        produtos = self.banco.buscar_produtos()

        categoria_atual = ""

        linha = None
        quantidade = 0

        for id_produto, nome, categoria, preco in produtos:

            if categoria != categoria_atual:

                categoria_atual = categoria

                titulo_categoria = QLabel(
                    categoria.upper()
                )

                titulo_categoria.setStyleSheet("""
                    font-size: 24px;
                    font-weight: bold;
                    margin-top: 20px;
                """)

                layout_produtos.addWidget(
                    titulo_categoria
                )

                linha = QHBoxLayout()

                layout_produtos.addLayout(
                    linha
                )

                quantidade = 0

            card = QFrame()

            card.setFrameShape(
                QFrame.StyledPanel
            )

            card.setMinimumSize(
                220,
                150
            )

            layout_card = QVBoxLayout()

            nome_produto = QLabel(
                nome
            )

            nome_produto.setAlignment(
                Qt.AlignCenter
            )

            nome_produto.setWordWrap(
                True
            )

            nome_produto.setStyleSheet("""
                font-size: 17px;
                font-weight: bold;
            """)

            preco_produto = QLabel(
                f"R$ {preco:.2f}"
            )

            preco_produto.setAlignment(
                Qt.AlignCenter
            )

            preco_produto.setStyleSheet("""
                font-size: 18px;
            """)

            botao = QPushButton(
                "ADICIONAR AO PEDIDO"
            )

            botao.clicked.connect(
                lambda _, id=id_produto,
                n=nome,
                p=preco:
                self.adicionar_produto(
                    id,
                    n,
                    p
                )
            )

            layout_card.addWidget(
                nome_produto
            )

            layout_card.addWidget(
                preco_produto
            )

            layout_card.addWidget(
                botao
            )

            card.setLayout(
                layout_card
            )

            linha.addWidget(
                card
            )

            quantidade += 1

            if quantidade == 4:

                linha = QHBoxLayout()

                layout_produtos.addLayout(
                    linha
                )

                quantidade = 0

        conteudo.setLayout(
            layout_produtos
        )

        area.setWidget(
            conteudo
        )

        layout_principal.addWidget(
            area
        )

        self.setLayout(
            layout_principal
        )

    def adicionar_produto(
        self,
        id_produto,
        nome,
        preco
    ):

        print(
            f"Produto selecionado: {nome}"
        )

    def voltar(self):

        self.close()

        if self.tela_anterior:
            self.tela_anterior.show()