from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtCore import Qt


class TelaInicio(QWidget):
    def __init__(self, banco):
        super().__init__()
        self.banco = banco
        self.setWindowTitle("Cantina IFSP CJO")
        self.setMinimumSize(1000, 700)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(80, 55, 80, 55)
        layout.setSpacing(16)

        logo = QLabel("🍔  CANTINA IFSP CJO  🥤")
        logo.setObjectName("titulo")
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        subtitulo = QLabel("Peça, pague e acompanhe — tudo em um só lugar.")
        subtitulo.setObjectName("subtitulo")
        subtitulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitulo)
        layout.addSpacing(28)

        destaque = QFrame()
        destaque.setObjectName("card")
        destaque_layout = QVBoxLayout(destaque)
        destaque_layout.setContentsMargins(35, 30, 35, 30)

        texto = QLabel("O QUE VOCÊ QUER FAZER?")
        texto.setAlignment(Qt.AlignCenter)
        texto.setStyleSheet("font-size: 20px; font-weight: 800; color: #164b8f;")
        destaque_layout.addWidget(texto)

        botoes = QHBoxLayout()
        botoes.setSpacing(15)

        pedido = QPushButton("🛒\nFAZER PEDIDO\n• Monte seu pedido")
        pedido.setMinimumHeight(105)
        pedido.clicked.connect(self.abrir_totem)

        acompanhar = QPushButton("📋\nACOMPANHAR PEDIDO\n• Consulte sua senha")
        acompanhar.setObjectName("secundario")
        acompanhar.setMinimumHeight(105)
        acompanhar.clicked.connect(self.abrir_acompanhar)

        gestor = QPushButton("👨‍💼\nÁREA DO PABLO\n• Fila e financeiro")
        gestor.setObjectName("secundario")
        gestor.setMinimumHeight(105)
        gestor.clicked.connect(self.abrir_gestor)

        botoes.addWidget(pedido)
        botoes.addWidget(acompanhar)
        botoes.addWidget(gestor)
        destaque_layout.addLayout(botoes)
        layout.addWidget(destaque)

        rodape = QLabel("Sistema de pedidos e gestão • Projeto Final – 3º Bimestre")
        rodape.setObjectName("subtitulo")
        rodape.setAlignment(Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(rodape)

    def abrir_totem(self):
        from telas.tela_totem import TelaTotem
        self.tela_totem = TelaTotem(self.banco, self)
        self.tela_totem.show()
        self.hide()

    def abrir_acompanhar(self):
        from telas.tela_acompanhar import TelaAcompanhar
        self.tela_acompanhar = TelaAcompanhar(self.banco, self)
        self.tela_acompanhar.show()
        self.hide()

    def abrir_gestor(self):
        from telas.tela_gestor import TelaGestor
        self.tela_gestor = TelaGestor(self.banco, self)
        self.tela_gestor.show()
        self.hide()
