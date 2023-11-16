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
        self.es_admin = False

    def registrar_profesor(self, identification, firstname, lastname, email, username, department):
        nuevo_profesor = nuevo_profesor = Profesor(identification, firstname, lastname, email, username, department, [])
        return nuevo_profesor

    def registrar_estudiante(self, identification, firstname, lastname, email, username, major):
        nuevo_estudiante = Estudiante(identification, firstname, lastname, email, username, major, [])
        return nuevo_estudiante
    @classmethod
    def buscar_por_username(cls, username, datos):
        for usuario in datos:
            if username == usuario.username:
                return usuario
        return None  # Retorna None si el usuario no se encuentra
   
    def buscar_por_departamento_o_carrera(self, tipo, datos):
        perfiles_encontrados = []
        
        if tipo == "1":
            criterio = input("Ingrese el departamento: ")
            perfiles_encontrados = [usuario for usuario in datos if usuario.departament == criterio]
        elif tipo == "2":
            criterio = input("Ingrese la carrera: ")
            perfiles_encontrados = [usuario for usuario in datos if usuario.major == criterio]

        return perfiles_encontrados

    
    def actualizar_informacion(self, firstname, lastname, email, new_username, departament, major):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = new_username
        self.departament = departament
        self.major = major
    

    @staticmethod
    def eliminar_cuenta(username, usuarios):
        usuario_encontrado = next((usuario for usuario in usuarios if username == usuario.username), None)
        if usuario_encontrado:
            usuarios.remove(usuario_encontrado)
            print("Cuenta eliminada exitosamente.")
        else:
            print("Perfil no encontrado.")

    def mostrar_perfil(self, username, usuarios, publicaciones):
        usuario = self.buscar_por_username(username, usuarios)
        if usuario:
            publicaciones_encontradas = [publicacion for publicacion in publicaciones if publicacion.usuario == usuario.identification]
            if publicaciones_encontradas:
                return publicaciones_encontradas
            else:
                print("No hay publicaciones encontradas para este usuario.")
        else:
            print("Usuario no encontrado.")
            return []

        
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

    #Funcion de busqueda de publicaciones refactorizada, es una funcion para las 2
    @staticmethod
    def buscar_publicaciones_por_criterio(datos, criterio, valor):
        publicaciones_encontradas = []
        for dato in datos:
            if criterio(dato, valor):
                if isinstance(dato, Usuario):
                    publicaciones_encontradas.extend(dato.publicaciones)
                elif isinstance(dato, Publicacion):
                    publicaciones_encontradas.append(dato)
        return publicaciones_encontradas

    @staticmethod
    def por_usuario(usuario, username):
        return usuario.username == username

    @staticmethod
    def por_hashtags(publicacion, hashtag):
        return hashtag in publicacion.tags
        
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
        if not self.solicitudes_pendientes:
            print("No tienes solicitudes de seguimiento pendientes.")
            return

        print("Solicitudes de seguimiento pendientes:")
        for i, solicitud in enumerate(self.solicitudes_pendientes, 1):
            print(f"{i}. {solicitud.username}")

        try:
            opcion = int(input("¿Deseas aceptar alguna solicitud? (Ingrese el número o '0' para cancelar): "))
            if opcion == 0:
                print("Cancelaste la gestión de solicitudes.")
                return
            elif 0 < opcion <= len(self.solicitudes_pendientes):
                estudiante_solicitante = self.solicitudes_pendientes[opcion - 1]
                accion = input(f"¿Deseas aceptar (A) o rechazar (R) la solicitud de {estudiante_solicitante.username}? (A/R): ").lower()
                
                if accion == "a":
                    self.seguir_usuario(estudiante_solicitante)
                    self.solicitudes_pendientes.remove(estudiante_solicitante)
                    print(f"Aceptaste la solicitud de seguimiento de {estudiante_solicitante.username}.")
                elif accion == "r":
                    self.solicitudes_pendientes.remove(estudiante_solicitante)
                    print(f"Rechazaste la solicitud de seguimiento de {estudiante_solicitante.username}.")
                else:
                    print("Opción no válida. Selecciona 'A' para aceptar o 'R' para rechazar.")
            else:
                print("Opción no válida. Ingresa un número correspondiente a una solicitud.")
        except ValueError:
            print("Entrada no válida. Debes ingresar un número.")


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
    def hacer_admin(self):
        self.es_admin = True
    def enviar_solicitud_seguimiento(self, otro_usuario):
        otro_usuario.solicitudes_pendientes.append(self)    

    #Funcion refactorizada
    def eliminar_post_ofensivo(self, publicaciones):
        if not self.es_admin:
            print("No tienes permisos para realizar esta acción.")
            return

        if not publicaciones:
            print("No hay publicaciones para mostrar.")
            return

        print("Publicaciones:")
        for i, publicacion in enumerate(publicaciones, 1):
            print(f"{i}. Descripción: {publicacion.descripcion}")
            print(f"   Fecha: {publicacion.fecha}")
            print("=" * 40)

        while True:
            opcion_eliminar = input("Ingresa el número de la publicación que quieres eliminar (o '0' para cancelar): ")
            
            try:
                opcion_eliminar = int(opcion_eliminar)
                if 0 < opcion_eliminar <= len(publicaciones):
                    publicacion_a_eliminar = publicaciones[opcion_eliminar - 1]
                    self.publicaciones.remove(publicacion_a_eliminar)
                    print("Post eliminado exitosamente.")
                    break
                elif opcion_eliminar == 0:
                    print("Cancelaste la eliminación de post.")
                    break
                else:
                    print("Número de publicación no válido.")
            except ValueError:
                print("Entrada no válida. Debes ingresar un número entero.")

    #Funcion refactorizada
    def eliminar_comentario_ofensivo(self, publicaciones):
        if not self.es_admin:
            print("No tienes permisos para realizar esta acción.")
            return

        if not publicaciones:
            print("No hay publicaciones para mostrar.")
            return

        print("Publicaciones:")
        for i, publicacion in enumerate(publicaciones, 1):
            print(f"{i}. Descripción: {publicacion.descripcion}")
            print(f"   Fecha: {publicacion.fecha}")
            print("   Comentarios:")
            for j, comentario in enumerate(publicacion.comentarios, 1):
                print(f"      {j}. {comentario}")
            print("=" * 40)

        while True:
            opcion_publicacion = input("Ingresa el número de la publicación que contiene el comentario a eliminar (o '0' para cancelar): ")

            try:
                opcion_publicacion = int(opcion_publicacion)
                if 0 < opcion_publicacion <= len(publicaciones):
                    publicacion_a_eliminar_comentario = publicaciones[opcion_publicacion - 1]

                    while True:
                        opcion_comentario = input("Ingresa el número del comentario que quieres eliminar (o '0' para cancelar): ")

                        try:
                            opcion_comentario = int(opcion_comentario)
                            if 0 < opcion_comentario <= len(publicacion_a_eliminar_comentario.comentarios):
                                comentario_a_eliminar = publicacion_a_eliminar_comentario.comentarios[opcion_comentario - 1]
                                publicacion_a_eliminar_comentario.comentarios.remove(comentario_a_eliminar)
                                print("Comentario eliminado exitosamente.")
                                break
                            elif opcion_comentario == 0:
                                print("Cancelaste la eliminación de comentario.")
                                break
                            else:
                                print("Número de comentario no válido.")
                        except ValueError:
                            print("Entrada no válida. Debes ingresar un número entero.")
                    break
                elif opcion_publicacion == 0:
                    print("Cancelaste la eliminación de comentario.")
                    break
                else:
                    print("Número de publicación no válido.")
            except ValueError:
                print("Entrada no válida. Debes ingresar un número entero.")

#Funcion refactorizada
    def eliminar_usuario_infractor(self, usuarios):
        if not self.es_admin:
            print("No tienes permisos para realizar esta acción.")
            return

        if not usuarios:
            print("No hay usuarios para mostrar.")
            return

        print("Usuarios:")
        for i, usuario in enumerate(usuarios, 1):
            print(f"{i}. Username: {usuario.username}")

        while True:
            opcion_usuario = input("Ingresa el número del usuario a eliminar (o '0' para cancelar): ")

            try:
                opcion_usuario = int(opcion_usuario)
                if 0 < opcion_usuario <= len(usuarios):
                    usuario_a_eliminar = usuarios[opcion_usuario - 1]
                    usuarios.remove(usuario_a_eliminar)
                    print(f"Usuario {usuario_a_eliminar.username} eliminado por infracciones múltiples.")
                    break
                elif opcion_usuario == 0:
                    print("Cancelaste la eliminación de usuario.")
                    break
                else:
                    print("Número de usuario no válido.")
            except ValueError:
                print("Entrada no válida. Debes ingresar un número entero.")


    def obtener_interacciones(self):
        total_interacciones = 0
        for publicacion in self.publicaciones:
            if self.username in publicacion.likes:
                total_interacciones += 1  # Sumar un like por publicación
            total_interacciones += len([comentario for comentario in publicacion.comentarios if self.username in comentario])
            # Sumar los comentarios donde participa el usuario
        return total_interacciones

    def obtener_interacciones_usuario(self, usuarios):
        total_interacciones_usuario = 0
        for usuario in usuarios:
            if usuario.username in self.following:
                total_interacciones_usuario += usuario.obtener_interacciones()
        return total_interacciones_usuario


# Clase para representar un Profesor
class Profesor(Usuario):
    def __init__(self, identification, firstname, lastname, email, username, department, following):
        super().__init__(identification, firstname, lastname, email, username, "profesor", department, following)
        self.department = department

# Clase para representar un Estudiante
class Estudiante(Usuario):
    def __init__(self, identification, firstname, lastname, email, username, major, following):
        super().__init__(identification, firstname, lastname, email, username, "estudiante", major, following)
        self.major = major
        self.solicitudes_seguimiento = []

    

