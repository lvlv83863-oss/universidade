from modules.mysql import MySQL
from modules.aluno import Aluno

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

class Listar:
    def __init__(self, app):
        self.app = app
        self.janela = QWidget()
        self.layout = QVBoxLayout()
        self.banco = MySQL()

        self.configurar_janela()
        self.criar_componentes()
        self.carregar_dados()

    def configurar_janela(self):
        self.janela.setWindowTitle("Listagem de Alunos")

        screen = self.app.primaryScreen().geometry()
        largura = int(screen.width() * 0.6)
        altura = int(screen.height() * 0.7)

        self.janela.resize(largura, altura)
        self.janela.setLayout(self.layout)

        # 🎨 Fundo geral da janela
        self.janela.setStyleSheet("""
            QWidget {
                background-color: #f4f6f9;
                font-family: Arial;
                font-size: 14px;
                color: black;
            }
        """)

    def criar_componentes(self):

        # 📊 TABELA ESTILIZADA
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels(
            ["ID", "Nome", "Email", "CPF", "Telefone", "Matricula"]
        )

        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tabela.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #008b8b;
                border-radius: 12px;
                gridline-color: #dcdde1;
            }

            QHeaderView::section {
                background-color: #008b8b;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }

            QTableWidget::item {
                padding: 6px;
            }

            QTableWidget::item:selected {
                background-color: #b2f0f0;
                color: black;
            }
        """)

        self.layout.addWidget(self.tabela)

        # 🔵 BOTÃO ESTILIZADO
        botao_atualizar = QPushButton("Atualizar")

        botao_atualizar.setStyleSheet("""
            QPushButton {
                background-color: #008b8b;
                color: white;
                padding: 12px;
                border-radius: 12px;
                font-size: 15px;
                font-weight: bold;
                border: 2px solid #006d6d;
            }

            QPushButton:hover {
                background-color: #006d6d;
            }

            QPushButton:pressed {
                background-color: #004f4f;
            }
        """)

        self.layout.addWidget(botao_atualizar)

        botao_atualizar.clicked.connect(self.carregar_dados)

    def carregar_dados(self):

        self.banco.connect()
        alunos = Aluno.listar(self.banco)
        self.banco.disconnect()

        self.tabela.setRowCount(len(alunos))

        for linha, aluno in enumerate(alunos):
            self.tabela.setItem(linha, 0, QTableWidgetItem(str(aluno["id"])))
            self.tabela.setItem(linha, 1, QTableWidgetItem(aluno["nome"]))
            self.tabela.setItem(linha, 2, QTableWidgetItem(aluno["email"]))
            self.tabela.setItem(linha, 3, QTableWidgetItem(aluno["cpf"]))
            self.tabela.setItem(linha, 4, QTableWidgetItem(aluno["telefone"]))

            if aluno["matricula"] == True:
                self.tabela.setItem(linha, 5, QTableWidgetItem("True"))
            else:
                self.tabela.setItem(linha, 5, QTableWidgetItem("False"))