
import time
from collections import deque
from logs import escribir_log

procesos = []

def agregar_proceso(pid, nombre, duracion):
    procesos.append({"pid": pid, "nombre": nombre, "duracion": duracion, "estado": "esperando"})

def fifo():
    print("\n--- Planificación FIFO ---")
    escribir_log("Inicio planificación FIFO")
    for proceso in procesos:
        print(f"Ejecutando proceso {proceso['pid']} ({proceso['nombre']})...")
        proceso["estado"] = "ejecutando"
        escribir_log(f"Proceso {proceso['pid']} ejecutándose (FIFO)")
        time.sleep(proceso["duracion"])
        proceso["estado"] = "finalizado"
        escribir_log(f"Proceso {proceso['pid']} finalizado (FIFO)")
    print("--- Fin planificación FIFO ---")

def round_robin(quantum=2):
    print("\n--- Planificación Round Robin ---")
    escribir_log("Inicio planificación Round Robin")
    cola = deque(procesos)

    while cola:
        proceso = cola.popleft()
        if proceso["estado"] == "finalizado":
            continue

        print(f"Ejecutando proceso {proceso['pid']} ({proceso['nombre']}) por {quantum} segundos...")
        escribir_log(f"Proceso {proceso['pid']} ejecutándose (RR)")

        time.sleep(min(quantum, proceso["duracion"]))

        proceso["duracion"] -= quantum
        if proceso["duracion"] > 0:
            proceso["estado"] = "esperando"
            cola.append(proceso)
        else:
            proceso["estado"] = "finalizado"
            escribir_log(f"Proceso {proceso['pid']} finalizado (RR)")

    print("--- Fin planificación Round Robin ---")

def planificar():
    print("\nElige algoritmo de planificación:")
    print("1. FIFO")
    print("2. Round Robin")
    opcion = input("Selecciona una opción: ")

    if not procesos:
        print("No hay procesos por planificar.")
        return

    if opcion == "1":
        fifo()
    elif opcion == "2":
        quantum = int(input("Ingresa el quantum para Round Robin (segundos): "))
        round_robin(quantum)
    else:
        print("Opción no válida.")
