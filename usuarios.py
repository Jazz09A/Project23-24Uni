import datetime
from publicaciones import Publicacion
from comentario import Comentario
class Usuario:
    def __init__(self, identification, firstname, lastname, email, username, types, departament, following):
        self.identification = identification
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.type = types
        self.departament = departament
        self.following = following
        self.publicaciones = [] 

    def registrar_profesor(self, identification, firstname, lastname, email, username, department):
        nuevo_profesor = Profesor(identification, firstname, lastname, email, username, "profesor", department, [])
        return nuevo_profesor

    def registrar_estudiante(self, identification, firstname, lastname, email, username, major):
        nuevo_estudiante = Estudiante(identification, firstname, lastname, email, username, "estudiante", major, [])
        return nuevo_estudiante
    @classmethod
    def buscar_por_username(cls, username, datos):
        for usuario in datos:
            if username == usuario.username:
                return usuario
        return None  # Retorna None si el usuario no se encuentra
   
    def buscar_por_departamento_o_carrera(self,tipo,datos):
        perfiles_encontrados = []
        if tipo == "1":
            departamento = input("Ingrese el departamento: ")
            for usuario in datos:
                if usuario.departament == departamento:
                    perfiles_encontrados.append(usuario)
        elif tipo == "2":
            carrera = input("Ingrese la carrera: ")
            for usuario in datos:
                if usuario.major == carrera:
                    perfiles_encontrados.append(usuario)
        return perfiles_encontrados
    
    def actualizar_informacion(self, firstname, lastname, email, new_username, departament, major):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = new_username
        self.departament = departament
        self.major = major
    

    @staticmethod
    def eliminar_cuenta(username,usuarios):
        for usuario in usuarios:
            if username == usuario.username:
                usuarios.remove(usuario)
                print("Cuenta eliminada exitosamente.")
                return  
        print("Perfil no encontrado.")

    def mostrar_perfil(self,username,usuarios,publicaciones):
        usuario = self.buscar_por_username(username,usuarios)
        publicaciones_encontradas = []
        for publicacion in publicaciones:
            if publicacion.publicacion == usuario.identification:
                publicaciones_encontradas.append(publicacion)
            else:
                print("No hay publicaciones encontradas")
        return publicaciones_encontradas
        
    def subir_publicacion(self, tipo, descripcion, hashtags):
        nueva_publicacion = Publicacion(self.identification, tipo, descripcion, hashtags, datetime.datetime.now(),multimedia={})
        return nueva_publicacion

    @staticmethod
    def obtener_usuario_actual(usuarios):
        username = input("Ingresa tu nombre de usuario: ")
        
        for usuario in usuarios:
            if usuario.username == username:
                return usuario

        print("Usuario no encontrado. Por favor, verifica tu nombre de usuario.")
        return None
    @staticmethod
    def buscar_publicaciones_por_usuario(usuarios, username):
        publicaciones_usuario = []
        for usuario in usuarios:
            if usuario.username == username:
                publicaciones_usuario.extend(usuario.publicaciones)
        return publicaciones_usuario

    @staticmethod
    def buscar_publicaciones_por_hashtags(publicaciones, hashtag):
        publicaciones_hashtags = []
        for publicacion in publicaciones:
            if hashtag in publicacion.tags:
                publicaciones_hashtags.append(publicacion)
        return publicaciones_hashtags
    
    def ver_publicaciones(self, usuario_a_seguir):
        # Verificar si el usuario actual sigue al usuario a seguir
        if usuario_a_seguir.identification in self.following:
            print(f"Publicaciones de {usuario_a_seguir.username}:")
            for publicacion in usuario_a_seguir.publicaciones:
                print(f"Tipo: {publicacion.tipo}")
                print(f"Descripción: {publicacion.descripcion}")
                print(f"Fecha: {publicacion.fecha}")
                print(f"Tags: {', '.join(publicacion.tags)}")
                print(f"Multimedia: {publicacion.multimedia['url']}")
                print(f"Likes: {len(publicacion.likes)}")
                print("Comentarios:")
                for comentario in publicacion.comentarios:
                    print(comentario)
                print("--------")
        else:
            print(f"No puedes ver las publicaciones de {usuario_a_seguir.username} porque no lo sigues.")
    
    def aprobar_seguidor(self, solicitante):
        if self.carrera == solicitante.carrera:
            # Si estudian la misma carrera, el seguimiento se aprueba automáticamente
            return True
        else:
            # Aquí podrías implementar una lógica más avanzada, como notificar al usuario
            # propietario de la cuenta para que apruebe o rechace la solicitud.
            # Por simplicidad, aquí simplemente preguntamos al usuario si desea aprobar.
            respuesta = input(f"{solicitante.nombre} solicita seguirte. ¿Aprobar la solicitud? (Sí/No): ")
            if respuesta.lower() == "si":
                return True
            else:
                return False
    
    def seguir_usuario(self, otro_usuario):
        if self.carrera == otro_usuario.carrera:
            # Si estudian la misma carrera, el follow es automático
            self.seguidos.append(otro_usuario)
            print(f"Ahora sigues a {otro_usuario.nombre}.")
        else:
            # Necesita aprobación si no estudian la misma carrera
            if otro_usuario.aprobar_seguidor(self):
                self.seguidos.append(otro_usuario)
                print(f"Ahora sigues a {otro_usuario.nombre}.")
            else:
                print(f"{otro_usuario.nombre} rechazó tu solicitud para seguirlo.")
        
    def comentar_publicacion(self, publicacion, texto):
        nuevo_comentario = Comentario(self, publicacion, texto)
        publicacion.comentarios.append(nuevo_comentario)
        print("Comentario agregado exitosamente.")
    
    def dar_like(self, publicacion):
        if self in publicacion.likes:
            # Si ya le dio like, quitarlo
            publicacion.likes.remove(self)
            print("Le diste dislike a la publicación.")
        else:
            publicacion.likes.append(self)
            print("Le diste like a la publicación.")
    
        

# Clase para representar un Profesor
class Profesor(Usuario):
    def __init__(self, id, firstName, lastName, email, username, department, following):
        super().__init__(id, firstName, lastName, email, username, "profesor", department, following)
        self.department = department

# Clase para representar un Estudiante
class Estudiante(Usuario):
    def __init__(self, id, firstName, lastName, email, username, major, following):
        super().__init__(id, firstName, lastName, email, username, "estudiante", major, following)
        self.major = major


