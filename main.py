import sys
from PySide6.QtWidgets import QApplication

from banco import Banco
from telas.tela_inicio import TelaInicio


ESTILO = """
QWidget {
    background: #f7f9ff;
    color: #18233a;
    font-family: "Segoe UI";
    font-size: 15px;
}
QLabel#titulo {
    color: #164b8f;
    font-size: 34px;
    font-weight: 900;
}
QLabel#subtitulo {
    color: #667085;
    font-size: 16px;
}
QLabel#aviso {
    background: #fff0f7;
    color: #a31d61;
    border: 1px solid #f4b4d2;
    border-radius: 12px;
    padding: 11px 16px;
    font-weight: 700;
}
QPushButton {
    background: #e83e8c;
    color: white;
    border: none;
    border-radius: 14px;
    padding: 13px 20px;
    font-weight: 800;
    min-height: 42px;
}
QPushButton:hover { background: #d92f7d; }
QPushButton:pressed { background: #b92568; }
QPushButton#secundario {
    background: #e8f1ff;
    color: #164b8f;
    border: 2px solid #c7dcff;
}
QPushButton#secundario:hover { background: #d9e8ff; border-color: #9ec1fa; }
QPushButton#voltar {
    background: transparent;
    color: #164b8f;
    text-align: left;
    padding: 8px 4px;
    border-radius: 10px;
    min-height: 30px;
}
QPushButton#voltar:hover { background: #eaf2ff; }
QPushButton#carrinho {
    background: #164b8f;
    border-radius: 16px;
    min-height: 56px;
    font-size: 17px;
}
QPushButton#carrinho:hover { background: #103b73; }
QPushButton#destaque {
    background: white;
    color: #164b8f;
}
QFrame#destaque {
    background: white;
    border: 1px solid #e0e7f2;
    border-radius: 24px;
}
QFrame#card {
    background: white;
    border: 1px solid #e0e7f2;
    border-radius: 18px;
}
QFrame#card:hover { border: 2px solid #f1a4c7; }
QLabel#status {
    background: #fff0f7;
    color: #c42673;
    border-radius: 10px;
    padding: 7px 12px;
    font-weight: 900;
}
QScrollArea { border: none; background: transparent; }
QLineEdit {
    background: white;
    color: #18233a;
    border: 2px solid #d8e0ec;
    border-radius: 13px;
    padding: 12px;
    font-size: 17px;
}
QLineEdit:focus { border: 2px solid #5c94e8; }
QRadioButton {
    background: white;
    border: 1px solid #dbe3ef;
    border-radius: 12px;
    padding: 13px;
}
QRadioButton:checked {
    border: 2px solid #e83e8c;
    background: #fff3f8;
}
QMessageBox QPushButton { min-width: 90px; }
"""


app = QApplication(sys.argv)
app.setStyleSheet(ESTILO)

banco = Banco()
banco.cadastrar_produtos_iniciais()

tela = TelaInicio(banco)
tela.show()

sys.exit(app.exec())
