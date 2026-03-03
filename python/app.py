from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton
)
from screen.cadastrar import Cadastrar
from screen.listar import Listar

import sys

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        
        self.janela = QWidget()
        self.layout = QVBoxLayout()
        
        self.janela.setWindowTitle("Sistema Universidade")
        self.janela.resize(400, 200)
        self.janela.setLayout(self.layout)
        
        self.criar_botoes()
        
        self.janela.show()
        
    def criar_botoes(self):
        botao_listar = QPushButton("Listar")
        self.layout.addWidget(botao_listar)
        botao_listar.clicked.connect(self.abrir_listagem)
        
        
        botao_cadastrar  = QPushButton("cadastrar")
        self.layout.addWidget(botao_cadastrar)
        botao_cadastrar.clicked.connect(self.abrir_cadastro)
        
    def abrir_cadastro(self):
        self.tela_cadastro = Cadastrar(self.app)
        self.tela_cadastro.janela.show()
    
    def abrir_listagem(self):
        self.tela_listagem = Listar(self.app)
        self.tela_listagem.janela.show()


if __name__ == "__main__":
    
    system = App()
    sys.exit(system.app.exec())