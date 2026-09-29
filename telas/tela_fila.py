from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea
from PySide6.QtCore import Qt


class TelaFila(QWidget):
    """Painel interno: quem altera o status é o gestor/Pablo, não o cliente."""
    def __init__(self, banco, tela_anterior=None):
        super().__init__()
        self.banco = banco
        self.tela_anterior = tela_anterior
        self.setWindowTitle("Gestão da fila - Cantina IFSP CJO")
        self.setMinimumSize(1000, 700)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(45, 30, 45, 30)
        layout.setSpacing(12)

        voltar = QPushButton("← Voltar para a gestão")
        voltar.setObjectName("voltar")
        voltar.clicked.connect(self.voltar)
        layout.addWidget(voltar)

        titulo = QLabel("GESTÃO DA FILA")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        sub = QLabel("Painel interno do Pablo: acompanhe os pedidos e atualize cada etapa do preparo.")
        sub.setObjectName("subtitulo")
        sub.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub)

        aviso = QLabel("🔐 Somente a equipe da cantina altera o status. O cliente apenas acompanha o pedido.")
        aviso.setObjectName("aviso")
        aviso.setAlignment(Qt.AlignCenter)
        aviso.setWordWrap(True)
        layout.addWidget(aviso)

        self.area = QScrollArea()
        self.area.setWidgetResizable(True)
        self.conteudo = QWidget()
        self.layout_fila = QVBoxLayout(self.conteudo)
        self.layout_fila.setSpacing(14)
        self.area.setWidget(self.conteudo)
        layout.addWidget(self.area)

        atualizar = QPushButton("↻ ATUALIZAR FILA")
        atualizar.setObjectName("secundario")
        atualizar.setMinimumHeight(52)
        atualizar.clicked.connect(self.carregar_fila)
        layout.addWidget(atualizar)
        self.carregar_fila()

    def carregar_fila(self):
        while self.layout_fila.count():
            item = self.layout_fila.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cursor = self.banco.conexao.cursor()
        cursor.execute("""
            SELECT id, data, hora, tipo, status, total, pagamento
            FROM pedidos
            WHERE status != 'Finalizado'
            ORDER BY CASE status
                WHEN 'Recebido' THEN 1
                WHEN 'Em preparação' THEN 2
                WHEN 'Pronto' THEN 3
                ELSE 4 END, id
        """)
        pedidos = cursor.fetchall()

        if not pedidos:
            vazio = QLabel("✨ Nenhum pedido pendente no momento.\nA fila está em dia!")
            vazio.setAlignment(Qt.AlignCenter)
            vazio.setStyleSheet("font-size: 20px; padding: 55px; color: #667085;")
            self.layout_fila.addWidget(vazio)
            return

        for id_pedido, data, hora, tipo, status, total, pagamento in pedidos:
            card = QFrame()
            card.setObjectName("card")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(22, 18, 22, 18)

            topo = QHBoxLayout()
            numero = QLabel(f"PEDIDO #{id_pedido}")
            numero.setStyleSheet("font-size: 23px; font-weight: 900; color: #164b8f;")
            status_label = QLabel(status.upper())
            status_label.setObjectName("status")
            topo.addWidget(numero)
            topo.addStretch()
            topo.addWidget(status_label)
            card_layout.addLayout(topo)

            info = QLabel(f"Recebido em {data} às {hora}  •  {tipo}  •  {pagamento}  •  R$ {total:.2f}")
            info.setObjectName("subtitulo")
            card_layout.addWidget(info)

            instru = QLabel("Atualizar etapa:")
            instru.setStyleSheet("font-weight: 800; color: #18233a;")
            card_layout.addWidget(instru)

            botoes = QHBoxLayout()
            botoes.setSpacing(8)
            for texto, novo_status in (
                ("RECEBIDO", "Recebido"),
                ("EM PREPARAÇÃO", "Em preparação"),
                ("PRONTO", "Pronto"),
                ("FINALIZADO", "Finalizado")
            ):
                botao = QPushButton(texto)
                botao.clicked.connect(lambda _, i=id_pedido, s=novo_status: self.alterar_status(i, s))
                botoes.addWidget(botao)
            card_layout.addLayout(botoes)
            self.layout_fila.addWidget(card)

        self.layout_fila.addStretch()

    def alterar_status(self, id_pedido, novo_status):
        cursor = self.banco.conexao.cursor()
        cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (novo_status, id_pedido))
        self.banco.conexao.commit()
        self.carregar_fila()

    def voltar(self):
        self.close()
        if self.tela_anterior:
            self.tela_anterior.show()
