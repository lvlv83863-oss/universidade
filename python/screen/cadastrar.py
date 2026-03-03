from modules.mysql import MySQL
from modules.aluno import Aluno

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)

class Cadastrar:
    def __init__(self, app):
        self.app = app
        self.janela = QWidget()
        self.layout = QVBoxLayout()
        self.banco = MySQL()

        self.campos = {}

        self.configurar_janela()
        self.criar_componentes()

    def configurar_janela(self):
        self.janela.setWindowTitle("Cadastrar Aluno")

        screen = self.app.primaryScreen().geometry()
        largura = int(screen.width() * 0.4)
        altura = int(screen.height() * 0.6)

        self.janela.resize(largura, altura)
        self.janela.setMinimumSize(400, 500)
        self.janela.setLayout(self.layout)

    def criar_componentes(self):
        componentes = {
            "nome": "Digite seu nome:",
            "email": "Digite seu email:",
            "cpf": "Digite seu cpf:",
            "telefone": "Digite seu telefone:",
            "endereco": "Digite seu endereco:"
        }

        for chave, valor in componentes.items():
            label = QLabel(valor)
            campo = QLineEdit()

            self.layout.addWidget(label)
            self.layout.addWidget(campo)

            self.campos[chave] = campo

        botao_cadastro = QPushButton("Cadastrar")
        self.layout.addWidget(botao_cadastro)

        botao_cadastro.clicked.connect(self.cadastrar)

    def validar_campos(self):
        dados = {chave: campo.text().strip() for chave, campo in self.campos.items()}

        for chave, valor in dados.items():
            if not valor:
                return False, f"O campo '{chave}' não pode estar vazio."

        if not dados["cpf"].isdigit() or len(dados["cpf"]) != 11:
            return False, "CPF deve conter exatamente 11 números."

        return True, dados

    def cadastrar(self):

        valido, resultado = self.validar_campos()

        if not valido:
            QMessageBox.warning(
                self.janela,
                "Validação",
                resultado
            )
            return

        aluno = Aluno(
            resultado["nome"],
            resultado["email"],
            resultado["cpf"],
            resultado["telefone"],
            resultado["endereco"],
        )

        try:
            self.banco.connect()
            aluno.cadastrar(self.banco)

            QMessageBox.information(
                self.janela,
                "Sucesso",
                "Aluno Cadastrado!"
            )
            self.limpar_campos()

        except Exception as e:
            QMessageBox.critical(
                self.janela,
                "Erro",
                f"Erro ao Cadastrar: {e}"
            )

        finally:
            self.banco.disconnect()

    def limpar_campos(self):
        for campo in self.campos.values():
            campo.clear()
 