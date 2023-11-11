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
        self.solicitudes_pendientes = []

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
    
    def seguir_usuario(self, otro_usuario):
        if isinstance(self, Estudiante) and isinstance(otro_usuario, Estudiante):
            if self.major == otro_usuario.major:
                # Si estudian la misma carrera, el follow es automático
                self.following.append(otro_usuario.identification)
                print(f"Ahora sigues a {otro_usuario.username}.")
            else:
                # Solicitar seguimiento
                self.enviar_solicitud_seguimiento(otro_usuario)
                print(f"Solicitud de seguimiento enviada a {otro_usuario.username}. Esperando aprobación.")
        else:
            print("Solo los estudiantes pueden seguir a otros estudiantes.")

    def gestionar_solicitudes_seguimiento(self, usuarios):
        if self.solicitudes_pendientes:
            print("Solicitudes de seguimiento pendientes:")
            for i, solicitud in enumerate(self.solicitudes_pendientes):
                print(f"{i + 1}. {solicitud.username}")

            opcion = input("¿Deseas aceptar alguna solicitud? (Ingrese el número o '0' para cancelar): ")
            if opcion.isdigit():
                opcion = int(opcion)
                if 0 < opcion <= len(self.solicitudes_pendientes):
                    estudiante_solicitante = self.solicitudes_pendientes[opcion - 1]
                    accion = input(f"¿Deseas aceptar (A) o rechazar (R) la solicitud de {estudiante_solicitante.username}? (A/R): ")
                    if accion.lower() == "a":
                        self.seguir_usuario(estudiante_solicitante)
                        self.solicitudes_pendientes.remove(estudiante_solicitante)
                        print(f"Aceptaste la solicitud de seguimiento de {estudiante_solicitante.username}.")
                    elif accion.lower() == "r":
                        self.solicitudes_pendientes.remove(estudiante_solicitante)
                        print(f"Rechazaste la solicitud de seguimiento de {estudiante_solicitante.username}.")
                    else:
                        print("Opción no válida.")
                elif opcion == 0:
                    print("Cancelaste la gestión de solicitudes.")
                else:
                    print("Opción no válida.")
        else:
            print("No tienes solicitudes de seguimiento pendientes.")

    def dejar_de_seguir_usuario(self, otro_usuario):
        if otro_usuario.identification in self.following:
            self.following.remove(otro_usuario.identification)
            print(f"Has dejado de seguir a {otro_usuario.username}.")
        else:
            print(f"No estabas siguiendo a {otro_usuario.username}.")

    def comentar_publicacion(self, publicacion, texto):
        nuevo_comentario = Comentario(self, publicacion, texto)
        publicacion.agregar_comentario(nuevo_comentario)
        print("Comentario agregado exitosamente.")

    def dar_like(self, publicacion):
        if self.identification not in publicacion.likes:
            # Si el usuario no había dado like, dar like
            publicacion.dar_like(self.identification)
            print("Le diste like a la publicación.")
        else:
            # Si ya había dado like, quitarlo
            publicacion.quitar_like(self.identification)
            print("Le diste dislike a la publicación.")

    def eliminar_comentario(self, publicacion, comentario):
        if comentario in publicacion.comentarios:
            publicacion.comentarios.remove(comentario)
            print("Comentario eliminado exitosamente.")
        else:
            print("Comentario no encontrado o no tienes permisos para eliminarlo.")
        
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
        self.solicitudes_seguimiento = []

    def enviar_solicitud_seguimiento(self, otro_usuario):
        otro_usuario.solicitudes_pendientes.append(self)

