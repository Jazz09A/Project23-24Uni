class Usuario:
    def __init__(self, identification, firstname, lastname, email, username, types, departament,following):
        self.identification = identification
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.type = types
        self.following = following

class Usuario_estudiante(Usuario):
    def __init__(self, id, firstname, lastname, email, username, type, following):
        super().__init__(id, firstname, lastname, email, username, type, following)

class Usuario_Docente(Usuario):
    def __init__(self, id, firstname, lastname, email, username, type, following):
        super().__init__(id, firstname, lastname, email, username, type, department, following)
        self.department = department    