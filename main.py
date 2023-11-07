import uuid
import requests
from usuarios import Usuario,Estudiante,Profesor
from publicaciones import Publicacion
#Intancias de las clases

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
            pass
        elif opcion == "4":
            pass
        elif opcion == "5":
            break
if __name__ == "__main__":
    menu()