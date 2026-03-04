from modules.mysql import MySQL
from modules.aluno import Aluno

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFrame
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QBrush
import math


# ---------------- FUNDO ANIMADO ----------------
class FundoAnimado(QWidget):
    def __init__(self):
        super().__init__()
        self.offset = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_animacao)
        self.timer.start(30)

    def atualizar_animacao(self):
        self.offset += 0.1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Degradê azul ciano
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#00c9c9"))
        gradient.setColorAt(1, QColor("#005f5f"))

        painter.fillRect(self.rect(), gradient)

        # Ondas animadas
        painter.setBrush(QColor(255, 255, 255, 40))
        painter.setPen(Qt.NoPen)

        for i in range(3):
            path = []
            for x in range(0, self.width(), 10):
                y = 50 * math.sin((x / 100) + self.offset + i) + (self.height() / 2)
                path.append((x, y))

            for x, y in path:
                painter.drawEllipse(int(x), int(y), 8, 8)


# ---------------- TELA CADASTRO ----------------
class Cadastrar:
    def __init__(self, app):
        self.app = app
        self.janela = FundoAnimado()
        self.layout_principal = QVBoxLayout(self.janela)
        self.banco = MySQL()

        self.campos = {}

        self.configurar_janela()
        self.criar_componentes()

    def configurar_janela(self):
        self.janela.setWindowTitle("Cadastrar Aluno")

        screen = self.app.primaryScreen().geometry()
        largura = int(screen.width() * 0.6)
        altura = int(screen.height() * 0.85)

        self.janela.resize(largura, altura)
        self.janela.setMinimumSize(750, 800)

        self.layout_principal.setAlignment(Qt.AlignCenter)

    def criar_componentes(self):

        # -------- TÍTULO --------
        titulo_principal = QLabel("Área de Cadastro")
        titulo_principal.setAlignment(Qt.AlignCenter)
        titulo_principal.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: white;
            margin-bottom: 20px;
        """)
        self.layout_principal.addWidget(titulo_principal)

        # -------- CARD --------
        card = QFrame()
        card.setFixedWidth(600)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 18px;
                padding: 40px;
            }
        """)

        layout_card = QVBoxLayout()
        layout_card.setSpacing(20)
        card.setLayout(layout_card)

        componentes = {
            "nome": "Nome",
            "email": "Email",
            "cpf": "CPF",
            "telefone": "Telefone",
            "endereco": "Endereço"
        }

        for chave, texto in componentes.items():
            label = QLabel(texto)
            label.setStyleSheet("font-weight: bold; color: black; font-size:16px;")

            campo = QLineEdit()
            campo.setMinimumHeight(50)
            campo.setPlaceholderText(f"Digite seu {texto.lower()}")

            campo.setStyleSheet("""
    QLineEdit {
        background-color: #e9ecef;   /* Cinza claro */
        padding: 14px;
        border: 2px solid #cfd4da;
        border-radius: 12px;
        color: black;               /* Letras pretas */
        font-size: 16px;
    }
    QLineEdit:focus {
        background-color: #f1f3f5;  /* Cinza um pouco mais claro ao focar */
        border: 2px solid #008b8b;  /* Destaque ciano */
    }
""")

            layout_card.addWidget(label)
            layout_card.addWidget(campo)

            self.campos[chave] = campo

        # 🔥 Espaçamento maior antes do botão
        layout_card.addSpacing(35)

        # -------- BOTÃO --------
        botao_cadastro = QPushButton("Cadastrar")
        botao_cadastro.setCursor(Qt.PointingHandCursor)
        botao_cadastro.setMinimumHeight(60)

        botao_cadastro.setStyleSheet("""
            QPushButton {
                background-color: #007c7c;
                color: white;
                border: 4px solid #004f4f;
                border-radius: 15px;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #009090;
            }
            QPushButton:pressed {
                background-color: #005f5f;
            }
        """)

        layout_card.addWidget(botao_cadastro)

        self.layout_principal.addWidget(card)

        botao_cadastro.clicked.connect(self.cadastrar)

    # -------- LÓGICA --------

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
            QMessageBox.warning(self.janela, "Validação", resultado)
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

            QMessageBox.information(self.janela, "Sucesso", "Aluno Cadastrado!")
            self.limpar_campos()

        except Exception as e:
            QMessageBox.critical(self.janela, "Erro", f"Erro ao Cadastrar: {e}")

        finally:
            self.banco.disconnect()

    def limpar_campos(self):
        for campo in self.campos.values():
            campo.clear()