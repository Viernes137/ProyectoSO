from login import get_usuario_actual, tiene_permisos_root
from logs import escribir_log
import random
import time
from datetime import datetime
import threading
# Importar la función de agregar proceso del planificador
from planificador import agregar_proceso

# Diccionario para almacenar los procesos del sistema
procesos_sistema = {}
contador_pid = 1000  # Contador para generar PIDs únicos

# Estados de procesos
ESTADOS = {
    'NUEVO': 'nuevo',
    'EJECUTANDO': 'ejecutando',
    'ESPERANDO': 'esperando',
    'PAUSADO': 'pausado',
    'ZOMBIE': 'zombie',
    'TERMINADO': 'terminado'
}

# Señales simuladas
SENALES = {
    'SIGTERM': 15,  # Terminar proceso
    'SIGSTOP': 19,  # Pausar proceso
    'SIGCONT': 18,  # Continuar proceso
    'SIGKILL': 9,   # Matar proceso (no se puede ignorar)
    'SIGCHLD': 17   # Proceso hijo terminado
}

def administrar_procesos():
    """Menú principal para la gestión de procesos"""
    while True:
        print("\n--- Gestión de Procesos ---")
        print("1. Crear proceso (fork)")
        print("2. Ejecutar comando en proceso (exec)")
        print("3. Listar procesos")
        print("4. Ver árbol de procesos")
        print("5. Enviar señal a proceso")
        print("6. Esperar proceso hijo (wait)")
        print("7. Ver procesos zombie")
        print("8. Monitor de sistema")
        print("9. Volver al menú principal")
        
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            fork_proceso()
        elif opcion == "2":
            exec_proceso()
        elif opcion == "3":
            listar_procesos()
        elif opcion == "4":
            mostrar_arbol_procesos()
        elif opcion == "5":
            enviar_senal()
        elif opcion == "6":
            wait_proceso()
        elif opcion == "7":
            mostrar_zombies()
        elif opcion == "8":
            monitor_sistema()
        elif opcion == "9":
            break
        else:
            print("Opción no válida.")

def fork_proceso():
    """Simula fork() - Crea un proceso hijo"""
    global contador_pid
    
    print("\n=== SIMULACIÓN DE fork() ===")
    
    # Verificar si hay un proceso padre seleccionado
    listar_procesos_propios()
    
    try:
        pid_padre = input("PID del proceso padre (Enter para usar proceso actual): ").strip()
        if pid_padre:
            pid_padre = int(pid_padre)
            if pid_padre not in procesos_sistema:
                print("Proceso padre no encontrado.")
                return
        else:
            # Crear un proceso padre si no existe
            pid_padre = crear_proceso_padre()
    except ValueError:
        print("PID inválido.")
        return
    
    proceso_padre = procesos_sistema[pid_padre]
    usuario = get_usuario_actual()
    
    # Verificar permisos
    if not (tiene_permisos_root() or proceso_padre['propietario'] == usuario):
        print("No tienes permisos para crear procesos hijos de este proceso.")
        return
    
    # Crear proceso hijo
    pid_hijo = contador_pid
    contador_pid += 1
    
    nombre_hijo = input("Nombre del proceso hijo: ") or f"{proceso_padre['nombre']}_child"
    
    # Simular fork() - el proceso hijo hereda del padre
    proceso_hijo = {
        'pid': pid_hijo,
        'ppid': pid_padre,  # Process Parent ID
        'nombre': nombre_hijo,
        'comando': proceso_padre['comando'],  # Hereda el comando del padre
        'propietario': proceso_padre['propietario'],
        'estado': ESTADOS['NUEVO'],
        'prioridad': proceso_padre['prioridad'],
        'tiempo_inicio': datetime.now(),
        'cpu_uso': 0,
        'memoria_uso': random.randint(5, 50),  # Los hijos usan menos memoria inicialmente
        'procesos_hijos': [],
        'es_hijo': True,
        'padre_esperando': False,
        'codigo_salida': None,
        'en_planificacion': False,
        'duracion_estimada': None
    }
    
    # Agregar hijo al sistema y al padre
    procesos_sistema[pid_hijo] = proceso_hijo
    proceso_padre['procesos_hijos'].append(pid_hijo)
    
    # Simular la ejecución del fork
    print(f"\n[SIMULACIÓN fork()]")
    print(f"Proceso padre PID: {pid_padre}")
    print(f"Proceso hijo creado PID: {pid_hijo}")
    print(f"El proceso hijo hereda el entorno del padre")
    
    # Agregar al planificador si se desea planificar
    duracion = input("Duración estimada para planificador (en segundos, Enter para omitir): ").strip()
    if duracion.isdigit():
        proceso_hijo['duracion_estimada'] = int(duracion)
        agregar_proceso(pid_hijo, nombre_hijo, int(duracion))
        proceso_hijo['en_planificacion'] = True

    # Cambiar estado del hijo a ejecutando
    time.sleep(1)
    proceso_hijo['estado'] = ESTADOS['EJECUTANDO']
    proceso_hijo['cpu_uso'] = random.randint(1, 10)
    
    escribir_log(f"fork(): Proceso {pid_padre} creó proceso hijo {pid_hijo}")
    print(f"Proceso hijo {pid_hijo} ({nombre_hijo}) creado y ejecutándose")

def exec_proceso():
    """Simula exec() - Reemplaza la imagen del proceso con un nuevo programa"""
    print("\n=== SIMULACIÓN DE exec() ===")
    
    listar_procesos_propios()
    
    try:
        pid = int(input("PID del proceso para exec(): "))
    except ValueError:
        print("PID inválido.")
        return
    
    if pid not in procesos_sistema:
        print("Proceso no encontrado.")
        return
    
    proceso = procesos_sistema[pid]
    usuario = get_usuario_actual()
    
    # Verificar permisos
    if not (tiene_permisos_root() or proceso['propietario'] == usuario):
        print("No tienes permisos para ejecutar exec() en este proceso.")
        return
    
    if proceso['estado'] == ESTADOS['TERMINADO']:
        print("No se puede ejecutar exec() en un proceso terminado.")
        return
    
    # Solicitar nuevo programa
    nuevo_programa = input("Ruta del nuevo programa a ejecutar: ")
    nuevos_args = input("Argumentos (opcional): ")
    
    # Simular exec() - reemplazar imagen del proceso
    print(f"\n[SIMULACIÓN exec()]")
    print(f"Reemplazando imagen del proceso PID {pid}")
    print(f"Programa anterior: {proceso['comando']}")
    print(f"Nuevo programa: {nuevo_programa}")
    
    # Simular el tiempo de carga del nuevo programa
    print("Cargando nuevo programa...")
    time.sleep(2)
    
    # Actualizar proceso con nueva imagen
    proceso['comando'] = f"{nuevo_programa} {nuevos_args}".strip()
    proceso['nombre'] = nuevo_programa.split('/')[-1]  # Tomar solo el nombre del archivo
    proceso['tiempo_inicio'] = datetime.now()  # Nuevo tiempo de inicio
    proceso['cpu_uso'] = random.randint(5, 20)
    proceso['memoria_uso'] += random.randint(10, 100)  # Puede usar más memoria
    
    escribir_log(f"exec(): Proceso {pid} ejecutó {nuevo_programa}")
    print(f"exec() exitoso. Proceso {pid} ahora ejecuta: {nuevo_programa}")

def wait_proceso():
    """Simula wait() - El proceso padre espera a que termine un hijo"""
    print("\n=== SIMULACIÓN DE wait() ===")
    
    # Mostrar procesos que tienen hijos
    procesos_con_hijos = [(pid, proc) for pid, proc in procesos_sistema.items() 
                        if proc['procesos_hijos'] and proc['propietario'] == get_usuario_actual()]
    
    if not procesos_con_hijos:
        print("No tienes procesos con hijos para esperar.")
        return
    
    print("Procesos padre con hijos:")
    for pid, proceso in procesos_con_hijos:
        hijos_vivos = [h for h in proceso['procesos_hijos'] if h in procesos_sistema]
        print(f"PID {pid} ({proceso['nombre']}) - Hijos: {hijos_vivos}")
    
    try:
        pid_padre = int(input("PID del proceso padre: "))
    except ValueError:
        print("PID inválido.")
        return
    
    if pid_padre not in procesos_sistema:
        print("Proceso padre no encontrado.")
        return
    
    proceso_padre = procesos_sistema[pid_padre]
    
    # Verificar permisos
    if not (tiene_permisos_root() or proceso_padre['propietario'] == get_usuario_actual()):
        print("No tienes permisos para este proceso.")
        return
    
    hijos_vivos = [h for h in proceso_padre['procesos_hijos'] 
    if h in procesos_sistema and procesos_sistema[h]['estado'] != ESTADOS['TERMINADO']]
    
    if not hijos_vivos:
        print("No hay procesos hijos vivos para esperar.")
        return
    
    print(f"[SIMULACIÓN wait()] Proceso {pid_padre} esperando a sus hijos...")
    proceso_padre['padre_esperando'] = True
    proceso_padre['estado'] = ESTADOS['ESPERANDO']
    
    print("Hijos ejecutándose:", hijos_vivos)
    print("Esperando... (simulando trabajo de procesos hijos)")
    
    # Simular trabajo de los hijos
    for i in range(5):
        time.sleep(1)
        for pid_hijo in hijos_vivos[:]:  # Copia de la lista
            if pid_hijo in procesos_sistema:
                hijo = procesos_sistema[pid_hijo]
                # Simular probabilidad de que el hijo termine
                if random.random() < 0.3:  # 30% probabilidad por segundo
                    hijo['estado'] = ESTADOS['ZOMBIE']
                    hijo['codigo_salida'] = random.randint(0, 2)
                    print(f"  Proceso hijo {pid_hijo} terminó con código {hijo['codigo_salida']}")
                    hijos_vivos.remove(pid_hijo)
                    
                    # Enviar señal SIGCHLD al padre
                    escribir_log(f"SIGCHLD enviado a proceso {pid_padre} por hijo {pid_hijo}")
        
        if not hijos_vivos:
            break
        print(f"  Esperando... hijos restantes: {hijos_vivos}")
    
    # Limpiar procesos zombie y reactivar padre
    for pid_hijo in proceso_padre['procesos_hijos'][:]:
        if pid_hijo in procesos_sistema and procesos_sistema[pid_hijo]['estado'] == ESTADOS['ZOMBIE']:
            codigo = procesos_sistema[pid_hijo]['codigo_salida']
            del procesos_sistema[pid_hijo]
            proceso_padre['procesos_hijos'].remove(pid_hijo)
            print(f"Proceso zombie {pid_hijo} limpiado, código de salida: {codigo}")
    
    proceso_padre['padre_esperando'] = False
    proceso_padre['estado'] = ESTADOS['EJECUTANDO']
    
    escribir_log(f"wait(): Proceso {pid_padre} terminó de esperar a sus hijos")
    print(f"wait() completado para proceso {pid_padre}")

def enviar_senal():
    """Simula el envío de señales a procesos"""
    print("\n=== ENVÍO DE SEÑALES ===")
    
    listar_procesos_propios()
    
    try:
        pid = int(input("PID del proceso destino: "))
    except ValueError:
        print("PID inválido.")
        return
    
    if pid not in procesos_sistema:
        print("Proceso no encontrado.")
        return
    
    proceso = procesos_sistema[pid]
    usuario = get_usuario_actual()
    
    # Verificar permisos
    if not (tiene_permisos_root() or proceso['propietario'] == usuario):
        print("No tienes permisos para enviar señales a este proceso.")
        return
    
    print("\nSeñales disponibles:")
    print("1. SIGTERM (15) - Terminar proceso graciosamente")
    print("2. SIGSTOP (19) - Pausar proceso")
    print("3. SIGCONT (18) - Continuar proceso pausado")
    print("4. SIGKILL (9) - Matar proceso inmediatamente")
    
    try:
        opcion = int(input("Selecciona señal: "))
    except ValueError:
        print("Opción inválida.")
        return
    
    if opcion == 1:  # SIGTERM
        if proceso['estado'] != ESTADOS['TERMINADO']:
            print(f"Enviando SIGTERM a proceso {pid}...")
            proceso['estado'] = ESTADOS['TERMINADO']
            proceso['codigo_salida'] = 0
            escribir_log(f"SIGTERM enviado a proceso {pid}")
            print(f"Proceso {pid} terminado graciosamente.")
        else:
            print("El proceso ya está terminado.")
    
    elif opcion == 2:  # SIGSTOP
        if proceso['estado'] == ESTADOS['EJECUTANDO']:
            proceso['estado'] = ESTADOS['PAUSADO']
            escribir_log(f"SIGSTOP enviado a proceso {pid}")
            print(f"Proceso {pid} pausado.")
        else:
            print("El proceso no está en ejecución.")
    
    elif opcion == 3:  # SIGCONT
        if proceso['estado'] == ESTADOS['PAUSADO']:
            proceso['estado'] = ESTADOS['EJECUTANDO']
            escribir_log(f"SIGCONT enviado a proceso {pid}")
            print(f"Proceso {pid} reanudado.")
        else:
            print("El proceso no está pausado.")
    
    elif opcion == 4:  # SIGKILL
        if proceso['estado'] != ESTADOS['TERMINADO']:
            print(f"Enviando SIGKILL a proceso {pid}...")
            proceso['estado'] = ESTADOS['TERMINADO']
            proceso['codigo_salida'] = -9
            escribir_log(f"SIGKILL enviado a proceso {pid}")
            print(f"Proceso {pid} terminado forzosamente.")
        else:
            print("El proceso ya está terminado.")
    
    else:
        print("Señal no válida.")

def mostrar_arbol_procesos():
    """Muestra el árbol de procesos padre-hijo"""
    usuario = get_usuario_actual()
    es_root = tiene_permisos_root()
    
    print("\n=== ÁRBOL DE PROCESOS ===")
    
    # Encontrar procesos raíz (sin padre o padre no existe)
    procesos_raiz = []
    for pid, proceso in procesos_sistema.items():
        if es_root or proceso['propietario'] == usuario:
            if 'ppid' not in proceso or proceso['ppid'] not in procesos_sistema:
                procesos_raiz.append(pid)
    
    if not procesos_raiz:
        print("No hay procesos para mostrar.")
        return
    
    def imprimir_proceso(pid, nivel=0):
        if pid not in procesos_sistema:
            return
        
        proceso = procesos_sistema[pid]
        indent = "  " * nivel
        symbol = "├─" if nivel > 0 else ""
        
        print(f"{indent}{symbol} PID:{pid} {proceso['nombre']} [{proceso['estado']}] "f"({proceso['propietario']}) CPU:{proceso['cpu_uso']}%")
        
        # Mostrar hijos
        for hijo_pid in proceso['procesos_hijos']:
            if hijo_pid in procesos_sistema:
                imprimir_proceso(hijo_pid, nivel + 1)
    
    for pid_raiz in sorted(procesos_raiz):
        imprimir_proceso(pid_raiz)

def mostrar_zombies():
    """Muestra procesos en estado zombie"""
    usuario = get_usuario_actual()
    es_root = tiene_permisos_root()
    
    zombies = [(pid, proc) for pid, proc in procesos_sistema.items() 
            if proc['estado'] == ESTADOS['ZOMBIE'] and 
            (es_root or proc['propietario'] == usuario)]
    
    if not zombies:
        print("No hay procesos zombie.")
        return
    
    print("\n=== PROCESOS ZOMBIE ===")
    print(f"{'PID':<8} {'Nombre':<20} {'PPID':<8} {'Código':<8} {'Tiempo'}")
    print("-" * 60)
    
    for pid, proceso in zombies:
        tiempo_zombie = (datetime.now() - proceso['tiempo_inicio']).seconds
        ppid = proceso.get('ppid', 'N/A')
        codigo = proceso.get('codigo_salida', 'N/A')
        print(f"{pid:<8} {proceso['nombre']:<20} {ppid:<8} {codigo:<8} {tiempo_zombie}s")

def listar_procesos():
    """Lista todos los procesos del sistema con información detallada"""
    usuario = get_usuario_actual()
    es_root = tiene_permisos_root()
    
    if not procesos_sistema:
        print("No hay procesos en ejecución.")
        return
    
    print("\n--- Lista de Procesos ---")
    print(f"{'PID':<8} {'PPID':<8} {'Nombre':<20} {'Usuario':<15} {'Estado':<12} {'CPU%':<6} {'Mem(MB)':<8}")
    print("-" * 95)
    
    for pid, proceso in sorted(procesos_sistema.items()):
        if es_root or proceso['propietario'] == usuario:
            ppid = proceso.get('ppid', 'N/A')
            print(f"{proceso['pid']:<8} {ppid:<8} {proceso['nombre']:<20} "f"{proceso['propietario']:<15} {proceso['estado']:<12} "f"{proceso['cpu_uso']:<6} {proceso['memoria_uso']:<8}")
    
    escribir_log(f"{usuario} consultó la lista de procesos")

def listar_procesos_propios():
    """Lista solo los procesos del usuario actual"""
    usuario = get_usuario_actual()
    
    procesos_propios = [(pid, proc) for pid, proc in procesos_sistema.items() 
                        if proc['propietario'] == usuario or tiene_permisos_root()]
    
    if not procesos_propios:
        print("No tienes procesos en ejecución.")
        return
    
    print("\nTus procesos:")
    for pid, proceso in procesos_propios:
        estado_info = f"[{proceso['estado']}]"
        hijos_info = f" (hijos: {len(proceso['procesos_hijos'])})" if proceso['procesos_hijos'] else ""
        print(f"  PID {pid}: {proceso['nombre']} {estado_info}{hijos_info}")

def crear_proceso_padre():
    """Crea un proceso padre básico"""
    global contador_pid
    
    nombre = input("Nombre del proceso padre: ") or "proceso_principal"
    usuario = get_usuario_actual()
    pid = contador_pid
    contador_pid += 1
    
    proceso = {
        'pid': pid,
        'nombre': nombre,
        'comando': f'/usr/bin/{nombre}',
        'propietario': usuario,
        'estado': ESTADOS['EJECUTANDO'],
        'prioridad': 5,
        'tiempo_inicio': datetime.now(),
        'cpu_uso': random.randint(1, 15),
        'memoria_uso': random.randint(50, 200),
        'procesos_hijos': [],
        'es_hijo': False,
        'padre_esperando': False,
        'codigo_salida': None,
        'en_planificacion': False,
        'duracion_estimada': None
    }
    
    procesos_sistema[pid] = proceso

    # Agregar al planificador si se desea planificar
    duracion = input("Duración estimada para planificador (en segundos, Enter para omitir): ").strip()
    if duracion.isdigit():
        proceso['duracion_estimada'] = int(duracion)
        agregar_proceso(pid, nombre, int(duracion))
        proceso['en_planificacion'] = True
    escribir_log(f"Proceso padre '{nombre}' (PID: {pid}) creado por {usuario}")
    print(f"Proceso padre '{nombre}' creado con PID: {pid}")
    
    return pid

def monitor_sistema():
    """Monitor del sistema con información de procesos padre-hijo"""
    usuario = get_usuario_actual()
    
    if not procesos_sistema:
        print("No hay procesos para monitorear.")
        return
    
    print("\n--- Monitor del Sistema ---")
    print("Presiona Enter para actualizar, 'q' para salir")
    
    while True:
        print("\n" * 2)
        print("=== MONITOR DE PROCESOS ===")
        
        # Estadísticas generales
        estados_count = {}
        for proceso in procesos_sistema.values():
            estado = proceso['estado']
            estados_count[estado] = estados_count.get(estado, 0) + 1
        
        print(f"Total procesos: {len(procesos_sistema)}")
        for estado, count in estados_count.items():
            print(f"  {estado}: {count}")
        
        # Procesos con más hijos
        procesos_con_hijos = [(pid, len(proc['procesos_hijos'])) 
                            for pid, proc in procesos_sistema.items() 
                            if proc['procesos_hijos']]
        
        if procesos_con_hijos:
            procesos_con_hijos.sort(key=lambda x: x[1], reverse=True)
            print(f"\nProcesos con más hijos:")
            for pid, num_hijos in procesos_con_hijos[:3]:
                proceso = procesos_sistema[pid]
                if tiene_permisos_root() or proceso['propietario'] == usuario:
                    print(f"  PID {pid} ({proceso['nombre']}): {num_hijos} hijos")
        
        # Simular cambios en el sistema
        for proceso in procesos_sistema.values():
            if proceso['estado'] == ESTADOS['EJECUTANDO']:
                proceso['cpu_uso'] = max(0, min(100, proceso['cpu_uso'] + random.randint(-3, 3)))
        
        entrada = input("\nPresiona Enter para actualizar, 'q' para salir: ")
        if entrada.lower() == 'q':
            break
    
    escribir_log(f"{usuario} usó el monitor del sistema")

# Función para crear proceso simple desde el menú principal (compatibilidad con main.py)
def crear_proceso_simple():
    """Función simplificada para crear proceso desde main.py"""
    return crear_proceso_padre()

# Función para inicializar algunos procesos de ejemplo
def inicializar_procesos_sistema():
    """Crea algunos procesos del sistema por defecto"""
    global contador_pid
    
    procesos_default = [
        {'nombre': 'init', 'comando': '/sbin/init', 'propietario': 'system'},
        {'nombre': 'kernel', 'comando': '/kernel', 'propietario': 'system'},
        {'nombre': 'systemd', 'comando': '/usr/lib/systemd/systemd', 'propietario': 'system'}
    ]
    
    for proc_data in procesos_default:
        if contador_pid not in procesos_sistema:
            proceso = {
                'pid': contador_pid,
                'nombre': proc_data['nombre'],
                'comando': proc_data['comando'],
                'propietario': proc_data['propietario'],
                'estado': ESTADOS['EJECUTANDO'],
                'prioridad': 1,
                'tiempo_inicio': datetime.now(),
                'cpu_uso': random.randint(1, 5),
                'memoria_uso': random.randint(50, 200),
                'procesos_hijos': [],
                'es_hijo': False,
                'padre_esperando': False,
                'codigo_salida': None,
                'en_planificacion': False,
                'duracion_estimada': None
            }
            procesos_sistema[contador_pid] = proceso
            contador_pid += 1

# Inicializar procesos del sistema al importar el módulo
if not procesos_sistema:
    inicializar_procesos_sistema()