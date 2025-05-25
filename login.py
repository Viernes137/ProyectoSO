import getpass

usuario_actual = ""
es_root = False
docs = "/home/vi3rn35/Documents/Escuela/3er semestre/SO/proyecto_final/users.txt"

usuarios = {}
with open(docs, "r") as archivo:
    for linea in archivo:
        user, pwd = linea.strip().split(":")
        usuarios[user] = pwd


def login():
    global usuario_actual, es_root

    print("=== SIMULADOR SO ===")
    user = input("Usuario: ")
    passwd = getpass.getpass("Contraseña: ")

    
    if (usuarios.get(user) == passwd):
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

def mod_usuarios(bnd):
    if (bnd == False):
        print("El usuario no tiene los permisos necesarios para acceder a esta configuracion.")
    else:
        config = input(''' 
1.- Ver usuarios
2.- Crear nuevo usuario 
--> ''')
        if config == "1":
            print("chimichanga")
            try:
                with open(docs, "r") as f:
                    print("\n=== usuarios ===")
                    for linea in f:
                        print(linea.strip())
            except FileNotFoundError:
                print("No se encontró el archivo de logs.")
            
        elif config == "2":
            user = input("Nombre del usuario: ")
            contraseña  = getpass.getpass("Contraseña: ")
            with open(docs, "a") as archivo:
                archivo.write(user+":"+contraseña+"\n")
        

