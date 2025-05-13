import os
import random

x = 0
y = 0

os.system("clear")


if os.path.exists("campus_lista.txt"):
    with open("campus_lista.txt", "r") as f:
        campus = [line.strip() for line in f if line.strip()]
else:
    campus = ["zona core", "campus uno", "campus matriz", "sector outsourcing"]
    with open("campus_lista.txt", "w") as f:
        for c in campus:
            f.write(c + "\n")

ip_ranges = {
    "zona core": (1, 50),
    "campus uno": (51, 100),
    "campus matriz": (101, 150),
    "sector outsourcing": (151, 200),
}

print("¿Qué quiere hacer?")
print("1. Ver los dispositivos. \n2. Ver los campus. \n3. Añadir dispositivo. \n4. Añadir campus. \n5. Borrar dispositivo. \n6. Borrar campus")

while True:
    try:
        selector = int(input("Elegir una opción: "))
        if selector < 1 or selector > 6:
            raise ValueError("Opción no válida.")
        break
    except ValueError as e:
        print(f"Error: {e}. Intenta nuevamente.")

if selector == 1:
    os.system("clear")
    print("Elige un campus:")
    for i, item in enumerate(campus, start=1):
        print(f"{i}. {item}")

    selector = input("\nElija una opción: ")
    x = int(selector) - 1

    if x >= 0:
        os.system("clear")
        with open(campus[x] + ".txt", "r") as file:
            print(file.read())

elif selector == 2:
    os.system("clear")
    print("Lista de campus:")
    for i, item in enumerate(campus, start=1):
        print(f"{i}. {item}")

elif selector == 3:
    os.system("clear")
    print("¿Dónde agregar el nuevo dispositivo?")
    for i, item in enumerate(campus, start=1):
        print(f"{i}. {item}")

    selector = input("\nElija una opción: ")
    x = int(selector) - 1

    if x >= 0:
        os.system("clear")
        with open(campus[x] + ".txt", "a") as file:
            print("Elija un dispositivo: \n \n1. Router. \n2. Switch. \n3. Switch multicapa. \n")
            while True:
                try:
                    variable1 = int(input("Elija su opción: "))
                    if variable1 < 1 or variable1 > 3:
                        raise ValueError("Opción no válida.")
                    break
                except ValueError as e:
                    print(f"Error: {e}. Intenta nuevamente.")

            os.system("clear")
            print("Agregue el nombre de su dispositivo")
            variable2 = input("Agregue su nombre: ")

            while True:
                print("¿Confirma este nombre? \n \n1. Sí \n2. No \n")
                variable3 = input("Introduzca su respuesta: ")
                if variable3 == "1":
                    print("Terminado")
                    break

            print("Elija una jerarquía: \n \n1. Nucleo, \n2. Acceso. \n3. Distribución. \n")
            while True:
                try:
                    variable3 = int(input("Elija una opción: "))
                    if variable3 < 1 or variable3 > 3:
                        raise ValueError("Opción no válida.")
                    break
                except ValueError as e:
                    print(f"Error: {e}. Intenta nuevamente.")

            campus_name = campus[x]
            ip_range_start, ip_range_end = ip_ranges.get(campus_name, (201, 250))

            while True:
                ip = input(f"Ingrese la IP del dispositivo (ej: 192.168.20.10): ")
                partes = ip.strip().split(".")

                if len(partes) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in partes):
                    ultimo_octeto = int(partes[3])
                    if ip_range_start <= ultimo_octeto <= ip_range_end:
                        break
                    else:
                        print(f"El último octeto ({ultimo_octeto}) no está permitido para {campus_name}. Debe estar entre {ip_range_start} y {ip_range_end}.")
                else:
                    print("IP no válida. Usa el formato correcto y valores entre 0-255.")

            file.write("\n---------------------------------\n")
            file.write(f"Nombre del dispositivo: {variable2}\n")
            file.write(f"IP: {ip}\n")

            if variable3 == 1:
                file.write("Jerarquía: Nucleo\n")
            elif variable3 == 2:
                file.write("Jerarquía: Distribución\n")
            elif variable3 == 3:
                file.write("Jerarquía: Acceso\n")

            vlan_input = input("¿Ingrese las VLANs configuradas (separadas por comas): ")
            vlans = vlan_input.split(",")
            file.write("VLANs: " + ", ".join(vlans) + "\n")

            servicios = []
            if variable1 == 1:
                opciones = ["Datos", "VLAN", "Trunking"]
            elif variable1 == 2:
                opciones = ["Datos", "VLAN", "Trunking"]
            elif variable1 == 3:
                opciones = ["Datos", "VLAN", "Trunking", "Enrutamiento"]

            while True:
                print("Seleccione servicios para el dispositivo:")
                for i, servicio in enumerate(opciones, start=1):
                    print(f"{i}. {servicio}")
                print(f"{len(opciones)+1}. Salir")

                try:
                    eleccion = int(input("Elija una opción: "))
                    if 1 <= eleccion <= len(opciones):
                        servicios.append(opciones[eleccion - 1])
                    elif eleccion == len(opciones) + 1:
                        break
                    else:
                        raise ValueError("Opción inválida.")
                except ValueError as e:
                    print(f"Error: {e}. Intente de nuevo.")

            file.write("Servicios: " + str(servicios) + "\n")
            file.write("---------------------------------\n")

elif selector == 4:
    os.system("clear")
    print("Añadir un nuevo campus")
    nuevo_campus = input("Ingrese el nombre del nuevo campus: ").strip()

    if nuevo_campus not in campus:
        campus.append(nuevo_campus)
        ip_ranges[nuevo_campus] = (201, 250)
        open(nuevo_campus + ".txt", "w").close()
        with open("campus_lista.txt", "a") as f:
            f.write(nuevo_campus + "\n")
        print(f"Campus {nuevo_campus} añadido correctamente.")
    else:
        print(f"El campus {nuevo_campus} ya existe.")

elif selector == 5:
    os.system("clear")
    print("Selecciona un campus para borrar un dispositivo:")
    for i, item in enumerate(campus, start=1):
        print(f"{i}. {item}")

    selector = input("\nElija una opción: ")
    x = int(selector) - 1

    if x >= 0:
        os.system("clear")
        campus_actual = campus[x]
        print(f"Dispositivos en {campus_actual}:")

        with open(campus_actual + ".txt", "r") as file:
            contenido = file.read()
            bloques = contenido.strip().split("---------------------------------")

        dispositivos_validos = []
        for i, bloque in enumerate(bloques):
            if "Nombre del dispositivo:" in bloque:
                nombre_linea = [line for line in bloque.splitlines() if "Nombre del dispositivo:" in line]
                nombre = nombre_linea[0].replace("Nombre del dispositivo: ", "") if nombre_linea else f"Desconocido {i}"
                dispositivos_validos.append((i, nombre.strip()))

        for i, (_, nombre) in enumerate(dispositivos_validos, start=1):
            print(f"{i}. {nombre}")
        print(f"{len(dispositivos_validos)+1}. Borrar todos los dispositivos")

        seleccion = int(input("Seleccione una opción: "))

        if seleccion == len(dispositivos_validos) + 1:
            open(campus_actual + ".txt", "w").close()
            print("Todos los dispositivos fueron borrados.")
        elif 1 <= seleccion <= len(dispositivos_validos):
            index_a_borrar = dispositivos_validos[seleccion - 1][0]
            bloques.pop(index_a_borrar)
            with open(campus_actual + ".txt", "w") as f:
                for bloque in bloques:
                    bloque = bloque.strip()
                    if bloque:
                        f.write(bloque.strip() + "\n---------------------------------\n")
            print("Dispositivo borrado correctamente.")
        else:
            print("Opción inválida.")

elif selector == 6:
    os.system("clear")
    print("Lista de campus para borrar:")
    for i, item in enumerate(campus, start=1):
        print(f"{i}. {item}")

    selector = input("\nElija el campus a borrar (número): ")
    try:
        x = int(selector) - 1
        if 0 <= x < len(campus):
            campus_a_borrar = campus[x]
            confirmacion = input(f"¿Estás seguro de que quieres borrar el campus {campus_a_borrar}? (1. Sí / 2. No): ")
            if confirmacion == "1":
                campus.pop(x)
                with open("campus_lista.txt", "w") as f:
                    for c in campus:
                        f.write(c + "\n")
                if campus_a_borrar in ip_ranges:
                    del ip_ranges[campus_a_borrar]
                if os.path.exists(campus_a_borrar + ".txt"):
                    os.remove(campus_a_borrar + ".txt")
                print(f"Campus {campus_a_borrar} borrado correctamente.")
            else:
                print("Operación cancelada.")
        else:
            print("Selección inválida.")
    except ValueError:
        print("Entrada no válida. Debe ser un número.")

