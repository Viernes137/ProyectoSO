import os
from login import get_usuario_actual, tiene_permisos_root
from logs import escribir_log

def administrar_archivos():
    while True:
        print("\n--- Gestión de Archivos ---")
        print("1. Crear archivo")
        print("2. Leer archivo")
        print("3. Escribir archivo")
        print("4. Crear directorio")
        print("5. Volver al menú principal")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            crear_archivo()
        elif opcion == "2":
            leer_archivo()
        elif opcion == "3":
            escribir_archivo()
        elif opcion == "4":
            crear_directorio()
        elif opcion == "5":
            break
        else:
            print("Opción no válida.")

def crear_archivo():
    ruta = input("Ruta del archivo (ej. carpeta/archivo.txt): ")
    contenido = input("Contenido inicial: ")
    propietario = get_usuario_actual()

    # Asegura que el directorio exista
    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    # Crea el archivo
    with open(ruta, 'w') as f:
        f.write(contenido)

    escribir_log(f"Archivo '{ruta}' creado por {propietario}.")
    print(f"Archivo '{ruta}' creado exitosamente.")

def leer_archivo():
    ruta = input("Ruta del archivo a leer: ")
    usuario = get_usuario_actual()

    if os.path.exists(ruta):
        with open(ruta, 'r') as f:
            contenido = f.read()
            print(f"\nContenido de '{ruta}':\n{contenido}")
            escribir_log(f"{usuario} leyó el archivo '{ruta}'.")
    else:
        print("Archivo no encontrado.")
        escribir_log(f"{usuario} intentó leer un archivo inexistente: '{ruta}'.")

def escribir_archivo():
    ruta = input("Ruta del archivo a escribir: ")
    usuario = get_usuario_actual()

    if os.path.exists(ruta):
        nuevo_texto = input("Texto a agregar: ")
        with open(ruta, 'a') as f:
            f.write(f"\n{nuevo_texto}")
        escribir_log(f"{usuario} escribió en el archivo '{ruta}'.")
    else:
        print("Archivo no encontrado.")
        escribir_log(f"{usuario} intentó escribir en un archivo inexistente: '{ruta}'.")

def crear_directorio():
    ruta = input("Ruta del nuevo directorio: ")
    try:
        os.makedirs(ruta, exist_ok=False)
        print(f"Directorio '{ruta}' creado exitosamente.")
        escribir_log(f"Directorio '{ruta}' creado por {get_usuario_actual()}.")
    except FileExistsError:
        print("El directorio ya existe.")
        escribir_log(f"{get_usuario_actual()} intentó crear un directorio ya existente: '{ruta}'.")

