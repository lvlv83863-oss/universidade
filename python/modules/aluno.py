from modules.mysql import MySQL

class Aluno:
    def __init__(self, nome, email, cpf, telefone, endereco):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.telefone = telefone
        self.endereco = endereco
        self.matricula = True

    def cadastrar(self, db=MySQL()):
        query = """
            INSERT INTO alunos (
                nome,
                email,
                cpf,
                telefone,
                endereco
            ) VALUES (
                %s,%s,%s,%s,%s
                )
            """
        values = (
                self.nome,
                self.email,
                self.cpf,
                self.telefone,
                self.endereco
            )
        

        return db.execute_query(query, values)

    def editar(self):
        pass

    def transferir(self):
        pass