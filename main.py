import funciones_catalogo

def main():
    """
    Muestra el menú principal del sistema MetroArt y gestiona la interacción con el usuario.
    """
    print()
    while True:
        print("Catálogo de Obras del Museo Metropolitano de Arte:\n")
        print("1 - Ver lista de obras por Departamento")
        print("2 - Ver lista de obras por Nacionalidad del autor")
        print("3 - Ver lista de obras por nombre del autor")
        print("4 - Salir del sistema")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            funciones_catalogo.ver_obras_por_departamento()
        elif opcion == "2":
            funciones_catalogo.ver_obras_por_nacionalidad()
        elif opcion == "3":
            passs
        elif opcion == "4":
            print()
            print("Saliendo del sistema...")
            print()
            break
        else:
            print()
            print("Opción inválida, por favor, intente de nuevo.")
            print()

main()
