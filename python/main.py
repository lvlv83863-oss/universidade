from modules.aluno import Aluno
from modules.mysql import MySQL

banco = MySQL(
    '127.0.0.1',
    'root',
    '',
    'universidade'
)

banco.connect()

aluno = Aluno(
    "José Maria",
    "jose.maria@email.com",
    "98765432110",
    "031944445555",
    "Rua Paineiras, Eldorado, 3000"
)

query = aluno.cadastrar(banco)

banco.disconnect()