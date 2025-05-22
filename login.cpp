#include "hdrs/login.h"

string usuario_actual = "";
bool es_root = false;

bool login()
{
    string user, pass;
    cout << "=== SIMULADOR SO ===\n";
    cout << "Usuario: ";
    cin >> user;
    cout << "Contraseña: ";
    cin >> pass;

    if ((user == "root" && pass == "toor") || (user == "bruno" && pass == "1234"))
    {
        usuario_actual = user;
        es_root = (user == "root");
        cout << "\nBienvenido, " << usuario_actual << "\n";
        return true;
    }
    else
    {
        cout << "Login incorrecto\n";
        return false;
    }
}
