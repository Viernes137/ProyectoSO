

#def administrar_archivos():
    # print("[Simulación] Aquí iría el módulo de sistema de archivos y control de permisos.")
    # Aquí podrías simular open(), read(), write(), close()

from login import get_usuario_actual, tiene_permisos_root
from logs import escribir_log

archivos_sistema = {}

def administrar_archivos():
    while True:
        print("\n--- Gestión de Archivos ---")
        print("1. Crear archivo")
        print("2. Leer archivo")
        print("3. Escribir archivo")
        print("4. Cerrar archivo (simulado)")
        print("5. Volver al menú principal")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            crear_archivo()
        elif opcion == "2":
            leer_archivo()
        elif opcion == "3":
            escribir_archivo()
        elif opcion == "4":
            cerrar_archivo()
        elif opcion == "5":
            break
        else:
            print("Opción no válida.")

def crear_archivo():
    nombre = input("Nombre del archivo: ")
    propietario = get_usuario_actual()
    contenido = input("Contenido inicial: ")

    archivos_sistema[nombre] = {
        'contenido': contenido,
        'propietario': propietario,
        'permisos': {'lectura': True, 'escritura': True}
    }

    escribir_log(f"Archivo '{nombre}' creado por {propietario}.")
    print(f"Archivo '{nombre}' creado exitosamente.")

def leer_archivo():
    nombre = input("Nombre del archivo a leer: ")
    usuario = get_usuario_actual()

    if nombre in archivos_sistema:
        archivo = archivos_sistema[nombre]
        if archivo['permisos']['lectura'] or usuario == archivo['propietario'] or tiene_permisos_root():
            print(f"Contenido de '{nombre}': {archivo['contenido']}")
            escribir_log(f"{usuario} leyó el archivo '{nombre}'.")
        else:
            print("No tienes permisos de lectura.")
            escribir_log(f"ACCESO DENEGADO: {usuario} intentó leer '{nombre}'.")
    else:
        print("Archivo no encontrado.")

def escribir_archivo():
    nombre = input("Nombre del archivo a escribir: ")
    usuario = get_usuario_actual()

    if nombre in archivos_sistema:
        archivo = archivos_sistema[nombre]
        if archivo['permisos']['escritura'] or usuario == archivo['propietario'] or tiene_permisos_root():
            nuevo_texto = input("Texto a agregar: ")
            archivo['contenido'] += f"\n{nuevo_texto}"
            escribir_log(f"{usuario} escribió en el archivo '{nombre}'.")
        else:
            print("No tienes permisos de escritura.")
            escribir_log(f"ACCESO DENEGADO: {usuario} intentó escribir en '{nombre}'.")
    else:
        print("Archivo no encontrado.")

def cerrar_archivo():
    print("Simulación: archivo cerrado correctamente.")
