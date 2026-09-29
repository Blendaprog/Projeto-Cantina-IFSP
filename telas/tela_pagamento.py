from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QRadioButton, QButtonGroup, QMessageBox, QFrame
from PySide6.QtCore import Qt


class TelaPagamento(QWidget):
    def __init__(self, banco, carrinho, tela_anterior=None):
        super().__init__()
        self.banco = banco
        self.carrinho = carrinho
        self.tela_anterior = tela_anterior
        self.setWindowTitle("Pagamento - Cantina IFSP CJO")
        self.setMinimumSize(700, 600)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(55, 35, 55, 35)
        layout.setSpacing(14)

        voltar = QPushButton("← Voltar ao pedido")
        voltar.setObjectName("voltar")
        voltar.clicked.connect(self.voltar)
        layout.addWidget(voltar)

        titulo = QLabel("PAGAMENTO")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        total = sum(item["preco"] * item["quantidade"] for item in self.carrinho)
        total_frame = QFrame()
        total_frame.setObjectName("card")
        total_layout = QVBoxLayout(total_frame)
        total_label = QLabel(f"TOTAL DO PEDIDO\nR$ {total:.2f}")
        total_label.setAlignment(Qt.AlignCenter)
        total_label.setStyleSheet("font-size: 28px; font-weight: 800; color: #164b8f;")
        total_layout.addWidget(total_label)
        layout.addWidget(total_frame)

        escolha = QLabel("Escolha a forma de pagamento:")
        escolha.setAlignment(Qt.AlignCenter)
        escolha.setStyleSheet("font-size: 17px; font-weight: 700;")
        layout.addWidget(escolha)

        self.pix = QRadioButton("📱 PIX")
        self.cartao = QRadioButton("💳 Cartão")
        self.dinheiro = QRadioButton("💵 Dinheiro")
        self.pix.setChecked(True)
        self.grupo_pagamento = QButtonGroup(self)
        for botao in (self.pix, self.cartao, self.dinheiro):
            self.grupo_pagamento.addButton(botao)
            layout.addWidget(botao)

        self.info_pagamento = QLabel("Pagamento por PIX selecionado.")
        self.info_pagamento.setAlignment(Qt.AlignCenter)
        self.info_pagamento.setObjectName("subtitulo")
        layout.addWidget(self.info_pagamento)

        self.pix.clicked.connect(lambda: self.atualizar_info("PIX"))
        self.cartao.clicked.connect(lambda: self.atualizar_info("Cartão"))
        self.dinheiro.clicked.connect(lambda: self.atualizar_info("Dinheiro"))

        confirmar = QPushButton("CONFIRMAR PAGAMENTO")
        confirmar.setMinimumHeight(58)
        confirmar.clicked.connect(self.confirmar_pagamento)
        layout.addWidget(confirmar)
        layout.addStretch()

    def atualizar_info(self, pagamento):
        self.info_pagamento.setText(f"Pagamento por {pagamento} selecionado.")

    def confirmar_pagamento(self):
        pagamento = "PIX" if self.pix.isChecked() else "Cartão" if self.cartao.isChecked() else "Dinheiro"
        pedido_id, total = self.banco.registrar_pedido(self.carrinho, pagamento)

        QMessageBox.information(
            self,
            "Pedido confirmado",
            f"Pagamento por {pagamento} confirmado!\n\n"
            f"Número do pedido: #{pedido_id}\n"
            f"Total: R$ {total:.2f}\n\n"
            "Seu pedido foi enviado para a fila."
        )

        if self.tela_anterior:
            self.tela_anterior.carrinho.clear()
            self.tela_anterior.atualizar_botao_carrinho()
            self.tela_anterior.show()
        self.close()

    def voltar(self):
        self.close()
        if self.tela_anterior:
            self.tela_anterior.show()
