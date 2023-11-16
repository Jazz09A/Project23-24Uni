import json
from usuarios import Profesor,Estudiante
from publicaciones import Publicacion
from datetime import datetime

# Función para serializar objetos datetime
def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()

# Guardar los datos con la función dump y el argumento default

def guardar_usuarios(usuarios):
    with open('usuarios.json', 'w') as file:
        usuarios_data = [
            {
                'id': usuario.identification,
                'firstName': usuario.firstname,
                'lastName': usuario.lastname,
                'email': usuario.email,
                'username': usuario.username,
                'type': 'professor' if isinstance(usuario, Profesor) else 'student',
                'department': getattr(usuario, 'department', None),
                'major': getattr(usuario, 'major', None),
                'following': usuario.following,
                'publicaciones': [
                    {
                        'publisher': publicacion.usuario,
                        'type': publicacion.tipo,
                        'caption': publicacion.descripcion,
                        'tags': publicacion.tags,
                        'date': publicacion.fecha,
                        'multimedia': publicacion.multimedia
                    }
                    for publicacion in usuario.publicaciones
                ]
            }
            for usuario in usuarios
        ]
        json.dump(usuarios_data, file, indent=4)

def guardar_publicaciones(publicaciones):
    with open('publicaciones.json', 'w') as file:
        publicaciones_data = [
            {
                'publisher': publicacion.usuario,
                'type': publicacion.tipo,
                'caption': publicacion.descripcion,
                'tags': publicacion.tags,
                'date': publicacion.fecha,
                'multimedia': publicacion.multimedia
            }
            for publicacion in publicaciones
        ]
        json.dump(publicaciones_data, file, indent=2,default=serialize_datetime)


def cargar_datos_usuarios():
    try:
        with open('usuarios.json', 'r') as file:
            usuarios_data = json.load(file)
            usuarios = []
            for usuario in usuarios_data:
                if usuario['type'] == 'professor':
                    nuevo_usuario = Profesor(
                        usuario['id'],
                        usuario['firstName'],
                        usuario['lastName'],
                        usuario['email'],
                        usuario['username'],
                        usuario['department'],
                        usuario['following']
                    )
                elif usuario['type'] == 'student':
                    nuevo_usuario = Estudiante(
                        usuario['id'],
                        usuario['firstName'],
                        usuario['lastName'],
                        usuario['email'],
                        usuario['username'],
                        usuario['major'],
                        usuario['following']
                    )
                usuarios.append(nuevo_usuario)
    except FileNotFoundError:
        usuarios = []
    return usuarios


def cargar_datos_publicaciones():
    try:
        with open('publicaciones.json', 'r') as file:
            publicaciones_data = json.load(file)
            publicaciones = [Publicacion(**publicacion) for publicacion in publicaciones_data]
    except FileNotFoundError:
        publicaciones = []
    return publicaciones

