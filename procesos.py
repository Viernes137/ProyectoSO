from login import get_usuario_actual, tiene_permisos_root
from logs import escribir_log
import random
import time
from datetime import datetime
# Importar la función de agregar proceso del planificador
from planificador import agregar_proceso

# Diccionario para almacenar los procesos del sistema
procesos_sistema = {}
contador_pid = 1000  # Contador para generar PIDs únicos

def administrar_procesos():
    """Menú principal para la gestión de procesos"""
    while True:
        print("\n--- Gestión de Procesos ---")
        print("1. Crear proceso")
        print("2. Listar procesos")
        print("3. Ver detalles de proceso")
        print("4. Terminar proceso")
        print("5. Cambiar prioridad")
        print("6. Pausar proceso")
        print("7. Reanudar proceso")
        print("8. Monitor de sistema")
        print("9. Volver al menú principal")
        
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            crear_proceso()
        elif opcion == "2":
            listar_procesos()
        elif opcion == "3":
            ver_detalles_proceso()
        elif opcion == "4":
            terminar_proceso()
        elif opcion == "5":
            cambiar_prioridad()
        elif opcion == "6":
            pausar_proceso()
        elif opcion == "7":
            reanudar_proceso()
        elif opcion == "8":
            monitor_sistema()
        elif opcion == "9":
            break
        else:
            print("Opción no válida.")

def crear_proceso():
    """Crea un nuevo proceso en el sistema"""
    global contador_pid
    
    nombre = input("Nombre del proceso: ")
    comando = input("Comando/ruta del programa: ")
    prioridad = input("Prioridad (1-10, por defecto 5): ") or "5"
    
    # Preguntar si se quiere agregar a la cola de planificación
    agregar_planificacion = input("¿Agregar a la cola de planificación? (s/n, por defecto n): ").lower()
    duracion = None
    
    if agregar_planificacion == 's':
        try:
            duracion = int(input("Duración estimada en segundos: "))
        except ValueError:
            duracion = 5  # Valor por defecto
            print("Duración inválida, usando 5 segundos por defecto.")
    
    try:
        prioridad = int(prioridad)
        if prioridad < 1 or prioridad > 10:
            prioridad = 5
    except ValueError:
        prioridad = 5
    
    usuario = get_usuario_actual()
    pid = contador_pid
    contador_pid += 1
    
    # Crear el proceso en el sistema
    proceso = {
        'pid': pid,
        'nombre': nombre,
        'comando': comando,
        'propietario': usuario,
        'estado': 'ejecutando',
        'prioridad': prioridad,
        'tiempo_inicio': datetime.now(),
        'cpu_uso': random.randint(1, 15),  # Simulación de uso de CPU
        'memoria_uso': random.randint(10, 500),  # MB de memoria
        'procesos_hijos': [],
        'en_planificacion': agregar_planificacion == 's',
        'duracion_estimada': duracion
    }
    
    procesos_sistema[pid] = proceso
    
    # Si se eligió agregar a planificación, agregarlo también al planificador
    if agregar_planificacion == 's':
        agregar_proceso(pid, nombre, duracion)
        escribir_log(f"Proceso '{nombre}' (PID: {pid}) creado por {usuario} y agregado a planificación")
        print(f"Proceso '{nombre}' creado exitosamente con PID: {pid} y agregado a la cola de planificación")
    else:
        escribir_log(f"Proceso '{nombre}' (PID: {pid}) creado por {usuario}")
        print(f"Proceso '{nombre}' creado exitosamente con PID: {pid}")

def listar_procesos():
    """Lista todos los procesos del sistema"""
    usuario = get_usuario_actual()
    es_root = tiene_permisos_root()
    
    if not procesos_sistema:
        print("No hay procesos en ejecución.")
        return
    
    print("\n--- Lista de Procesos ---")
    print(f"{'PID':<8} {'Nombre':<20} {'Usuario':<15} {'Estado':<12} {'CPU%':<6} {'Mem(MB)':<8} {'Prioridad':<10} {'Planif.'}")
    print("-" * 95)
    
    for pid, proceso in procesos_sistema.items():
        # Solo mostrar procesos propios o si es root
        if es_root or proceso['propietario'] == usuario:
            planif_status = "Sí" if proceso.get('en_planificacion', False) else "No"
            print(f"{proceso['pid']:<8} {proceso['nombre']:<20} {proceso['propietario']:<15} "
                  f"{proceso['estado']:<12} {proceso['cpu_uso']:<6} {proceso['memoria_uso']:<8} "
                  f"{proceso['prioridad']:<10} {planif_status}")
    
    escribir_log(f"{usuario} consultó la lista de procesos")

def ver_detalles_proceso():
    """Muestra detalles específicos de un proceso"""
    try:
        pid = int(input("PID del proceso: "))
    except ValueError:
        print("PID inválido.")
        return
    
    usuario = get_usuario_actual()
    
    if pid not in procesos_sistema:
        print("Proceso no encontrado.")
        return
    
    proceso = procesos_sistema[pid]
    
    # Verificar permisos
    if not (tiene_permisos_root() or proceso['propietario'] == usuario):
        print("No tienes permisos para ver este proceso.")
        escribir_log(f"ACCESO DENEGADO: {usuario} intentó ver detalles del proceso PID {pid}")
        return
    
    # Mostrar detalles
    print(f"\n--- Detalles del Proceso PID {pid} ---")
    print(f"Nombre: {proceso['nombre']}")
    print(f"Comando: {proceso['comando']}")
    print(f"Propietario: {proceso['propietario']}")
    print(f"Estado: {proceso['estado']}")
    print(f"Prioridad: {proceso['prioridad']}")
    print(f"Tiempo de inicio: {proceso['tiempo_inicio'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Uso de CPU: {proceso['cpu_uso']}%")
    print(f"Uso de memoria: {proceso['memoria_uso']} MB")
    print(f"En planificación: {'Sí' if proceso.get('en_planificacion', False) else 'No'}")
    
    if proceso.get('duracion_estimada'):
        print(f"Duración estimada: {proceso['duracion_estimada']} segundos")
    
    if proceso['procesos_hijos']:
        print(f"Procesos hijos: {', '.join(map(str, proceso['procesos_hijos']))}")
    
    escribir_log(f"{usuario} consultó detalles del proceso PID {pid}")

def terminar_proceso():
    """Termina un proceso específico"""
    try:
        pid = int(input("PID del proceso a terminar: "))
    except ValueError:
        print("PID inválido.")
        return
    
    usuario = get_usuario_actual()
    
    if pid not in procesos_sistema:
        print("Proceso no encontrado.")
        return
    
    proceso = procesos_sistema[pid]
    
    # Verificar permisos (solo el propietario o root pueden terminar)
    if not (tiene_permisos_root() or proceso['propietario'] == usuario):
        print("No tienes permisos para terminar este proceso.")
        escribir_log(f"ACCESO DENEGADO: {usuario} intentó terminar proceso PID {pid}")
        return
    
    # Confirmar terminación
    confirmar = input(f"¿Estás seguro de terminar el proceso '{proceso['nombre']}'? (s/n): ")
    if confirmar.lower() == 's':
        del procesos_sistema[pid]
        print(f"Proceso PID {pid} terminado exitosamente.")
        escribir_log(f"{usuario} terminó el proceso '{proceso['nombre']}' (PID: {pid})")
    else:
        print("Operación cancelada.")

def cambiar_prioridad():
    """Cambia la prioridad de un proceso"""
    try:
        pid = int(input("PID del proceso: "))
        nueva_prioridad = int(input("Nueva prioridad (1-10): "))
    except ValueError:
        print("Valores inválidos.")
        return
    
    if nueva_prioridad < 1 or nueva_prioridad > 10:
        print("La prioridad debe estar entre 1 y 10.")
        return
    
    usuario = get_usuario_actual()
    
    if pid not in procesos_sistema:
        print("Proceso no encontrado.")
        return
    
    proceso = procesos_sistema[pid]
    
    # Solo root o el propietario pueden cambiar prioridad
    if not (tiene_permisos_root() or proceso['propietario'] == usuario):
        print("No tienes permisos para cambiar la prioridad de este proceso.")
        escribir_log(f"ACCESO DENEGADO: {usuario} intentó cambiar prioridad del proceso PID {pid}")
        return
    
    prioridad_anterior = proceso['prioridad']
    proceso['prioridad'] = nueva_prioridad
    print(f"Prioridad del proceso PID {pid} cambiada de {prioridad_anterior} a {nueva_prioridad}")
    escribir_log(f"{usuario} cambió prioridad del proceso PID {pid} de {prioridad_anterior} a {nueva_prioridad}")

def pausar_proceso():
    """Pausa un proceso (cambia estado a 'pausado')"""
    try:
        pid = int(input("PID del proceso a pausar: "))
    except ValueError:
        print("PID inválido.")
        return
    
    usuario = get_usuario_actual()
    
    if pid not in procesos_sistema:
        print("Proceso no encontrado.")
        return
    
    proceso = procesos_sistema[pid]
    
    if not (tiene_permisos_root() or proceso['propietario'] == usuario):
        print("No tienes permisos para pausar este proceso.")
        escribir_log(f"ACCESO DENEGADO: {usuario} intentó pausar proceso PID {pid}")
        return
    
    if proceso['estado'] == 'pausado':
        print("El proceso ya está pausado.")
        return
    
    proceso['estado'] = 'pausado'
    print(f"Proceso PID {pid} pausado exitosamente.")
    escribir_log(f"{usuario} pausó el proceso PID {pid}")

def reanudar_proceso():
    """Reanuda un proceso pausado"""
    try:
        pid = int(input("PID del proceso a reanudar: "))
    except ValueError:
        print("PID inválido.")
        return
    
    usuario = get_usuario_actual()
    
    if pid not in procesos_sistema:
        print("Proceso no encontrado.")
        return
    
    proceso = procesos_sistema[pid]
    
    if not (tiene_permisos_root() or proceso['propietario'] == usuario):
        print("No tienes permisos para reanudar este proceso.")
        escribir_log(f"ACCESO DENEGADO: {usuario} intentó reanudar proceso PID {pid}")
        return
    
    if proceso['estado'] != 'pausado':
        print("El proceso no está pausado.")
        return
    
    proceso['estado'] = 'ejecutando'
    print(f"Proceso PID {pid} reanudado exitosamente.")
    escribir_log(f"{usuario} reanudó el proceso PID {pid}")

def monitor_sistema():
    """Muestra un monitor en tiempo real del sistema"""
    usuario = get_usuario_actual()
    
    if not procesos_sistema:
        print("No hay procesos para monitorear.")
        return
    
    print("\n--- Monitor del Sistema ---")
    print("Presiona Enter para actualizar, 'q' para salir")
    
    while True:
        # Limpiar pantalla (simulado)
        print("\n" * 2)
        print("=== MONITOR DE PROCESOS ===")
        print(f"Procesos activos: {len(procesos_sistema)}")
        
        # Calcular estadísticas
        cpu_total = sum(p['cpu_uso'] for p in procesos_sistema.values())
        memoria_total = sum(p['memoria_uso'] for p in procesos_sistema.values())
        
        print(f"CPU total en uso: {cpu_total}%")
        print(f"Memoria total en uso: {memoria_total} MB")
        print()
        
        # Mostrar top 5 procesos por CPU
        procesos_ordenados = sorted(procesos_sistema.values(), 
                                  key=lambda x: x['cpu_uso'], reverse=True)[:5]
        
        print("TOP 5 PROCESOS POR CPU:")
        print(f"{'PID':<8} {'Nombre':<20} {'CPU%':<6} {'Estado'}")
        print("-" * 45)
        
        for proceso in procesos_ordenados:
            if tiene_permisos_root() or proceso['propietario'] == usuario:
                print(f"{proceso['pid']:<8} {proceso['nombre']:<20} "
                      f"{proceso['cpu_uso']:<6} {proceso['estado']}")
        
        # Simular cambios en el sistema
        for proceso in procesos_sistema.values():
            proceso['cpu_uso'] = max(1, proceso['cpu_uso'] + random.randint(-2, 3))
            if proceso['cpu_uso'] > 100:
                proceso['cpu_uso'] = 100
        
        entrada = input("\nPresiona Enter para actualizar, 'q' para salir: ")
        if entrada.lower() == 'q':
            break
    
    escribir_log(f"{usuario} usó el monitor del sistema")

# Función para crear proceso simple desde el menú principal (compatibilidad con main.py)
def crear_proceso_simple():
    """Función simplificada para crear proceso desde main.py"""
    global contador_pid
    
    nombre = input("Nombre del proceso: ")
    usuario = get_usuario_actual()
    pid = contador_pid
    contador_pid += 1
    
    # Crear el proceso básico
    proceso = {
        'pid': pid,
        'nombre': nombre,
        'comando': f'/usr/bin/{nombre}',
        'propietario': usuario,
        'estado': 'ejecutando',
        'prioridad': 5,
        'tiempo_inicio': datetime.now(),
        'cpu_uso': random.randint(1, 15),
        'memoria_uso': random.randint(10, 500),
        'procesos_hijos': [],
        'en_planificacion': False,
        'duracion_estimada': None
    }
    
    procesos_sistema[pid] = proceso
    escribir_log(f"Proceso '{nombre}' (PID: {pid}) creado por {usuario}")
    print(f"Proceso '{nombre}' creado exitosamente con PID: {pid}")

# Función para inicializar algunos procesos de ejemplo
def inicializar_procesos_sistema():
    """Crea algunos procesos del sistema por defecto"""
    global contador_pid
    
    procesos_default = [
        {'nombre': 'kernel', 'comando': '/kernel', 'propietario': 'system'},
        {'nombre': 'init', 'comando': '/sbin/init', 'propietario': 'system'},
        {'nombre': 'networkd', 'comando': '/usr/sbin/networkd', 'propietario': 'system'}
    ]
    
    for proc_data in procesos_default:
        if contador_pid not in procesos_sistema:  # Evitar duplicados
            proceso = {
                'pid': contador_pid,
                'nombre': proc_data['nombre'],
                'comando': proc_data['comando'],
                'propietario': proc_data['propietario'],
                'estado': 'ejecutando',
                'prioridad': 1,
                'tiempo_inicio': datetime.now(),
                'cpu_uso': random.randint(1, 5),
                'memoria_uso': random.randint(50, 200),
                'procesos_hijos': [],
                'en_planificacion': False,
                'duracion_estimada': None
            }
            procesos_sistema[contador_pid] = proceso
            contador_pid += 1

# Inicializar procesos del sistema al importar el módulo
if not procesos_sistema:  # Solo si no hay procesos ya creados
    inicializar_procesos_sistema()