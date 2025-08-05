class Obra:
    def __init__(self, id, titulo, autor, nacionalidad, nacimiento, fallecimiento, tipo, fecha_creacion, imagen_url):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.nacionalidad = nacionalidad
        self.nacimiento = nacimiento
        self.fallecimiento = fallecimiento
        self.tipo = tipo
        self.fecha_creacion = fecha_creacion
        self.imagen_url = imagen_url

    def mostrar_detalles(self):
        print("Detalles de la Obra seleccionada: ")
        print("ID:",self.id)
        print("Título: ",self.titulo)
        print("Nombre del Artista: ",self.autor)
        print("Nacionalidad: ",self.nacionalidad)
        print("Fecha de nacimiento: ",self.nacimiento)
        print("Fecha de muerte: ",self.fallecimiento)
        print("Tipo: ",self.tipo)
        print("Año de creación: ",self.fecha_creacion)
        print("Imagen de la obra: ",self.imagen_url)