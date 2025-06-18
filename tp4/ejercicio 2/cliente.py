import socket
import threading

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            print(f"Mensaje recibido: {data}")
        except:
            break

def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = input("Ingrese la ip: ")
    sock.connect((host, 5000))  

    receive_thread = threading.Thread(target=receive_messages, args=(sock,))
    receive_thread.daemon = True
    receive_thread.start()

    try:
        while True:
            message = input()
            sock.send(message.encode())
            if message.lower() == "exit":
                break
    finally:
        sock.close()

if __name__ == "__main__":
    start_client()