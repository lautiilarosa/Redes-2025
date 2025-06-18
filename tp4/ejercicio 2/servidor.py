import socket
import threading
import sys

# Variable global para llevar el control de clientes conectados
clientes_conectados = {}
lock = threading.Lock()

def handle_client(client_socket, addr):
    global clientes_conectados
    print(f"Conexión establecida con {addr}")
    
    with lock:
        clientes_conectados[addr] = client_socket
    
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data or data.lower() == "exit":
                print(f"Cliente {addr} se desconectó.")
                break
            print(f"Cliente {addr} dice: {data}")
    except ConnectionResetError:
        print(f"Conexión con {addr} perdida inesperadamente")
    finally:
        client_socket.close()
        with lock:
            del clientes_conectados[addr]

def handle_server_input():
    """Maneja la entrada del servidor para enviar mensajes o cerrar"""
    global clientes_conectados
    while True:
        message = input("Ingrese algo: ")
        
        if message.lower() == "exit":
            with lock:
                if clientes_conectados:
                    print("No es posible cerrar el proceso servidor si hay un cliente conectado")
                else:
                    print("Cerrando servidor...")
                    os._exit(0)
        else:
            with lock:
                for addr, sock in list(clientes_conectados.items()):
                    try:
                        sock.send(message.encode())
                    except:
                        print(f"No se pudo enviar mensaje a {addr}")
                        del clientes_conectados[addr]

def start_server():
    global clientes_conectados
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 5000))
    server_socket.listen(5)
    print("Servidor escuchando en el puerto 5000...")

    # Hilo para manejar la entrada del servidor
    input_thread = threading.Thread(target=handle_server_input, daemon=True)
    input_thread.start()

    try:
        while True:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("\nIntentando cerrar servidor...")
        with lock:
            if clientes_conectados:
                print("No es posible cerrar el proceso servidor si hay un cliente conectado")
                # Continuar ejecución
            else:
                print("Cerrando servidor...")
                server_socket.close()
                sys.exit(0)
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    import os
    start_server()