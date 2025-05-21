import getpass

usuario_actual = ""
es_root = False

def login():
    global usuario_actual, es_root

    print("=== SIMULADOR SO ===")
    user = input("Usuario: ")
    passwd = getpass.getpass("Contraseña: ")

    if (user == "root" and passwd == "toor") or (user == "bruno" and passwd == "1234"):
        usuario_actual = user
        es_root = (user == "root")
        print(f"\nBienvenido, {usuario_actual}\n")
        return True
    else:
        print("Login incorrecto")
        return False

def get_usuario_actual():
    return usuario_actual

def tiene_permisos_root():
    return es_root
