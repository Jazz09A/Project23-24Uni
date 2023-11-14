import matplotlib.pyplot as plt
from collections import Counter

class Estadisticas:
    @staticmethod
    def usuarios_con_mas_publicaciones(usuarios, top_n=5):
        usuarios_sorted = sorted(usuarios, key=lambda x: len(x.publicaciones), reverse=True)
        top_usuarios = usuarios_sorted[:top_n]
        return top_usuarios

    @staticmethod
    def carreras_con_mas_publicaciones(usuarios, top_n=5):
        carreras_publicaciones = Counter([usuario.departament for usuario in usuarios for _ in usuario.publicaciones])
        carreras_sorted = dict(sorted(carreras_publicaciones.items(), key=lambda x: x[1], reverse=True)[:top_n])
        return carreras_sorted

    @staticmethod
    def post_con_mas_interacciones(publicaciones, top_n=1):
        post_sorted = sorted(publicaciones, key=lambda x: len(x.likes) + len(x.comentarios), reverse=True)
        top_post = post_sorted[:top_n]
        return top_post

    @staticmethod
    def usuarios_con_mas_interacciones(usuarios, top_n=5):
        usuarios_sorted = sorted(usuarios, key=lambda x: x.obtener_interacciones(), reverse=True)
        top_usuarios = usuarios_sorted[:top_n]
        return top_usuarios

    @staticmethod
    def usuarios_con_mas_post_tumbados(usuarios, top_n=5):
        usuarios_sorted = sorted(usuarios, key=lambda x: x.post_tumbados, reverse=True)
        top_usuarios = usuarios_sorted[:top_n]
        return top_usuarios

    @staticmethod
    def carreras_con_mas_comentarios_inadecuados(usuarios, top_n=5):
        carreras_comentarios = Counter([usuario.departament for usuario in usuarios for comentario in usuario.comentarios_inadecuados])
        carreras_sorted = dict(sorted(carreras_comentarios.items(), key=lambda x: x[1], reverse=True)[:top_n])
        return carreras_sorted

    @staticmethod
    def usuarios_eliminados_por_infracciones(usuarios_eliminados, top_n=5):
        usuarios_eliminados_sorted = sorted(usuarios_eliminados, key=lambda x: x.infracciones, reverse=True)
        top_usuarios_eliminados = usuarios_eliminados_sorted[:top_n]
        return top_usuarios_eliminados

    @staticmethod
    def generar_grafico_barras(etiquetas, valores, titulo, etiqueta_x, etiqueta_y):
        plt.bar(etiquetas, valores)
        plt.xlabel(etiqueta_x)
        plt.ylabel(etiqueta_y)
        plt.title(titulo)
        plt.show()