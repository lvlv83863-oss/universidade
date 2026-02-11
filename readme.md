 #  Projetos Universidade

 Modelagem em orientação à Objetos das Entidades Alunos, Cursos e Temas.

 ## Caso de Uso

 ```mermaid
flowchart LR
    Usuario([Secretaria])

    UC1((Cadastrar Alunos))
    UC2((Editar Alunos))
    UC3((Transferir Alunos))

    Usuario --> UC1
    Usuario --> UC2
    Usuario --> UC3
 ```
 ## Diagrama de Classes

 ```mermaid
 classDiagram
    class Aluno{
        - nome
        - email
        - cpf
        - telefone
        - endereço
        - matricula
        + cadastrar()
        + editar()
        + transferir()
    }
 ```

 ## Dependências

 -**VScodeIDE**: (Interface de Desenvolvimento).

 - **Mermaid**: Linguagem para confecção de Digramas em documentos MD (Mark Down).

-**Material Icon Theme**: Tema para colorir as pastas.

-**Gt Lens**: Interface gráfica pra o versionamento. git integrado ao VScode.