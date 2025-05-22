#include "hdrs/login.h"

void mostrar_menu()
{
    cout << "\n=== Menú principal ===\n";
    cout << "1. Crear proceso\n";
    cout << "2. Ejecutar planificación CPU\n";
    cout << "3. Administrar archivos\n";
    cout << "4. Mostrar logs\n";
    cout << "5. Salir\n";
    cout << "Selecciona una opción: ";
}

void crear_proceso()
{
    cout << "[Simulación] Aquí iría el módulo de gestión de procesos.\n";
}

void planificacion_cpu()
{
    cout << "[Simulación] Aquí iría el planificador FIFO o Round Robin.\n";
}

void administrar_archivos()
{
    cout << "[Simulación] Aquí iría el módulo de sistema de archivos.\n";
}

void mostrar_logs()
{
    ifstream log("logs.txt");
    if (!log.is_open())
    {
        cout << "No se pudo abrir el archivo de logs.\n";
        return;
    }

    cout << "\n=== Logs del sistema ===\n";
    string linea;
    while (getline(log, linea))
    {
        cout << linea << '\n';
    }
    log.close();
}

int main()
{
    if (!login())
        return 1;

    int opcion;
    while (true)
    {
        mostrar_menu();
        cin >> opcion;
        cin.ignore();

        switch (opcion)
        {
        case 1:
            crear_proceso();
            break;
        case 2:
            planificacion_cpu();
            break;
        case 3:
            administrar_archivos();
            break;
        case 4:
            mostrar_logs();
            break;
        case 5:
            cout << "Saliendo del sistema...\n";
            return 0;
        default:
            cout << "Opción no válida.\n";
        }
    }
}
