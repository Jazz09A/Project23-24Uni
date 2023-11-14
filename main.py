import uuid
import requests
from usuarios import Usuario,Estudiante,Profesor
from publicaciones import Publicacion
from estadisticas import Estadisticas
#funcion para imprimir las estadisticas
def imprimir_estadistica(titulo, datos):
    print(titulo)
    for dato in datos:
        print(f"{dato.username}: {dato.informacion_estadistica()}")
#Funcion para cargar datos
def carga_datos_usuarios() ->list:
    #Cargando datos de la API con requests
    api_usuarios = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/08d4d2ce028692d71e9f8c32ea8c29ae24efe5b1/users.json"
    response_usuarios = requests.get(api_usuarios)
    datos_usuarios = response_usuarios.json()

    #lista para almacenar datos de los usuarios
    usuarios = []
    for data in datos_usuarios:
        if data['type'] == 'professor':
            usuario = Profesor(data['id'], data['firstName'], data['lastName'], data['email'], data['username'], data['department'], data['following'])
        elif data['type'] == 'student':
            usuario = Estudiante(data['id'], data['firstName'], data['lastName'], data['email'], data['username'], data['major'], data['following'])
        usuarios.append(usuario)
    return usuarios
def cargar_datos_publicaciones():
    api_Post = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/main/posts.json"
    response_Post = requests.get(api_Post)
    datos_post = response_Post.json()
    publicaciones = []

    for datos in datos_post:
        publicacion = Publicacion(datos['publisher'],datos['type'],datos['caption'],datos['tags'],datos['date'],datos['multimedia'])
        publicaciones.append(publicacion)
    return publicaciones

#Menu principal de la app
def menu():
    usuarios = carga_datos_usuarios()
    publicaciones = cargar_datos_publicaciones()
    for publicacion in publicaciones:
        for usuario in usuarios:
            if publicacion.usuario == usuario.identification:
                usuario.publicaciones.append(publicacion)
    while True:
        opcion= input("Bienvenido\n1. Gestion de perfiles\n2.Gestion multimedia\n3. Gestion de interacciones\n4. indicadores de gestion\n5. Salir.")
        if opcion == "1":
            opcionGP = input("1. Registrar nuevo usuario\n2. Buscar Perfiles\n3.Cambiar informacion de la cuenta\n4.Borrar datos de la cuenta\n5.Acceder a la cuenta de otro usuario")
            if opcionGP =="1":
                identification = str(uuid.uuid4())
                firstName = input("Ingrese el nombre: ")
                lastName = input("Ingrese el apellido: ")
                email = input("Ingrese el email: ")
                username = input("Ingrese un username: ")
                types = ("Ingrese el tipo de usuario (profesor o estudiante)")
                if types.lower() == "estudiante":
                    major = input("Ingresa la carrera que estudias: ")
                    nuevo_usuario = usuario.registrar_estudiante(identification,firstName,lastName,email,username,major)
                    usuarios.append(nuevo_usuario)
                elif types.lower() == "profesor":
                    departament = input("Ingrese el departamento: ")
                    nuevo_profesor = usuario.registrar_profesor(identification,firstName,lastName,email,username,departament) 
                    usuarios.append(nuevo_profesor)
                else:
                    print("Ingrese un tipo correcto(Estudiante o Profesor)")
            elif opcionGP == "2":
                pass
            elif opcionGP == "3":
                username = "Hernan2"
                for usuario in usuarios:
                    if username == usuario.username:
                        print(f"Perfil encontrado: {usuario.firstname} {usuario.lastname}")
                        firstname = input("Nuevo nombre: ")
                        lastname = input("Nuevo apellido: ")
                        email = input("Nuevo correo electrónico: ")
                        new_username = input("Nuevo username: ")

                        if usuario.type == "profesor":
                            department = input("Nuevo departamento: ")
                            usuario.actualizar_informacion(firstname, lastname, email, new_username, department, "")
                        elif usuario.type == "estudiante":
                            major = input("Nueva carrera: ")
                            usuario.actualizar_informacion(firstname, lastname, email, new_username, "", major)

                        print("\nInformación actualizada:")
                        print(f"Nombre: {usuario.firstname} {usuario.lastname}")
                        print(f"Correo Electrónico: {usuario.email}")
                        print(f"Username: {usuario.username}")
                        if usuario.type == "profesor":
                            print(f"Departamento: {usuario.departament}")
                        elif usuario.type == "estudiante":
                            print(f"Carrera: {usuario.major}")
                print("Perfil no encontrado.")
            elif opcionGP == "4":
                username = input("Ingrese el nombre del usuario: ")
                Usuario.eliminar_cuenta(username,usuarios)
            elif opcionGP =="5":
                pass
        elif opcion == "2":
            print("Gestión de multimedia")
            opcionGM = input("")
            if opcionGM == "1":
                usuario_actual = Usuario.obtener_usuario_actual(usuarios)
                if usuario_actual:
                    tipo_multimedia = input("Tipo de multimedia (foto o video): ")
                    descripcion = input("Descripción: ")
                    hashtags = input("Hashtags (separados por comas): ").split(',')
                    nueva_publicacion = usuario_actual.subir_publicacion(tipo_multimedia, descripcion, hashtags)
                    publicaciones.append(nueva_publicacion)
                    print("Publicación subida exitosamente.")
                else:
                    print("Debes iniciar sesión primero.")
            elif opcionGM == "2":
                # Acceder a la cuenta de otro usuario
                username_buscado = input("Ingresa el nombre de usuario que buscas: ")
                usuario_a_seguir = Usuario.buscar_por_username(username_buscado,usuarios)
                if usuario_a_seguir:
                    username_actual = input("Ingresa tu nombre de usuario: ")
                    usuario_actual = Usuario.buscar_por_username(username_actual, usuarios)
                    if usuario_actual:
                        usuario_actual.ver_publicaciones(usuario_a_seguir)
                    else:
                        print(f"El usuario actual con nombre de usuario '{username_actual}' no fue encontrado.")
                else:
                    print(f"No se encontró al usuario con nombre de usuario '{username_buscado}'.")
            elif opcionGM == "3":
                opcionBP = input("1. Buscar publicaciones por usuario (username)\n2. Buscar publicaciones por hashtags (#)\n")
    
                if opcionBP == "1":
                    username_busqueda = input("Ingresa el username del usuario cuyas publicaciones deseas buscar: ")
                    publicaciones_usuario = Usuario.buscar_publicaciones_por_usuario(usuarios, username_busqueda)
                    if publicaciones_usuario:
                        print(f"Publicaciones del usuario '{username_busqueda}':")
                        for publicacion in publicaciones_usuario:
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
                        print(f"No se encontraron publicaciones del usuario '{username_busqueda}'.")
                
                elif opcionBP == "2":
                    hashtag_busqueda = input("Ingresa el hashtag que deseas buscar: ")
                    publicaciones_hashtags = Usuario.buscar_publicaciones_por_hashtags(publicaciones, hashtag_busqueda)
                    if publicaciones_hashtags:
                        print(f"\nPublicaciones con el hashtag '{hashtag_busqueda}':")
                        for publicacion in publicaciones_hashtags:
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
                        print(f"No se encontraron publicaciones con el hashtag '{hashtag_busqueda}'.")
        elif opcion == "3":
            opcionGI = input("1. Seguir a un usuario\n2. Dejar de seguir a un usuario\n3. Comentar una publicación\n4. Dar like a una publicación\n5. Eliminar comentario de una publicación\n6. Acceder al perfil de otro usuario desde likes o comentarios\n7. Gestionar solicitudes de seguimiento\n")

            if opcionGI == "1":
                username_seguidor = input("Ingresa tu nombre de usuario: ")
                usuario_seguidor = Usuario.buscar_por_username(username_seguidor, usuarios)
                
                username_a_seguir = input("Ingresa el nombre de usuario a seguir: ")
                usuario_a_seguir = Usuario.buscar_por_username(username_a_seguir, usuarios)

                if usuario_seguidor and usuario_a_seguir:
                    usuario_seguidor.seguir_usuario(usuario_a_seguir)
                else:
                    print("Usuario no encontrado.")

            elif opcionGI == "2":
                username_seguidor = input("Ingresa tu nombre de usuario: ")
                usuario_seguidor = Usuario.buscar_por_username(username_seguidor, usuarios)
                
                username_a_dejar_de_seguir = input("Ingresa el nombre de usuario a dejar de seguir: ")
                usuario_a_dejar_de_seguir = Usuario.buscar_por_username(username_a_dejar_de_seguir, usuarios)

                if usuario_seguidor and usuario_a_dejar_de_seguir:
                    usuario_seguidor.dejar_de_seguir_usuario(usuario_a_dejar_de_seguir)
                else:
                    print("Usuario no encontrado.")

            elif opcionGI == "3":
                username_comentador = input("Ingresa tu nombre de usuario: ")
                usuario_comentador = Usuario.buscar_por_username(username_comentador, usuarios)

                if usuario_comentador:
                    # Mostrar una lista de usuarios a los que sigue y puede comentar
                    usuarios_a_comentar = [usuario for usuario in usuarios if usuario.identification != usuario_comentador.identification and usuario.identification in usuario_comentador.following]
                    if not usuarios_a_comentar:
                        print("No sigues a nadie a quien puedas comentar.")
                    else:
                        print("Usuarios a los que sigues y puedes comentar:")
                        for i, otro_usuario in enumerate(usuarios_a_comentar):
                            print(f"{i + 1}. {otro_usuario.username}")

                        opcion_usuario = input("Ingresa el número del usuario al que quieres comentar: ")
                        if opcion_usuario.isdigit():
                            opcion_usuario = int(opcion_usuario) - 1
                            if 0 <= opcion_usuario < len(usuarios_a_comentar):
                                usuario_a_comentar = usuarios_a_comentar[opcion_usuario]

                                # Mostrar las publicaciones del usuario a comentar
                                print(f"Publicaciones de {usuario_a_comentar.username}:")
                                for i, publicacion in enumerate(usuario_a_comentar.publicaciones):
                                    print(f"{i + 1}: {publicacion.descripcion}")

                                opcion_publicacion = input("Ingresa el número de la publicación a comentar: ")
                                if opcion_publicacion.isdigit():
                                    opcion_publicacion = int(opcion_publicacion) - 1
                                    if 0 <= opcion_publicacion < len(usuario_a_comentar.publicaciones):
                                        publicacion_a_comentar = usuario_a_comentar.publicaciones[opcion_publicacion]
                                        texto_comentario = input("Ingresa el comentario: ")
                                        usuario_comentador.comentar_publicacion(publicacion_a_comentar, texto_comentario)
                                    else:
                                        print("Opción de publicación no válida.")
                                else:
                                    print("Opción de publicación no válida.")
                            else:
                                print("Opción de usuario no válida.")
                        else:
                            print("Opción de usuario no válida.")
                else:
                    print("Usuario comentador no encontrado.")

            elif opcionGI == "4":
                username_liker = input("Ingresa tu nombre de usuario: ")
                usuario_liker = Usuario.buscar_por_username(username_liker, usuarios)

                if usuario_liker:
                    # Mostrar una lista de usuarios a los que sigue y puede dar "like"
                    usuarios_a_dar_like = [usuario for usuario in usuarios if usuario.identification != usuario_liker.identification and usuario.identification in usuario_liker.following]
                    if not usuarios_a_dar_like:
                        print("No sigues a nadie a cuyas publicaciones puedas dar 'like'.")
                    else:
                        print("Usuarios a los que sigues y cuyas publicaciones puedes dar 'like':")
                        for i, otro_usuario in enumerate(usuarios_a_dar_like):
                            print(f"{i + 1}. {otro_usuario.username}")

                        opcion_usuario = input("Ingresa el número del usuario cuya publicación quieres dar 'like': ")
                        if opcion_usuario.isdigit():
                            opcion_usuario = int(opcion_usuario) - 1
                            if 0 <= opcion_usuario < len(usuarios_a_dar_like):
                                usuario_a_dar_like = usuarios_a_dar_like[opcion_usuario]

                                # Mostrar las publicaciones del usuario a dar "like"
                                print(f"Publicaciones de {usuario_a_dar_like.username}:")
                                for i, publicacion in enumerate(usuario_a_dar_like.publicaciones):
                                    print(f"{i + 1}: {publicacion.descripcion}")

                                opcion_publicacion = input("Ingresa el número de la publicación a la que quieres dar 'like': ")
                                if opcion_publicacion.isdigit():
                                    opcion_publicacion = int(opcion_publicacion) - 1
                                    if 0 <= opcion_publicacion < len(usuario_a_dar_like.publicaciones):
                                        publicacion_a_dar_like = usuario_a_dar_like.publicaciones[opcion_publicacion]
                                        usuario_liker.dar_like(publicacion_a_dar_like)
                                        print("Has dado 'like' a la publicación exitosamente.")
                                    else:
                                        print("Opción de publicación no válida.")
                                else:
                                    print("Opción de publicación no válida.")
                            else:
                                print("Opción de usuario no válida.")
                        else:
                            print("Opción de usuario no válida.")
                else:
                    print("Usuario que da 'like' no encontrado.")


            elif opcionGI == "5":
                username_dueno_post = input("Ingresa tu nombre de usuario: ")
                usuario_dueno_post = Usuario.buscar_por_username(username_dueno_post, usuarios)

                if usuario_dueno_post:
                    print(f"Publicaciones de {usuario_dueno_post.username}:")
                    for i, publicacion in enumerate(usuario_dueno_post.publicaciones):
                        print(f"{i + 1}: {publicacion.descripcion}")

                    opcion_publicacion = input("Ingresa el número de la publicación en la que quieres eliminar un comentario: ")
                    if opcion_publicacion.isdigit():
                        opcion_publicacion = int(opcion_publicacion) - 1
                        if 0 <= opcion_publicacion < len(usuario_dueno_post.publicaciones):
                            publicacion_a_eliminar_comentario = usuario_dueno_post.publicaciones[opcion_publicacion]

                            # Mostrar los comentarios en la publicación con comentarios a eliminar
                            if publicacion_a_eliminar_comentario.comentarios:
                                print("Comentarios en la publicación:")
                                for i, comentario in enumerate(publicacion_a_eliminar_comentario.comentarios):
                                    print(f"{i + 1}: {comentario}")

                                opcion_comentario = input("Ingresa el número del comentario que deseas eliminar (o '0' para cancelar): ")
                                if opcion_comentario.isdigit():
                                    opcion_comentario = int(opcion_comentario) - 1
                                    if 0 <= opcion_comentario < len(publicacion_a_eliminar_comentario.comentarios):
                                        comentario_a_eliminar = publicacion_a_eliminar_comentario.comentarios[opcion_comentario]
                                        print(f"Comentario seleccionado: {comentario_a_eliminar}")
                                        
                                        confirmacion = input("¿Seguro que deseas eliminar este comentario? (s/n): ")
                                        if confirmacion.lower() == "s":
                                            usuario_dueno_post.eliminar_comentario(publicacion_a_eliminar_comentario, comentario_a_eliminar)
                                            print("Comentario eliminado exitosamente.")
                                        else:
                                            print("Eliminación de comentario cancelada.")
                                    else:
                                        print("Opción de comentario no válida.")
                                elif opcion_comentario == "0":
                                    print("Cancelaste la eliminación de comentario.")
                                else:
                                    print("Opción de comentario no válida.")
                            else:
                                print("La publicación no tiene comentarios.")
                        else:
                            print("Opción de publicación no válida.")
                    else:
                        print("Opción de publicación no válida.")
                else:
                    print("Usuario dueño del post no encontrado.")


            elif opcionGI == "6":
            # Acceder al perfil de otro usuario desde comentarios
                publicacion_id = input("Ingrese el ID de la publicación: ")
                publicacion_a_ver = None
                for publicacion in publicaciones:
                    if publicacion.identification == publicacion_id:
                        publicacion_a_ver = publicacion
                        break

                if publicacion_a_ver:
                    # Ver comentarios y acceder a perfiles desde los comentarios
                    publicacion_a_ver.ver_comentarios(usuarios)
                else:
                    print("Publicación no encontrada.")
            elif opcionGI == "7":
             # Después de que un usuario inicie sesión con éxito, asigna el usuario actual
                usuario_actual = Usuario.obtener_usuario_actual(usuarios)
                usuario_actual.gestionar_solicitudes_seguimiento(usuarios)
        elif opcion == "4":
            pass
        elif opcion == "5":
            # Estadísticas
            print("Indicadores de gestión (Estadísticas)")
            opcion_estadisticas = input("1. Usuarios con más publicaciones\n2. Carreras con más publicaciones\n3. Post con más interacciones\n4. Usuarios con más interacciones\n5. Usuarios con más post tumbados\n6. Carreras con más comentarios inadecuados\n7. Usuarios eliminados por infracciones\n")
            
            if opcion_estadisticas == "1":
                top_usuarios_publicaciones = Estadisticas.usuarios_con_mas_publicaciones(usuarios)
                imprimir_estadistica("Usuarios con más publicaciones", top_usuarios_publicaciones)
                
            elif opcion_estadisticas == "2":
                top_carreras_publicaciones = Estadisticas.carreras_con_mas_publicaciones(usuarios)
                imprimir_estadistica("Carreras con más publicaciones", top_carreras_publicaciones)
                
            elif opcion_estadisticas == "3":
                top_post_interacciones = Estadisticas.post_con_mas_interacciones(publicaciones)
                imprimir_estadistica("Post con más interacciones", top_post_interacciones)
                
            elif opcion_estadisticas == "4":
                top_usuarios_interacciones = Estadisticas.usuarios_con_mas_interacciones(usuarios)
                imprimir_estadistica("Usuarios con más interacciones", top_usuarios_interacciones)
                
            elif opcion_estadisticas == "5":
                top_usuarios_tumbados = Estadisticas.usuarios_con_mas_post_tumbados(usuarios)
                imprimir_estadistica("Usuarios con más post tumbados", top_usuarios_tumbados)
                
            elif opcion_estadisticas == "6":
                top_carreras_comentarios_inadecuados = Estadisticas.carreras_con_mas_comentarios_inadecuados(usuarios)
                imprimir_estadistica("Carreras con más comentarios inadecuados", top_carreras_comentarios_inadecuados)
                
            elif opcion_estadisticas == "7":
                usuarios_eliminados = []  # Lista de usuarios eliminados
                top_usuarios_eliminados = Estadisticas.usuarios_eliminados_por_infracciones(usuarios_eliminados)
                imprimir_estadistica("Usuarios eliminados por infracciones", top_usuarios_eliminados)
        elif opcion == "6":
            break
if __name__ == "__main__":
    menu()

