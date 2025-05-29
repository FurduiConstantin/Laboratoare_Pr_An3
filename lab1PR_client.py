import socket

# Definirea conexiunii la server
HOST = '127.0.0.1'  # Adresa serverului
PORT = 65433       # Portul serverului

# Creăm socket-ul clientului
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Funcție pentru a asculta mesajele primite de la server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            break

# Pornim un thread pentru a asculta mesajele de la server
import threading
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Transmiterea mesajelor de la utilizator către server
while True:
    message = input("Introduceți mesajul de trimis: ")
    client_socket.send(message.encode('utf-8'))
