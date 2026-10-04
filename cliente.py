import sys

import requests

API_URL = "http://127.0.0.1:5000"


def menu():
    print("\n--- Sistema de Gestion de Tareas (PFO 2) ---")
    print("1. Registrarse")
    print("2. Iniciar sesion")
    print("3. Ver tareas (HTML de bienvenida)")
    print("4. Salir")
    return input("Opcion: ")


def pedir_credenciales():
    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")
    return {"usuario": usuario, "contraseña": contrasena}


def main():
    while True:
        opcion = menu()

        if opcion == "1":
            datos = pedir_credenciales()
            try:
                respuesta = requests.post(f"{API_URL}/registro", json=datos)
            except requests.exceptions.ConnectionError:
                print("Error: no se pudo conectar. Asegurate de que el servidor este corriendo.")
                continue
            print(respuesta.json().get("mensaje", respuesta.json().get("error")))

        elif opcion == "2":
            datos = pedir_credenciales()
            try:
                respuesta = requests.post(f"{API_URL}/login", json=datos)
            except requests.exceptions.ConnectionError:
                print("Error: no se pudo conectar. Asegurate de que el servidor este corriendo.")
                continue
            print(respuesta.json().get("mensaje", respuesta.json().get("error")))

        elif opcion == "3":
            try:
                respuesta = requests.get(f"{API_URL}/tareas")
            except requests.exceptions.ConnectionError:
                print("Error: no se pudo conectar. Asegurate de que el servidor este corriendo.")
                continue
            print("HTTP", respuesta.status_code)
            print(respuesta.text[:200])

        elif opcion == "4":
            print("Hasta luego.")
            sys.exit(0)

        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    main()