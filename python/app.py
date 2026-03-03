from PySide6.QtWidgets import QApplication

from screen.cadastrar import Cadastrar

import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    tela = Cadastrar(app)
    tela.janela.show()

    sys.exit(tela.app.exec())