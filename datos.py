import json
from usuarios import Profesor,Estudiante
from publicaciones import Publicacion

def guardar_datos_local(usuarios, publicaciones):
    with open('usuarios.json', 'w') as file:
        usuarios_data = [
            {
                'id': usuario.id,
                'firstName': usuario.firstName,
                'lastName': usuario.lastName,
                'email': usuario.email,
                'username': usuario.username,
                'type': 'professor' if isinstance(usuario, Profesor) else 'student',
                'department': getattr(usuario, 'department', None),
                'major': getattr(usuario, 'major', None),
                'following': usuario.following
            }
            for usuario in usuarios
        ]
        json.dump(usuarios_data, file, indent=2)

    with open('publicaciones.json', 'w') as file:
        publicaciones_data = [
            {
                'publisher': publicacion.publisher,
                'type': publicacion.type,
                'caption': publicacion.caption,
                'tags': publicacion.tags,
                'date': publicacion.date,
                'multimedia': publicacion.multimedia
            }
            for publicacion in publicaciones
        ]
        json.dump(publicaciones_data, file, indent=2)

def cargar_datos_local():
    try:
        with open('usuarios.json', 'r') as file:
            usuarios_data = json.load(file)
            usuarios = [
                Profesor(**usuario) if usuario['type'] == 'professor' else Estudiante(**usuario)
                for usuario in usuarios_data
            ]
    except FileNotFoundError:
        usuarios = []

    try:
        with open('publicaciones.json', 'r') as file:
            publicaciones_data = json.load(file)
            publicaciones = [Publicacion(**publicacion) for publicacion in publicaciones_data]
    except FileNotFoundError:
        publicaciones = []

    return usuarios, publicaciones
