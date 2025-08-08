import Catalogo
from Obras import Obra
import csv
import requests

#    Muestra los departamentos  y pide al usuario escoger uno:
def ver_obras_por_departamento():
    departamentos = Catalogo.obtener_departamentos()

    if departamentos and "departments" in departamentos:
        print()
        print("--- Departamentos del Museo ---")
        for departamento in departamentos["departments"]:
            print(f"ID: {departamento['departmentId']} - Nombre: {departamento['displayName']}")

        try:
            print()
            depto_id = int(input("Ingrese el ID del departamento para ver las obras: "))
            print()
            obras_data = Catalogo.obtener_obras_por_departamento(depto_id)

            if obras_data and "objectIDs" in obras_data and obras_data["objectIDs"]:
                print(f"Se encontraron {len(obras_data['objectIDs'])} obras")
                mostrar_listado_obras(obras_data["objectIDs"])
            else:
                print("No se encontró ninguna obra para este departamento.")

        except (KeyError):
            print("Error, asegúrese de ingresar un ID numérico válido")
    else:
        print("No se pudieron obtener los departamentos.")


#Muestra una lista de nacionalidades en el archivo dado en las instrucciones del proyecto.
#El usuario puede seleccionar una para buscar obras por nacionalidad del autor.
def ver_obras_por_nacionalidad():
    nacionalidades = []
    try:
        with open("CH_Nationality_List_20171130_v1.csv", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                if fila and fila[0].strip() != "":
                    nacionalidades.append(fila[0].strip())
    except:
        print("No se pudo leer el archivo de nacionalidades.")
        return

    for i, nacionalidad in enumerate(nacionalidades):
        print(f"{i + 1}. {nacionalidad}")

    seleccion = input("Ingrese el número de la nacionalidad: ")
    if not seleccion.isnumeric():
        print("Valor inválido.")
        return

    indice = int(seleccion) - 1
    if indice < 0 or indice >= len(nacionalidades):
        print("Número fuera de rango.")
        return

    valor = nacionalidades[indice]
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={valor}"
    importar_y_mostrar_ids(url)

# Solicita al usuario un nombre de autor y muestra obras relacionadas.
def ver_obras_por_autor():
    nombre = input("Ingrese el nombre del autor: ").strip()
    if nombre == "":
        print("Nombre vacío.")
        return

    url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={nombre}"
    importar_y_mostrar_ids(url)


# Hace una solicitud a la API  y trae los IDs de las obras.
#   Luego llama a mostrar_listado_obras() para presentar los resultados en bloques.

def importar_y_mostrar_ids(url):
    respuesta = requests.get(url)
    try:
        datos = respuesta.json()
    except:
        print("No se pudo procesar la respuesta.")
        return

    if "objectIDs" not in datos or not datos["objectIDs"]:
        print("No se encontraron obras.")
        return

    mostrar_listado_obras(datos["objectIDs"])

# Muestra obras en bloques de 20. Permite al usuario ver detalles de obras mostradas en cada bloque.
def mostrar_listado_obras(object_ids):
    obras_encontradas = []
    total = len(object_ids)
    inicio = 0

    while inicio < total:
        obras_encontradas.clear()
        print(f"\nMostrando obras {inicio + 1} a {min(inicio + 20, total)} de {total}\n")

        for obj_id in object_ids[inicio:inicio + 20]:
            obra_data = Catalogo.obtener_datos_de_la_obra(obj_id)

            if not obra_data:
                print(f"No se pudo cargar la obra con ID {obj_id}")
                continue

            # Validaciones individuales para cada campo
            if "objectID" in obra_data and obra_data["objectID"] != "":
                id_obra = obra_data["objectID"]
            else:
                id_obra = "N/A"

            if "title" in obra_data and obra_data["title"] != "":
                titulo = obra_data["title"]
            else:
                titulo = "Sin título"

            if "artistDisplayName" in obra_data and obra_data["artistDisplayName"] != "":
                autor = obra_data["artistDisplayName"]
            else:
                autor = "Desconocido"

            if "artistNationality" in obra_data and obra_data["artistNationality"] != "":
                nacionalidad = obra_data["artistNationality"]
            else:
                nacionalidad = "N/A"

            if "artistBeginDate" in obra_data and obra_data["artistBeginDate"] != "":
                nacimiento = obra_data["artistBeginDate"]
            else:
                nacimiento = "N/A"

            if "artistEndDate" in obra_data and obra_data["artistEndDate"] != "":
                fallecimiento = obra_data["artistEndDate"]
            else:
                fallecimiento = "N/A"

            if "classification" in obra_data and obra_data["classification"] != "":
                tipo = obra_data["classification"]
            else:
                tipo = "N/A"

            if "objectDate" in obra_data and obra_data["objectDate"] != "":
                fecha = obra_data["objectDate"]
            else:
                fecha = "N/A"

            if "primaryImage" in obra_data and obra_data["primaryImage"] != "":
                imagen = obra_data["primaryImage"]
            else:
                imagen = "N/A"

            # Crear objeto obra con toda la información validada
            obra = Obra(
                id=id_obra,
                titulo=titulo,
                autor=autor,
                nacionalidad=nacionalidad,
                nacimiento=nacimiento,
                fallecimiento=fallecimiento,
                tipo=tipo,
                fecha_creacion=fecha,
                imagen_url=imagen
            )

            obras_encontradas.append(obra)
            print(f"ID: {obra.id}, Título: {obra.titulo}, Autor: {obra.autor}")

        if obras_encontradas:
            mostrar_detalles_opcion(obras_encontradas)
        else:
            print("No se encontraron obras para mostrar.")

        inicio += 20
        if inicio < total:
            continuar = input("¿Desea ver más obras? (si/no): ")
            if continuar.lower() != "si":
                break

#Permite al usuario seleccionar una o más obras del grupo para ver sus detalles. El usuario puede ver varias antes de volver al menú.
def mostrar_detalles_opcion(obras):

    while True:
        print()
        opcion_detalles = input("Ingrese el ID de la obra para ver detalles (o escriba 'volver' para regresar): ")

        if opcion_detalles.lower() == "volver":
            print()
            break

        obra_seleccionada = None
        for obra in obras:
            if str(obra.id) == opcion_detalles:
                obra_seleccionada = obra
                break

        if obra_seleccionada:
            obra_seleccionada.mostrar_detalles()
        else:
            print("Error, por favor, ingrese un ID válido.")

        print()
        seguir = input("¿Desea ver otra obra de este grupo? (si/no): ")
        if seguir.lower() != "si":
            break

