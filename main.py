import os
# main.py
from login import login, get_usuario_actual, tiene_permisos_root
import procesos 
import planificador
import archivos
import logs

def mostrar_menu():
    print("\n=== Menú principal ===")
    print("1. Crear proceso")
    print("2. Ejecutar planificación CPU")
    print("3. Administrar archivos")
    print("4. Mostrar logs")
    print("5. Gestionar usuarios")
    print("6. Salir")
    return input("Selecciona una opción: ")

def main():
    if not login():
        return

    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            procesos.crear_proceso()
        elif opcion == "2":
            planificador.planificar()
        elif opcion == "3":
            archivos.administrar_archivos()
        elif opcion == "4":
            logs.mostrar_logs()
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()