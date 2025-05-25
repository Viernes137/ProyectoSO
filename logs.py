from datetime import datetime

LOG_FILE = "/home/vi3rn35/Documents/Escuela/3er semestre/SO/proyecto_final/logs_file.txt"

def escribir_log(mensaje):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {mensaje}\n")

def mostrar_logs():
    try:
        with open(LOG_FILE, "r") as f:
            print("\n=== Logs del sistema ===")
            for linea in f:
                print(linea.strip())
    except FileNotFoundError:
        print("No se encontró el archivo de logs.")