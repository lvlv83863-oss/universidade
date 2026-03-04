from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton
)
from PySide6.QtCore import Qt, QTimer, QRect, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QBrush, QLinearGradient, QRadialGradient

from screen.cadastrar import Cadastrar
from screen.listar import Listar

import sys
import random


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema Universidade")
        self.resize(600, 400)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(25)

        self.explodindo = False
        self.particulas = []
        self.destino = None

        self.criar_bolhas()

        self.timer = QTimer()
        self.timer.timeout.connect(self.animar)
        self.timer.start(30)

        self.criar_botoes()

    # ---------------- BOTÕES ----------------
    def criar_botoes(self):
        self.botao_listar = QPushButton("Listar")
        self.botao_cadastrar = QPushButton("Cadastrar")

        for botao in [self.botao_listar, self.botao_cadastrar]:

            botao.setFixedSize(230, 60)

            botao.setStyleSheet("""
                QPushButton {
                    background-color: #1ee3e3;
                    color: #003f3f;
                    font-size: 17px;
                    font-weight: bold;
                    border-radius: 18px;
                    border: 3px solid #007777;
                }

                QPushButton:hover {
                    background-color: #5efefe;
                    border: 3px solid #004f4f;
                }

                QPushButton:pressed {
                    background-color: #a0ffff;
                    border: 3px solid #003f3f;
                }
            """)

            botao.clicked.connect(self.acao_com_explosao)
            self.layout.addWidget(botao)

    # ---------------- AÇÃO COM DELAY ----------------
    def acao_com_explosao(self):
        botao = self.sender()

        if botao == self.botao_listar:
            self.destino = "listar"
        else:
            self.destino = "cadastrar"

        anim = QPropertyAnimation(botao, b"geometry")
        anim.setDuration(180)
        anim.setEasingCurve(QEasingCurve.OutBack)

        rect = botao.geometry()

        anim.setStartValue(rect)
        anim.setEndValue(QRect(
            rect.x() - 6,
            rect.y() - 6,
            rect.width() + 12,
            rect.height() + 12
        ))
        anim.start()

        self.criar_explosao()

        QTimer.singleShot(1000, self.abrir_destino)

    # ---------------- EXPLOSÃO ----------------
    def criar_explosao(self):
        self.particulas = []

        for bolha in self.bolhas:
            for _ in range(8):
                self.particulas.append({
                    "x": bolha["x"],
                    "y": bolha["y"],
                    "dx": random.uniform(-5, 5),
                    "dy": random.uniform(-5, 5),
                    "vida": random.randint(20, 40),
                    "cor": bolha["cor"]
                })

        self.explodindo = True

    # ---------------- ANIMAÇÃO ----------------
    def animar(self):

        if not self.explodindo:
            for bolha in self.bolhas:
                bolha["y"] -= bolha["velocidade"]

                if bolha["y"] < -60:
                    bolha["y"] = self.height() + 60
                    bolha["x"] = random.randint(0, self.width())

        else:
            for p in self.particulas:
                p["x"] += p["dx"]
                p["y"] += p["dy"]
                p["vida"] -= 1

            self.particulas = [p for p in self.particulas if p["vida"] > 0]

            if not self.particulas:
                self.explodindo = False
                self.criar_bolhas()

        self.update()

    # ---------------- BOLHAS AZUL CLARO E BRANCO ----------------
    def criar_bolhas(self):
        self.bolhas = []

        paleta = [
            QColor(200, 240, 255, 170),
            QColor(180, 230, 255, 160),
            QColor(220, 250, 255, 150),
            QColor(255, 255, 255, 180),
            QColor(210, 245, 255, 140)
        ]

        for _ in range(25):
            cor = random.choice(paleta)

            self.bolhas.append({
                "x": random.randint(0, self.width()),
                "y": random.randint(0, self.height()),
                "raio": random.randint(30, 60),
                "velocidade": random.uniform(0.5, 1.2),
                "cor": cor
            })

    # ---------------- DESENHO ----------------
    def paintEvent(self, event):
        painter = QPainter(self)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#00e5e5"))
        gradient.setColorAt(1, QColor("#002f2f"))
        painter.fillRect(self.rect(), gradient)

        if not self.explodindo:
            for bolha in self.bolhas:

                grad = QRadialGradient(
                    bolha["x"],
                    bolha["y"],
                    bolha["raio"]
                )

                grad.setColorAt(0, QColor(255, 255, 255, 220))
                grad.setColorAt(0.4, bolha["cor"])
                grad.setColorAt(1, QColor(
                    max(bolha["cor"].red() - 40, 0),
                    max(bolha["cor"].green() - 40, 0),
                    max(bolha["cor"].blue() - 40, 0),
                    120
                ))

                painter.setBrush(QBrush(grad))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(
                    int(bolha["x"] - bolha["raio"] / 2),
                    int(bolha["y"] - bolha["raio"] / 2),
                    bolha["raio"],
                    bolha["raio"]
                )
        else:
            painter.setPen(Qt.NoPen)
            for p in self.particulas:
                painter.setBrush(p["cor"])
                painter.drawEllipse(int(p["x"]), int(p["y"]), 5, 5)

    # ---------------- ABRIR DESTINO ----------------
    def abrir_destino(self):

        if self.destino == "listar":
            self.tela_listagem = Listar(QApplication.instance())
            self.tela_listagem.janela.show()

        elif self.destino == "cadastrar":
            self.tela_cadastro = Cadastrar(QApplication.instance())
            self.tela_cadastro.janela.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = App()
    janela.show()
    sys.exit(app.exec())