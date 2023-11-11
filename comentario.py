import datetime
class Comentario:
    def __init__(self, autor, publicacion, texto):
        self.autor = autor
        self.publicacion = publicacion
        self.texto = texto
        self.fecha = datetime.datetime.now()

    def __str__(self):
        return f"{self.autor.firstname} {self.autor.lastname}: {self.texto} ({self.fecha})"