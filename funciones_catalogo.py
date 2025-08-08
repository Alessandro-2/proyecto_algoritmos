import Catalogo
from Obras import Obra

def ver_obras_por_departamento():
    
    departamentos = Catalogo.obtener_departamentos()
    
    if departamentos and "departments" in departamentos:
        print()
        print("--- Departamentos del Museo ---")
        for departamento in departamentos["departments"]:
            print(f"ID: {departamento["departmentId"]} - Nombre: {departamento["displayName"]}")
    
        try:
            print()
            depto_id = int(input("Ingrese el ID del departamento para ver las obras: "))
            print()
            obras_data = Catalogo.obtener_obras_por_departamento(depto_id)
            
            if obras_data and "objectIDs" in obras_data and obras_data["objectIDs"]:
                print(f"Se encontraron {len(obras_data["objectIDs"])} obras")
                mostrar_listado_obras(obras_data["objectIDs"])
            else:
                print("No se encontro ninguna obra para este departamento")

        except (ValueError, KeyError):
            print("Error, asegúrese de ingresar un ID numérico válido")
        else:
            print("No se pudieron obtener los departamentos ")

def mostrar_listado_obras(object_ids):
    
    obras_encontradas = []
    
    for i, obj_id in enumerate(object_ids[:20]):
        obra_data = Catalogo.obtener_datos_de_la_obra(obj_id)
        
        if obra_data:
            obra = Obra(
                id=obra_data.get("objectID", "N/A"),
                titulo=obra_data.get("title", "Sin título"),
                autor=obra_data.get("artistDisplayName", "Desconocido"),
                nacionalidad=obra_data.get("artistNationality", "N/A"),
                nacimiento=obra_data.get("artistBeginDate", "N/A"),
                fallecimiento=obra_data.get("artistEndDate", "N/A"),
                tipo=obra_data.get("classification", "N/A"),
                fecha_creacion=obra_data.get("objectDate", "N/A"),
                imagen_url=obra_data.get("primaryImage", "N/A")
            )
            obras_encontradas.append(obra)
            print(f"ID: {obra.id}, Título: {obra.titulo}, Autor: {obra.autor}")

    if obras_encontradas:
        mostrar_detalles_opcion(obras_encontradas)
    else:
        print("No se encontraron obras para mostrar ")

def mostrar_detalles_opcion(obras):
    
    while True:
        print()
        opcion_detalles = input("Ingrese el ID de la obra para ver detalles: \nRegresar al menú principal: \nIngrese el numero del id o escriba 'volver' para regresar al menu: ")
        
        if opcion_detalles == "volver":
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
            print("Error, por favor, ingrese un ID de obra válido o '2' para regresar")

#Muestra una lista de nacionalidades
#El usuario puede seleccionar una para buscar obras por nacionalidad del autor.
def ver_obras_por_nacionalidad():

    nacionalidades=[]

    try:
        with open("CH_Nationality_List_20171130_v1.csv", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                if fila and fila[0].strip() != "":
                    nacionalidades.append(fila[0].strip())
    except:
        print("No se pudo leer el archivo de nacionalidades de los autores.")
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
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?artistOrCulture=true&q={valor}"
    importar_y_mostrar_ids(url)

#Hace una solicitud a la API usando la URL dada y extrae los IDs de las obras.
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

            # Validacion para cada campo
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

            # Crear objeto obra con la info validada
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
            continuar = input("¿Desea ver más obras? (s/n): ")
            if continuar.lower() != "s":
                break

