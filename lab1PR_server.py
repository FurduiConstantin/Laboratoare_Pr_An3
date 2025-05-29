import socket
import threading

# Definirea serverului
HOST = '127.0.0.1'  # Adresa IP locală
PORT = 65433      # Portul serverului

# Lista pentru clienții conectați
clients = []

# Funcție care va asculta și va trata clienții
def handle_client(client_socket, addr):
    print(f"Client conectat: {addr}")
    
    # Adăugăm clientul la lista de clienți
    clients.append(client_socket)

    # Ascultăm mesajele de la client
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Mesaj de la {addr}: {message}")
                
                # Retransmite mesajul la toți clienții
                for client in clients:
                    try:
                        client.send(f"{addr} spune: {message}".encode('utf-8'))
                    except:
                        continue
        except:
            break
    
    # Închidem conexiunea clientului când acesta se deconectează
    clients.remove(client_socket)
    client_socket.close()

# Creăm serverul și îl pornim
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Serverul este pornit pe {HOST}:{PORT}...")

while True:
    # Așteptăm conexiuni de la clienți
    client_socket, addr = server_socket.accept()
    
    # Creăm un thread pentru fiecare client care se conectează
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
