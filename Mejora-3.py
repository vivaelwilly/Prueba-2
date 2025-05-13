import os
import datetime
import shutil

ADMIN_PASSWORD = "victomonan1"
CAMPUS_LIST_FILE = "campus_lista.txt"
USUARIOS_FILE = "usuarios.txt"
BACKUP_DIR = "backups"  

# Cargar o crear lista de campus
try:
    with open(CAMPUS_LIST_FILE, "r") as f:
        campus = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    campus = ["zona core", "campus uno", "campus matriz", "sector outsourcing"]
    with open(CAMPUS_LIST_FILE, "w") as f:
        for c in campus:
            f.write(c + "\n")

campus_octetos = {campus[i]: (i + 1) * 10 for i in range(len(campus))}

def guardar_lista_campus():
    with open(CAMPUS_LIST_FILE, "w") as f:
        for c in campus:
            f.write(c + "\n")

def login():
    print("¿Eres admin o usuario?")
    print("1. Admin\n2. Usuario")
    tipo = input("Selecciona tu rol: ")
    if tipo == "1":
        clave = input("Introduce la contraseña del admin: ")
        if clave == ADMIN_PASSWORD:
            return "admin", None
        else:
            print("Contraseña incorrecta.")
            exit()
    elif tipo == "2":
        try:
            open(USUARIOS_FILE, "x").close()
        except FileExistsError:
            pass

        print("1. Registrarse\n2. Iniciar sesión")
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            nombre = input("Nombre de usuario: ")
            clave = input("Contraseña: ")
            print("Elige tu campus:")
            for i, c in enumerate(campus, 1):
                print(f"{i}. {c}")
            idx = int(input("Opción: ")) - 1
            usuario_campus = campus[idx]
            with open(USUARIOS_FILE, "a") as f:
                f.write(f"{nombre}:{clave}:{usuario_campus}\n")
            print("Usuario registrado correctamente.")
            return "usuario", usuario_campus
        elif opcion == "2":
            nombre = input("Nombre de usuario: ")
            clave = input("Contraseña: ")
            with open(USUARIOS_FILE, "r") as f:
                for line in f:
                    u, p, c = line.strip().split(":")
                    if u == nombre and p == clave:
                        return "usuario", c
            print("Credenciales incorrectas.")
            exit()
    else:
        print("Opción inválida.")
        exit()

def mostrar_dispositivos(campus_actual):
    archivo = campus_actual + ".txt"
    try:
        with open(archivo, "r") as f:
            contenido = f.read().strip()
            if contenido:
                print(f"\nDispositivos en {campus_actual}:")
                print(contenido)
            else:
                print("No hay dispositivos registrados en este campus.")
    except FileNotFoundError:
        print("Archivo de dispositivos no encontrado para este campus.")

def crear_campus():
    nuevo = input("Nombre del nuevo campus: ").strip()
    if nuevo in campus:
        print("Ya existe.")
        return
    campus.append(nuevo)
    campus_octetos[nuevo] = (len(campus)) * 10
    guardar_lista_campus()
    open(nuevo + ".txt", "w").close()
    print("Campus creado.")

def eliminar_campus():
    print("Campus disponibles:")
    for i, c in enumerate(campus, 1):
        print(f"{i}. {c}")
    idx = int(input("Selecciona el campus a eliminar: ")) - 1
    if 0 <= idx < len(campus):
        eliminar = campus[idx]
        try:
            os.remove(eliminar + ".txt")
        except FileNotFoundError:
            pass
        campus.pop(idx)
        guardar_lista_campus()
        print("Campus eliminado.")
    else:
        print("Opción inválida.")

def agregar_dispositivo(campus_actual):
    archivo = campus_actual + ".txt"
    print("Tipo de dispositivo:\n1. Router\n2. Switch\n3. Switch Multicapa\n4. PC")
    tipo = int(input("Opción: "))
    nombre = input("Nombre del dispositivo: ")

    jerarquia_txt = "N/A"
    if tipo in [1, 2, 3]:
        print("Jerarquía:\n1. Núcleo\n2. Distribución\n3. Acceso")
        jerarquia = int(input("Opción: "))
        jerarquia_txt = ["Núcleo", "Distribución", "Acceso"][jerarquia - 1]
    elif tipo == 4:
        jerarquia_txt = "Acceso"

    penultimo = campus_octetos.get(campus_actual, 90)

    #Maxi

    def obtener_ips_existentes(campus):
        ips = set()
        try:
            with open(campus + ".txt", "r") as f:
                for line in f:
                    if line.startswith("IP: "):
                        ips.add(line.strip().split()[1])
        except FileNotFoundError:
            pass
        return ips
    
    ips_existentes = obtener_ips_existentes(campus_actual)

    while True:
        ip = input(f"Ingresa la IP (ej: 172.16.{penultimo}.X): ")
        
        partes = ip.strip().split(".")
        if len(partes) != 4 or not all(p.isdigit() for p in partes):
            print("Formato de IP incorrecto. Debe ser X.X.X.X donde X son números")
            continue
            
        if not (int(partes[2]) == penultimo and 1 <= int(partes[3]) <= 50):
            print(f"IP inválida. Penúltimo octeto debe ser {penultimo} y el último entre 1-50")
            continue
    
        if ip in ips_existentes:
            print(f"¡ALERTA! La IP {ip} ya está configurada en este campus.")
            print("Por favor ingrese una IP diferente.")
            continue
            
        break 

    vlans = input("Ingrese las VLANs (separadas por coma): ").split(",")

    servicios = []
    if tipo in [1, 2, 3]:
        servicios_opciones = ["Datos", "VLAN", "Trunking"]
        if tipo == 3:
            servicios_opciones.append("Enrutamiento")
        while True:
            print("Servicios disponibles:")
            for i, s in enumerate(servicios_opciones, 1):
                print(f"{i}. {s}")
            print(f"{len(servicios_opciones)+1}. Terminar")
            sel = int(input("Opción: "))
            if 1 <= sel <= len(servicios_opciones):
                servicios.append(servicios_opciones[sel - 1])
            else:
                break

    with open(archivo, "a") as f:
        f.write("\n---------------------------------\n")
        f.write(f"Nombre del dispositivo: {nombre}\n")
        f.write(f"IP: {ip}\n")
        f.write(f"Jerarquía: {jerarquia_txt}\n")
        f.write("VLANs: " + ", ".join(vlans) + "\n")
        f.write("Servicios: " + ", ".join(servicios) + "\n")
        f.write("---------------------------------\n")

def eliminar_dispositivos(campus_actual):
    archivo = campus_actual + ".txt"
    try:
        with open(archivo, "r") as f:
            contenido = f.read()
    except FileNotFoundError:
        print("No hay dispositivos para eliminar.")
        return

    bloques = contenido.strip().split("---------------------------------")
    dispositivos = [(i, b) for i, b in enumerate(bloques) if "Nombre del dispositivo:" in b]
    for i, b in enumerate(dispositivos, 1):
        nombre = [line for line in b[1].splitlines() if "Nombre del dispositivo:" in line][0]
        print(f"{i}. {nombre.replace('Nombre del dispositivo: ', '')}")
    print(f"{len(dispositivos)+1}. Eliminar todos")
    sel = int(input("Opción: "))
    if sel == len(dispositivos) + 1:
        open(archivo, "w").close()
    elif 1 <= sel <= len(dispositivos):
        bloques.pop(dispositivos[sel-1][0])
        with open(archivo, "w") as f:
            for b in bloques:
                if b.strip():
                    f.write(b.strip() + "\n---------------------------------\n")

# Funcines backup

def crear_backup():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    os.makedirs(backup_path)
    for campus_name in campus:
        campus_file = campus_name + ".txt"
        if os.path.exists(campus_file):
            shutil.copy2(campus_file, backup_path)
    
    if os.path.exists(CAMPUS_LIST_FILE):
        shutil.copy2(CAMPUS_LIST_FILE, backup_path)
    
    if os.path.exists(USUARIOS_FILE):
        shutil.copy2(USUARIOS_FILE, backup_path)
    
    print(f"Backup creado exitosamente: {backup_name}")

def listar_backups():
    if not os.path.exists(BACKUP_DIR):
        print("No hay backups disponibles.")
        return []
    
    backups = sorted(os.listdir(BACKUP_DIR))
    print("\nBackups disponibles:")
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup}")
    return backups

def restaurar_backup():
    backups = listar_backups()
    if not backups:
        return
    
    opcion = int(input("Selecciona el backup a restaurar: ")) - 1
    if 0 <= opcion < len(backups):
        backup_path = os.path.join(BACKUP_DIR, backups[opcion])
        
        for campus_name in campus:
            campus_file = campus_name + ".txt"
            backup_file = os.path.join(backup_path, campus_file)
            if os.path.exists(backup_file):
                shutil.copy2(backup_file, ".")
        
        backup_campus_list = os.path.join(backup_path, CAMPUS_LIST_FILE)
        if os.path.exists(backup_campus_list):
            shutil.copy2(backup_campus_list, ".")
        
        backup_usuarios = os.path.join(backup_path, USUARIOS_FILE)
        if os.path.exists(backup_usuarios):
            shutil.copy2(backup_usuarios, ".")
        
        print("Backup restaurado exitosamente.")
    else:
        print("Opción inválida.")

# INICIO DEL SCRIPT
rol, usuario_campus = login()

while True:
    print("\n¿QUÉ QUIERES HACER?")
    if rol == "admin":
        print("1. Ver dispositivos")
        print("2. Ver campus")
        print("3. Agregar dispositivo")
        print("4. Crear campus")
        print("5. Eliminar dispositivo")
        print("6. Eliminar campus")
        print("7. Opciones de backup")
        print("8. Salir")
        op = input("Opción: ")
        if op == "1":
            print("Selecciona un campus para ver sus dispositivos:")
            for i, c in enumerate(campus, 1):
                print(f"{i}. {c}")
            idx = int(input("Campus: ")) - 1
            if 0 <= idx < len(campus):
                mostrar_dispositivos(campus[idx])
            else:
                print("Opción inválida.")
        elif op == "2":
            print("Campus disponibles:")
            for c in campus:
                print("-", c)
        elif op == "3":
            print("Selecciona un campus para agregar el dispositivo:")
            for i, c in enumerate(campus, 1):
                print(f"{i}. {c}")
            idx = int(input("Campus: ")) - 1
            if 0 <= idx < len(campus):
                agregar_dispositivo(campus[idx])
            else:
                print("Opción inválida.")
        elif op == "4":
            crear_campus()
        elif op == "5":
            print("Selecciona un campus para eliminar dispositivos:")
            for i, c in enumerate(campus, 1):
                print(f"{i}. {c}")
            idx = int(input("Campus: ")) - 1
            if 0 <= idx < len(campus):
                eliminar_dispositivos(campus[idx])
            else:
                print("Opción inválida.")
        elif op == "6":
            eliminar_campus()
        elif op == "7":
            print("\nOpciones de Backup:")
            print("1. Crear backup")
            print("2. Restaurar backup")
            print("3. Volver al menú principal")
            backup_op = input("Opción: ")
            if backup_op == "1":
                crear_backup()
            elif backup_op == "2":
                restaurar_backup()
            elif backup_op == "3":
                continue
            else:
                print("Opción inválida.")
        elif op == "8":
            break
        else:
            print("Opción inválida.")
            
    else:
        print("1. Ver dispositivos de tu campus")
        print("2. Ver campus disponibles")
        print("3. Salir")
        op = input("Opción: ")
        if op == "1":
            mostrar_dispositivos(usuario_campus)
        elif op == "2":
            print("Campus disponibles:")
            for c in campus:
                print("-", c)
        elif op == "3":
            break
        else:
            print("Opción inválida.")