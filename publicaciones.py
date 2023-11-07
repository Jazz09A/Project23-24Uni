class Publicacion:
    def __init__(self, usuario, tipo, descripcion, tags, fecha,multimedia):
        self.usuario = usuario  # El usuario que sube la publicación
        self.tipo = tipo
        self.descripcion = descripcion
        self.tags = tags
        self.fecha = fecha
        self.multimedia = multimedia
        self.likes = []  # Lista de usuarios que dieron like
        self.comentarios = []  # Lista de comentarios

    def dar_like(self, usuario):
        self.likes.append(usuario)

    def agregar_comentario(self, usuario, comentario):
        comentario_str = f"{usuario.username}: {comentario}"
        self.comentarios.append(comentario_str)

    def ver_publicaciones(self,usuario_A, usuario_B,publicaciones):
        if usuario_B.identification in usuario_A.following:
            for publicacion in publicaciones:  # Recorre todas las publicaciones
                if publicacion.usuario == usuario_B:
                    print(f"Descripción: {publicacion.descripcion}")
                    print(f"Fecha: {publicacion.fecha}")
                    print(f"Likes: {', '.join([u.username for u in publicacion.likes])}")
                    print(f"Comentarios:")
                    for comentario in publicacion.comentarios:
                        print(f"- {comentario}")
                    print("-" * 40)
        else:
            print(f"{usuario_A.username} no sigue a {usuario_B.username}.")
        
        def eliminar_comentario(self, comentario):
            if comentario in self.comentarios:
                if comentario.autor == self.usuario:
                    self.comentarios.remove(comentario)
                    print("Comentario eliminado.")
                else:
                    print("No tienes permiso para eliminar este comentario.")
            else:
                print("Comentario no encontrado en esta publicación.")
