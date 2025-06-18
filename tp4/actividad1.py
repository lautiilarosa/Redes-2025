import socket
import threading

# Configuración del socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 60000))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

user = input("Introduzca nombre de usuario: ")
finalizado = threading.Event()

# Notificar ingreso al chat
sock.sendto(f"{user}:nuevo".encode(), ('255.255.255.255', 60000))

def enviar_mensajes():
    while not finalizado.is_set():
        mensaje = input("Escriba Mensaje: ")
        if mensaje.lower() == "exit":
            sock.sendto(f'{user}:exit'.encode(), ('255.255.255.255', 60000))
            finalizado.set()
            break
        sock.sendto(f'{user}:{mensaje}'.encode(), ('255.255.255.255', 60000))

def recibir_mensajes():
    while not finalizado.is_set():
        try:
            data, addr = sock.recvfrom(1024)
            decoded = data.decode()
            if ":" not in decoded:  
                continue
                
            remitente, contenido = decoded.split(":", 1)
            ip_remitente = addr[0]

            if contenido == "nuevo":
                print(f"El usuario {remitente} se ha unido a la conversación.")
            elif contenido == "exit":
                print(f"El usuario {remitente} ({ip_remitente}) ha abandonado la conversación.")
                if remitente == user:  # Soy yo quien salió
                    break
            else:
                print(f"{remitente} ({ip_remitente}) dice: {contenido}")
        except Exception as e:
            if finalizado.is_set():
                break
            print(f"Error: {e}")

# Crear hilos
enviar_hilo = threading.Thread(target=enviar_mensajes)
recibir_hilo = threading.Thread(target=recibir_mensajes, daemon=True)

enviar_hilo.start()
recibir_hilo.start()

enviar_hilo.join()  # Esperar a que termine el hilo de envío
sock.close()  # Cerrar socket al final