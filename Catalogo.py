import requests
import json 


def obtener_departamentos ():
    departamento = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/departments")

    datos = departamento.json()

    #print(json.dumps(datos, indent = 4))

    return datos 

def obtener_obras_por_departamento(num):
    obras = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects?departmentIds={num}")

    datos = obras.json()

    return datos 

def obtener_datos_de_la_obra(num):
    datosdeobra = requests.get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{num}")

    datos = datosdeobra.json()

    return datos







