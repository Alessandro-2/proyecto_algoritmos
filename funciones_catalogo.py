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

# Solicita al usuario un nombre de autor y muestra obras relacionadas.
def ver_obras_por_autor():
    nombre=input("Ingrese el nombre del autor: ").strip()
    if nombre == "":
        print("Nombre vacío.")
        return
    
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?artistOrCulture=true&q={nombre}"
    importar_y_mostrar_ids(url)
    
# Hace una solicitud a la API usando la URL dada y extrae los IDs de las obras.
# Luego llama a mostrar_listado_obras() para presentar los resultados en bloques. 
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
        seguir = input("¿Desea ver otra obra de este grupo? (s/n): ")
        if seguir.lower() != "s":
            break

