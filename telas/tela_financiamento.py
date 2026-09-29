from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QLineEdit, QMessageBox
from PySide6.QtCore import Qt
from datetime import datetime


class TelaFinanceiro(QWidget):
    def __init__(self, banco, tela_anterior=None):
        super().__init__()
        self.banco = banco
        self.tela_anterior = tela_anterior
        self.setWindowTitle("Financeiro - Cantina IFSP CJO")
        self.setMinimumSize(950, 680)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(45, 30, 45, 30)
        layout.setSpacing(12)

        voltar = QPushButton("← Voltar")
        voltar.setObjectName("voltar")
        voltar.clicked.connect(self.voltar)
        layout.addWidget(voltar)

        titulo = QLabel("CONTROLE FINANCEIRO")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        sub = QLabel("Consulte receitas, despesas e o saldo da cantina.")
        sub.setObjectName("subtitulo")
        sub.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub)

        resumo = QHBoxLayout()
        self.card_receitas = self.criar_card("RECEITAS", "R$ 0,00")
        self.card_despesas = self.criar_card("DESPESAS", "R$ 0,00")
        self.card_saldo = self.criar_card("SALDO", "R$ 0,00")
        resumo.addWidget(self.card_receitas)
        resumo.addWidget(self.card_despesas)
        resumo.addWidget(self.card_saldo)
        layout.addLayout(resumo)

        titulo_despesa = QLabel("CADASTRAR DESPESA")
        titulo_despesa.setStyleSheet("font-size: 20px; font-weight: 800; margin-top: 15px;")
        layout.addWidget(titulo_despesa)

        self.campo_descricao = QLineEdit()
        self.campo_descricao.setPlaceholderText("Descrição da despesa")
        self.campo_valor = QLineEdit()
        self.campo_valor.setPlaceholderText("Valor (ex.: 25,50)")
        layout.addWidget(self.campo_descricao)
        layout.addWidget(self.campo_valor)

        botoes = QHBoxLayout()
        adicionar = QPushButton("ADICIONAR DESPESA")
        atualizar = QPushButton("↻ ATUALIZAR DADOS")
        atualizar.setObjectName("secundario")
        adicionar.setMinimumHeight(48)
        atualizar.setMinimumHeight(48)
        adicionar.clicked.connect(self.adicionar_despesa)
        atualizar.clicked.connect(self.atualizar_financeiro)
        botoes.addWidget(adicionar)
        botoes.addWidget(atualizar)
        layout.addLayout(botoes)
        layout.addStretch()
        self.atualizar_financeiro()

    def criar_card(self, titulo, valor):
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)
        label_titulo = QLabel(titulo)
        label_titulo.setAlignment(Qt.AlignCenter)
        label_titulo.setStyleSheet("font-size: 16px; font-weight: 800;")
        label_valor = QLabel(valor)
        label_valor.setAlignment(Qt.AlignCenter)
        label_valor.setStyleSheet("font-size: 25px; font-weight: 800; color: #164b8f;")
        layout.addWidget(label_titulo)
        layout.addWidget(label_valor)
        card.valor_label = label_valor
        return card

    def adicionar_despesa(self):
        descricao = self.campo_descricao.text().strip()
        valor_texto = self.campo_valor.text().strip()
        if not descricao or not valor_texto:
            QMessageBox.warning(self, "Atenção", "Preencha a descrição e o valor.")
            return
        try:
            valor = float(valor_texto.replace(",", "."))
        except ValueError:
            QMessageBox.warning(self, "Erro", "Digite um valor válido.")
            return
        if valor <= 0:
            QMessageBox.warning(self, "Erro", "O valor deve ser maior que zero.")
            return

        cursor = self.banco.conexao.cursor()
        cursor.execute("INSERT INTO despesas (descricao, valor, data) VALUES (?, ?, ?)",
                       (descricao, valor, datetime.now().strftime("%d/%m/%Y")))
        self.banco.conexao.commit()
        self.campo_descricao.clear()
        self.campo_valor.clear()
        QMessageBox.information(self, "Sucesso", "Despesa cadastrada com sucesso!")
        self.atualizar_financeiro()

    def atualizar_financeiro(self):
        cursor = self.banco.conexao.cursor()
        cursor.execute("SELECT COALESCE(SUM(valor), 0) FROM despesas")
        despesas = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(SUM(total), 0) FROM pedidos WHERE status != 'Cancelado'")
        receitas = cursor.fetchone()[0]
        saldo = receitas - despesas
        self.card_receitas.valor_label.setText(f"R$ {receitas:.2f}")
        self.card_despesas.valor_label.setText(f"R$ {despesas:.2f}")
        self.card_saldo.valor_label.setText(f"R$ {saldo:.2f}")

    def voltar(self):
        self.close()
        if self.tela_anterior:
            self.tela_anterior.show()
