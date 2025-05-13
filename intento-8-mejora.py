import os

ADMIN_PASSWORD = "victomonan1"
CAMPUS_LIST_FILE = "campus_lista.txt"
USUARIOS_FILE = "usuarios.txt"

# Cargar o crear lista de campus
if os.path.exists(CAMPUS_LIST_FILE):
    with open(CAMPUS_LIST_FILE, "r") as f:
        campus = [line.strip() for line in f if line.strip()]
else:
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
        if not os.path.exists(USUARIOS_FILE):
            open(USUARIOS_FILE, "w").close()

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
    if os.path.exists(archivo):
        with open(archivo, "r") as f:
            contenido = f.read().strip()
            if contenido:
                print(f"\nDispositivos en {campus_actual}:")
                print(contenido)
            else:
                print("No hay dispositivos registrados en este campus.")
    else:
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
    print("Tipo de dispositivo:\n1. Router\n2. Switch\n3. Switch Multicapa")
    tipo = int(input("Opción: "))
    nombre = input("Nombre del dispositivo: ")
    print("Jerarquía:\n1. Núcleo\n2. Distribución\n3. Acceso")
    jerarquia = int(input("Opción: "))
    jerarquia_txt = ["Núcleo", "Distribución", "Acceso"][jerarquia - 1]

    penultimo = campus_octetos.get(campus_actual, 90)
    while True:
        ip = input(f"Ingresa la IP (ej: 172.16.{penultimo}.X): ")
        partes = ip.strip().split(".")
        if len(partes) == 4 and all(p.isdigit() for p in partes):
            if int(partes[2]) == penultimo and 1 <= int(partes[3]) <= 50:
                break
        print("IP inválida. Penúltimo octeto debe ser", penultimo, "y el último entre 1-50") 
    if tipo == 4:
        with open(archivo, "a") as f:
            f.write("\n-------------------------\n")
            f.write(f"nombre del dispositivo: {nombre}\n")
            f.write(f"IP: {ip}\n")
            f.write("\--------------------------\n")
        return
        
    vlans = input("Ingrese las VLANs (separadas por coma): ").split(",")

    servicios_opciones = ["Datos", "VLAN", "Trunking"]
    if tipo == 3:
        servicios_opciones.append("Enrutamiento")
    servicios = []
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
        if tipo != 4:
            f.write(f"Jerarquía: {jerarquia_txt}\n")
            f.write("VLANs: " + ", ".join(vlans) + "\n")
            f.write("Servicios: " + ", ".join(servicios) + "\n")
            f.write("---------------------------------\n")

def eliminar_dispositivos(campus_actual):
    archivo = campus_actual + ".txt"
    if not os.path.exists(archivo):
        print("No hay dispositivos para eliminar.")
        return
    with open(archivo, "r") as f:
        contenido = f.read()
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
        print("7. Salir")
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






