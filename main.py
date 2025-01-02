import os
import sys
import time
import socket
import logging
import subprocess
from datetime import datetime
import netifaces

# Configurar el logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def obtener_ip_externa():
    try:
        ip_externa = subprocess.check_output(['curl', 'ifconfig.me']).decode('utf-8').strip()
        return ip_externa
    except Exception as e:
        logging.error(f"Error al obtener la IP externa: {e}")
        return "Desconocida"

def obtener_estado_conexion():
    try:
        eth_interfaces = netifaces.interfaces()
        for interface in eth_interfaces:
            if netifaces.AF_INET in netifaces.ifaddresses(interface):
                return "ETHERNET", netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
        return "WIFI", socket.gethostbyname(socket.gethostname())
    except Exception as e:
        logging.error(f"Error al obtener el estado de la conexion: {e}")
        return "Desconocida", "Desconocida"

def enviar_wol(mac_address):
    try:
        logging.info(f"Enviando paquete WOL a {mac_address}")
        os.system(f"wakeonlan {mac_address}")
    except Exception as e:
        logging.error(f"Error al enviar paquete WOL: {e}")

def mostrar_menu():
    print("\n=== Menu ===")
    print("1. Enviar paquete WOL")
    print("2. Mostrar estado de la conexion")
    print("3. Reiniciar script")
    print("4. Salir")

def main():
    while True:
        tipo_conexion, ip_local = obtener_estado_conexion()
        ip_externa = obtener_ip_externa()

        print(f"\nEstado de la conexion: {tipo_conexion}")
        print(f"IP Local: {ip_local} | IP Externa: {ip_externa}")

        mostrar_menu()

        opcion = input("Selecciona una opcion: ")

        if opcion == '1':
            mac_address = input("Introduce la direccion MAC del dispositivo: ")
            enviar_wol(mac_address)
        elif opcion == '2':
            print(f"Estado de la conexion: {tipo_conexion}")
            print(f"IP Local: {ip_local}")
            print(f"IP Externa: {ip_externa}")
        elif opcion == '3':
            logging.info("Reiniciando script...")
            main()
        elif opcion == '4':
            logging.info("Saliendo del script...")
            break
        else:
            print("Opcion no valida. Por favor, selecciona una opcion del menu.")

if __name__ == "__main__":
    main()
