from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtCore import Qt


class TelaGestor(QWidget):
    def __init__(self, banco, tela_anterior=None):
        super().__init__()
        self.banco = banco
        self.tela_anterior = tela_anterior
        self.setWindowTitle("Área do Gestor - Cantina IFSP CJO")
        self.setMinimumSize(900, 650)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 35, 50, 35)
        layout.setSpacing(16)

        voltar = QPushButton("← Voltar")
        voltar.setObjectName("voltar")
        voltar.clicked.connect(self.voltar)
        layout.addWidget(voltar)

        titulo = QLabel("ÁREA DO PABLO")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        sub = QLabel("Painel interno para o Pablo administrar a fila e o financeiro da cantina.")
        sub.setObjectName("subtitulo")
        sub.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub)
        layout.addSpacing(25)

        linha = QHBoxLayout()
        linha.setSpacing(18)

        fila = self.criar_botao("📋", "FILA DE PEDIDOS", "Gerencie os pedidos e seus status.")
        financeiro = self.criar_botao("💰", "FINANCEIRO", "Consulte receitas, despesas e saldo.")
        fila.clicked.connect(self.abrir_fila)
        financeiro.clicked.connect(self.abrir_financeiro)
        linha.addWidget(fila)
        linha.addWidget(financeiro)
        layout.addLayout(linha)
        layout.addStretch()

    def criar_botao(self, icone, titulo, descricao):
        botao = QPushButton()
        botao.setObjectName("secundario")
        botao.setMinimumHeight(160)
        botao.setText(f"{icone}\n{titulo}\n{descricao}")
        botao.setStyleSheet("QPushButton { font-size: 16px; line-height: 1.5; }")
        return botao

    def abrir_fila(self):
        from telas.tela_fila import TelaFila
        self.tela = TelaFila(self.banco, self)
        self.tela.show()
        self.hide()

    def abrir_financeiro(self):
        from telas.tela_financiamento import TelaFinanceiro
        self.tela = TelaFinanceiro(self.banco, self)
        self.tela.show()
        self.hide()

    def voltar(self):
        self.close()
        if self.tela_anterior:
            self.tela_anterior.show()
