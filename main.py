import funciones_catalogo

def main():

    print()
    while True:
        print("Catálogo de Obras del Museo Metropolitano de Arte: \n \n1- Ver lista de obras por Departamento \n2- Ver lista de obras por Nacionalidad del autor \n3- Ver lista de obras por nombre del autor \n4- Salir del sistema")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            funciones_catalogo.ver_obras_por_departamento()
        elif opcion == "2":
            pass
        elif opcion == "3":
            pass
        elif opcion == "4":
            print()
            print("Saliendo del sistema...")    
            print()
            break
        else:
            print()
            print("Opción invalida, por favor, intente de nuevo.")
            print()

main()
