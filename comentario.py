import datetime
class Comentario:
    def __init__(self, autor, publicacion, texto):
        self.autor = autor
        self.publicacion = publicacion
        self.texto = texto
        self.fecha = datetime.datetime.now()
